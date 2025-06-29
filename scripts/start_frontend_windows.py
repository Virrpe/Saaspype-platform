# -*- coding: utf-8 -*-
import sys
import os
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import mimetypes

# Ensure UTF-8 encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

class LuciqHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route mapping for Luciq pages
        routes = {
            '/': 'src/frontend/pages/core/landing.html',
            '/dashboard': 'src/frontend/pages/core/dashboard.html', 
            '/discovery': 'src/frontend/pages/core/discovery.html',
            '/home': 'src/frontend/pages/core/home.html',
            '/performance': 'src/frontend/pages/core/performance.html',
            '/discover': 'src/frontend/pages/features/discover.html',
            '/my-ideas': 'src/frontend/pages/features/my-ideas.html',
            '/trends': 'src/frontend/pages/features/trends.html',
            '/quality': 'src/frontend/pages/features/quality.html',
            '/ps2-dashboard': 'src/frontend/pages/features/ps2-dashboard.html',
            '/ps2-showcase': 'src/frontend/pages/features/ps2-showcase.html',
            '/ai-terminal': 'src/frontend/pages/features/ai-terminal.html'
        }
        
        if path in routes:
            try:
                file_path = routes[path]
                if os.path.exists(file_path):
                    self.path = '/' + file_path
                else:
                    self.send_error(404, f"File not found: {file_path}")
                    return
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
                return
        
        # Handle static files
        if path.startswith('/src/'):
            file_path = path[1:]  # Remove leading slash
            if os.path.exists(file_path):
                self.path = '/' + file_path
            else:
                self.send_error(404, f"Static file not found: {file_path}")
                return
        
        super().do_GET()
    
    def guess_type(self, path):
        """Override to handle additional file types"""
        mimetype, encoding = mimetypes.guess_type(path)
        
        # Handle specific file types
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.html'):
            return 'text/html; charset=utf-8'
        elif path.endswith('.json'):
            return 'application/json'
        
        return mimetype or 'application/octet-stream'
    
    def log_message(self, format, *args):
        """Custom logging to handle Unicode properly"""
        try:
            message = format % args
            print(f"[{self.address_string()}] {message}")
        except UnicodeEncodeError:
            print(f"[{self.address_string()}] <Unicode encoding error in log>")

def run_server(port=3000):
    """Start the Luciq frontend server"""
    try:
        with socketserver.TCPServer(("", port), LuciqHandler) as httpd:
            print(f"Luciq Frontend Server starting on port {port}")
            print(f"Serving from: {os.getcwd()}")
            print(f"Access at: http://localhost:{port}")
            print("Available Routes:")
            print(f"   http://localhost:{port}/          → Landing Page")
            print(f"   http://localhost:{port}/dashboard → Trial Dashboard")
            print(f"   http://localhost:{port}/discovery → Discovery Viewer")
            print(f"   http://localhost:{port}/home      → Home Page")
            print(f"   http://localhost:{port}/performance → Performance Showcase")
            print("PS2-Themed Feature Pages:")
            print(f"   http://localhost:{port}/discover  → PS2 Discovery Engine")
            print(f"   http://localhost:{port}/my-ideas  → PS2 Ideas Manager")
            print(f"   http://localhost:{port}/trends    → PS2 Trends Analysis")
            print(f"   http://localhost:{port}/quality   → PS2 Quality Dashboard")
            print(f"   http://localhost:{port}/ps2-dashboard → PS2 Main Dashboard")
            print(f"   http://localhost:{port}/ps2-showcase → PS2 Component Showcase")
            print(f"   http://localhost:{port}/ai-terminal → PS2 AI Terminal (ARIA)")
            print("Press Ctrl+C to stop")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    print("Starting Luciq Frontend...")
    run_server(3000) 