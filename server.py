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

