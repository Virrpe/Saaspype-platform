#!/usr/bin/env python3
"""
Luciq Frontend Startup Script
Properly configured frontend server with routing
"""

import os
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

class LuciqHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom handler for Luciq frontend routing"""
    
    def __init__(self, *args, **kwargs):
        # Serve from project root so all paths work correctly
        project_root = Path(__file__).parent
        super().__init__(*args, directory=str(project_root), **kwargs)
    
    def do_GET(self):
        """Handle GET requests with proper routing"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Log the request
        print(f"Request: {self.path} -> {path}")
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
        
        # Default routes - map to frontend directory
        if path == '' or path == '/':
            path = 'src/frontend/pages/landing.html'
        elif path == 'dashboard':
            path = 'src/frontend/pages/core/trial-dashboard.html'
        elif path == 'discovery':
            path = 'src/frontend/pages/core/discovery-viewer.html'
        elif path == 'home':
            path = 'src/frontend/pages/core/home.html'
        elif path == 'performance':
            path = 'src/frontend/pages/performance-showcase.html'
        # PS2-themed feature pages
        elif path == 'discover':
            path = 'src/frontend/pages/features/discover.html'
        elif path == 'my-ideas':
            path = 'src/frontend/pages/features/my-ideas.html'
        elif path == 'trends':
            path = 'src/frontend/pages/features/trends.html'
        elif path == 'quality':
            path = 'src/frontend/pages/features/quality-dashboard.html'
        elif path == 'ps2-dashboard':
            path = 'src/frontend/pages/features/dashboard.html'
        elif path == 'ps2-showcase':
            path = 'src/frontend/pages/features/ps2-showcase.html'
        elif path == 'ai-terminal':
            path = 'src/frontend/pages/features/ai-terminal.html'
        elif path == 'orchestration-client':
            path = 'src/frontend/pages/features/orchestration-client.html'
        
        # Check if file exists
        full_path = os.path.join(self.directory, path)
        print(f"Looking for: {full_path}")
        print(f"File exists: {os.path.exists(full_path)}")
        
        if os.path.exists(full_path) and os.path.isfile(full_path):
            print(f"Serving: {path}")
            self.path = '/' + path
            return super().do_GET()
        else:
            print(f"File not found, trying original path: {self.path}")
            # Try to serve the file as requested (for CSS, JS, etc.)
            return super().do_GET()
    
    def end_headers(self):
        """Add CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server(port=3000):
    """Run the frontend server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LuciqHTTPRequestHandler)
    
    project_root = Path(__file__).parent
    print(f"Luciq Frontend Server starting on port {port}")
    print(f"Serving from: {project_root}")
    print(f"Access at: http://localhost:{port}")
    print("\nAvailable Routes:")
    print("   http://localhost:3000/          -> Landing Page")
    print("   http://localhost:3000/dashboard -> Trial Dashboard")
    print("   http://localhost:3000/discovery -> Discovery Viewer")
    print("   http://localhost:3000/home      -> Home Page")
    print("   http://localhost:3000/performance -> Performance Showcase")
    print("\nPS2-Themed Feature Pages:")
    print("   http://localhost:3000/discover  -> PS2 Discovery Engine")
    print("   http://localhost:3000/my-ideas  -> PS2 Ideas Manager")
    print("   http://localhost:3000/trends    -> PS2 Trends Analysis")
    print("   http://localhost:3000/quality   -> PS2 Quality Dashboard")
    print("   http://localhost:3000/ps2-dashboard -> PS2 Main Dashboard")
    print("   http://localhost:3000/ps2-showcase -> PS2 Component Showcase")
    print("   http://localhost:3000/ai-terminal -> PS2 AI Terminal (ARIA)")
    print("   http://localhost:3000/orchestration-client -> Orchestration API Client")
    print("\nPress Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()

if __name__ == '__main__':
    print("Starting Luciq Frontend...")
    run_server(3000) 