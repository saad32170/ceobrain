#!/usr/bin/env python3
"""
Simple HTTP server for CEO Personal OS
Run this script to serve the webapp locally
Supports file editing and saving
"""

import http.server
import socketserver
import os
import webbrowser
import json
import subprocess
import threading
from pathlib import Path

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for saving and duplicating files"""
        if self.path == '/api/save':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                file_path = data.get('file')
                content = data.get('content')
                
                if not file_path or content is None:
                    self.send_error(400, "Missing file path or content")
                    return
                
                # Security: Only allow saving .md files in the ceo-personal-os directory
                if not file_path.endswith('.md'):
                    self.send_error(400, "Only .md files can be saved")
                    return
                
                # Get the base directory (where server.py is located)
                base_dir = Path(__file__).parent
                full_path = base_dir / file_path
                
                # Ensure the file is within the base directory (prevent directory traversal)
                try:
                    full_path.resolve().relative_to(base_dir.resolve())
                except ValueError:
                    self.send_error(403, "Invalid file path")
                    return
                
                # Ensure parent directories exist
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write file
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': 'File saved successfully'}).encode('utf-8'))
                
                self.log_message(f"Saved: {file_path}")
                
                # Run git operations asynchronously
                base_dir = Path(__file__).parent
                run_git_operations(base_dir)
                
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
            except Exception as e:
                self.send_error(500, f"Error saving file: {str(e)}")
        elif self.path == '/api/duplicate':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                source_path = data.get('source')
                target_path = data.get('target')
                
                if not source_path or not target_path:
                    self.send_error(400, "Missing source or target path")
                    return
                
                # Security: Only allow .md files
                if not source_path.endswith('.md') or not target_path.endswith('.md'):
                    self.send_error(400, "Only .md files can be duplicated")
                    return
                
                # Get the base directory
                base_dir = Path(__file__).parent
                source_full_path = base_dir / source_path
                target_full_path = base_dir / target_path
                
                # Ensure files are within the base directory
                try:
                    source_full_path.resolve().relative_to(base_dir.resolve())
                    target_full_path.resolve().relative_to(base_dir.resolve())
                except ValueError:
                    self.send_error(403, "Invalid file path")
                    return
                
                # Check if source file exists
                if not source_full_path.exists():
                    self.send_error(404, "Source file not found")
                    return
                
                # Check if target file already exists
                if target_full_path.exists():
                    self.send_error(409, "Target file already exists")
                    return
                
                # Ensure parent directories exist
                target_full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Read source file and write to target
                with open(source_full_path, 'r', encoding='utf-8') as src:
                    content = src.read()
                
                with open(target_full_path, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': 'File duplicated successfully',
                    'target': target_path
                }).encode('utf-8'))
                
                self.log_message(f"Duplicated: {source_path} -> {target_path}")
                
                # Run git operations asynchronously
                base_dir = Path(__file__).parent
                run_git_operations(base_dir)
                
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
            except Exception as e:
                self.send_error(500, f"Error duplicating file: {str(e)}")
        else:
            self.send_error(404, "Not found")
    
    def end_headers(self):
        # Add CORS headers for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_git_operations(base_dir):
    """
    Run git add, commit, and push operations asynchronously.
    This function runs in a separate thread to not block HTTP responses.
    Only operates on the ceo-personal-os directory, not parent directories.
    """
    def git_worker():
        try:
            # Change to the base directory
            original_dir = os.getcwd()
            base_dir_path = Path(base_dir).resolve()
            os.chdir(base_dir_path)
            
            try:
                # First, verify we're in the right git repo (not a parent repo)
                result = subprocess.run(
                    ['git', 'rev-parse', '--show-toplevel'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=str(base_dir_path)
                )
                
                if result.returncode != 0:
                    # Git not initialized in this directory
                    print("[Git] Not a git repository in ceo-personal-os. Skipping git operations.")
                    return
                
                # Verify the git root is actually our directory (not a parent)
                git_root = Path(result.stdout.strip()).resolve()
                if git_root != base_dir_path:
                    print(f"[Git] WARNING: Git repository root is {git_root}, but we want {base_dir_path}")
                    print("[Git] Parent git repository detected. Initializing new git repository in ceo-personal-os...")
                    
                    # Check if .git exists and is a file (submodule) or directory
                    git_dir = base_dir_path / '.git'
                    if git_dir.exists():
                        if git_dir.is_file():
                            # It's a submodule pointer, remove it
                            git_dir.unlink()
                        elif git_dir.is_dir():
                            # It's a directory but wrong repo, we'll init over it
                            pass
                    
                    # Initialize git in this directory
                    result = subprocess.run(
                        ['git', 'init'],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        cwd=str(base_dir_path)
                    )
                    if result.returncode != 0:
                        print(f"[Git] Failed to initialize git repository: {result.stderr}")
                        return
                    print("[Git] Git repository initialized in ceo-personal-os")
                    
                    # Verify it's now correct
                    result = subprocess.run(
                        ['git', 'rev-parse', '--show-toplevel'],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        cwd=str(base_dir_path)
                    )
                    if result.returncode == 0:
                        new_git_root = Path(result.stdout.strip()).resolve()
                        if new_git_root != base_dir_path:
                            print(f"[Git] ERROR: Still detecting wrong git root. Aborting git operations.")
                            return
                
                # Check if git is initialized (double check after potential init)
                result = subprocess.run(
                    ['git', 'status'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=str(base_dir_path)
                )
                
                if result.returncode != 0:
                    # Git not initialized or not a git repo
                    print("[Git] Not a git repository or git not available. Skipping git operations.")
                    return
                
                # Check if there are any changes (only in this directory)
                result = subprocess.run(
                    ['git', 'diff', '--quiet', 'HEAD'],
                    capture_output=True,
                    text=True,
                    cwd=str(base_dir_path)
                )
                
                has_changes = result.returncode != 0
                
                # Check for untracked files (only in this directory)
                result = subprocess.run(
                    ['git', 'ls-files', '--others', '--exclude-standard'],
                    capture_output=True,
                    text=True,
                    cwd=str(base_dir_path)
                )
                
                has_untracked = bool(result.stdout.strip())
                
                if not has_changes and not has_untracked:
                    print("[Git] No changes to commit.")
                    return
                
                # Stage all changes (only in this directory)
                print("[Git] Staging all changes in ceo-personal-os...")
                result = subprocess.run(
                    ['git', 'add', '.'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(base_dir_path)
                )
                
                if result.returncode != 0:
                    print(f"[Git] Error staging changes: {result.stderr}")
                    return
                
                # Commit changes
                print("[Git] Committing changes...")
                result = subprocess.run(
                    ['git', 'commit', '-m', 'waow'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(base_dir_path)
                )
                
                if result.returncode != 0:
                    if 'nothing to commit' in result.stdout.lower() or 'nothing to commit' in result.stderr.lower():
                        print("[Git] Nothing to commit.")
                    else:
                        print(f"[Git] Error committing: {result.stderr}")
                    return
                
                print("[Git] Commit successful.")
                
                # Push to origin
                print("[Git] Pushing to origin...")
                
                # Get current branch name
                branch_result = subprocess.run(
                    ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=str(base_dir_path)
                )
                
                branch_name = branch_result.stdout.strip() if branch_result.returncode == 0 else 'main'
                
                # Try push with upstream tracking
                result = subprocess.run(
                    ['git', 'push', '-u', 'origin', branch_name],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(base_dir_path)
                )
                
                if result.returncode != 0:
                    # If that fails, try without -u
                    result = subprocess.run(
                        ['git', 'push', 'origin', branch_name],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        cwd=str(base_dir_path)
                    )
                    
                    if result.returncode != 0:
                        # Check if it's because there's no remote
                        if 'no upstream branch' in result.stderr.lower() or 'fatal: no such remote' in result.stderr.lower():
                            print("[Git] No remote 'origin' configured. Skipping push.")
                        elif 'no such ref' in result.stderr.lower() or 'src refspec' in result.stderr.lower():
                            # Branch doesn't exist on remote, try pushing main
                            print(f"[Git] Branch {branch_name} not on remote, trying main...")
                            result = subprocess.run(
                                ['git', 'push', '-u', 'origin', 'main'],
                                capture_output=True,
                                text=True,
                                timeout=30,
                                cwd=str(base_dir_path)
                            )
                            if result.returncode != 0:
                                print(f"[Git] Error pushing: {result.stderr}")
                                return
                        else:
                            print(f"[Git] Error pushing: {result.stderr}")
                            return
                
                print("[Git] Push successful.")
                
            except subprocess.TimeoutExpired:
                print("[Git] Git operation timed out.")
            except FileNotFoundError:
                print("[Git] Git not found. Please install Git to enable auto-commit.")
            except Exception as e:
                print(f"[Git] Unexpected error: {str(e)}")
            finally:
                # Restore original directory
                try:
                    os.chdir(original_dir)
                except:
                    pass
                
        except Exception as e:
            print(f"[Git] Error in git worker thread: {str(e)}")
    
    # Run git operations in a separate thread
    thread = threading.Thread(target=git_worker, daemon=True)
    thread.start()

def main():
    # Change to the directory containing this script
    os.chdir(Path(__file__).parent)
    
    Handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n{'='*60}")
        print(f"CEO Personal OS - Web Server")
        print(f"{'='*60}")
        print(f"\nServer running at: {url}")
        print(f"Edit mode: Enabled")
        print(f"Auto-commit: Enabled")
        
        # Check git status
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=2,
                cwd=Path(__file__).parent
            )
            if result.returncode == 0:
                print(f"Git: Repository detected")
                # Check for remote
                result = subprocess.run(
                    ['git', 'remote', 'get-url', 'origin'],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    cwd=Path(__file__).parent
                )
                if result.returncode == 0:
                    print(f"Git: Remote 'origin' configured")
                else:
                    print(f"Git: No remote 'origin' (run setup-git.bat to configure)")
            else:
                print(f"Git: Not a git repository (run setup-git.bat to initialize)")
        except:
            print(f"Git: Not available or not configured")
        
        print(f"\nPress Ctrl+C to stop the server\n")
        
        # Open browser automatically
        try:
            webbrowser.open(url)
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()

