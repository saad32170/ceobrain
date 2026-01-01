#!/usr/bin/env python3
"""
Simple HTTP server for CEO Personal OS
Run this script to serve the webapp locally
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
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

