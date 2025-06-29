#!/usr/bin/env python3
"""
Luciq Unified Frontend Startup Script
Enterprise-grade frontend server with cross-platform compatibility
Auto-detects platform and provides unified functionality
"""

import os
import sys
import platform
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import mimetypes

# Platform-specific encoding setup for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

class LuciqUnifiedHandler(SimpleHTTPRequestHandler):
    """Unified handler for Luciq frontend routing with cross-platform support"""
    
    def __init__(self, *args, **kwargs):
        # Serve from project root for proper path resolution
        project_root = Path(__file__).parent.parent  # Go up from scripts/ to project root
        super().__init__(*args, directory=str(project_root), **kwargs)
    
    def do_GET(self):
        """Handle GET requests with enterprise-grade routing"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Log the request with platform-aware formatting
        self.log_request(path)
        
        # Remove leading slash for processing
        if path.startswith('/'):
            path = path[1:]
        
        # Enterprise route mapping - comprehensive Luciq navigation
        route_map = {
            '': 'src/frontend/pages/landing.html',
            '/': 'src/frontend/pages/landing.html',
            'dashboard': 'src/frontend/pages/core/trial-dashboard.html',
            'discovery': 'src/frontend/pages/core/discovery-viewer.html',
            'home': 'src/frontend/pages/core/home.html',
            'performance': 'src/frontend/pages/performance-showcase.html',
            # PS2-themed enterprise feature pages
            'discover': 'src/frontend/pages/features/discover.html',
            'my-ideas': 'src/frontend/pages/features/my-ideas.html',
            'trends': 'src/frontend/pages/features/trends.html',
            'quality': 'src/frontend/pages/features/quality-dashboard.html',
            'ps2-dashboard': 'src/frontend/pages/features/dashboard.html',
            'ps2-showcase': 'src/frontend/pages/features/ps2-showcase.html',
            'ai-terminal': 'src/frontend/pages/features/ai-terminal.html',
            'orchestration-client': 'src/frontend/pages/features/orchestration-client.html'
        }
        
        # Route resolution with enterprise-grade error handling
        if path in route_map:
            target_path = route_map[path]
            full_path = os.path.join(self.directory, target_path)
            
            if os.path.exists(full_path) and os.path.isfile(full_path):
                self.path = '/' + target_path
                return super().do_GET()
            else:
                self.send_error(404, f"Enterprise route target not found: {target_path}")
                return
        
        # Handle static assets (CSS, JS, images) with proper MIME types
        if path.startswith('src/'):
            full_path = os.path.join(self.directory, path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                self.path = '/' + path
                return super().do_GET()
        
        # Default handling for other requests
        return super().do_GET()
    
    def guess_type(self, path):
        """Enhanced MIME type detection for enterprise assets"""
        mimetype, encoding = mimetypes.guess_type(path)
        
        # Enterprise-grade MIME type mapping
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.html'):
            return 'text/html; charset=utf-8'
        elif path.endswith('.json'):
            return 'application/json'
        elif path.endswith('.svg'):
            return 'image/svg+xml'
        elif path.endswith('.woff2'):
            return 'font/woff2'
        elif path.endswith('.woff'):
            return 'font/woff'
        
        return mimetype or 'application/octet-stream'
    
    def end_headers(self):
        """Add enterprise-grade CORS and security headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Enterprise security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        super().end_headers()
    
    def log_request(self, path):
        """Platform-aware request logging"""
        try:
            print(f"[{self.address_string()}] Request: {self.path} -> {path}")
        except UnicodeEncodeError:
            print(f"[{self.address_string()}] <Unicode encoding error in request log>")
    
    def log_message(self, format, *args):
        """Platform-aware message logging"""
        try:
            message = format % args
            print(f"[{self.address_string()}] {message}")
        except UnicodeEncodeError:
            print(f"[{self.address_string()}] <Unicode encoding error in log>")

def detect_platform():
    """Detect platform for optimized server configuration"""
    system = platform.system().lower()
    return {
        'system': system,
        'is_windows': system == 'windows',
        'is_unix': system in ['linux', 'darwin'],
        'python_version': sys.version,
        'architecture': platform.architecture()[0]
    }

def run_unified_server(port=3000):
    """Run the unified enterprise-grade frontend server"""
    platform_info = detect_platform()
    
    print("🚀 Luciq Unified Frontend Server")
    print("=" * 50)
    print(f"Platform: {platform_info['system'].title()} ({platform_info['architecture']})")
    print(f"Python: {platform_info['python_version']}")
    print(f"Server Type: {'Windows-optimized' if platform_info['is_windows'] else 'Unix-optimized'}")
    print("=" * 50)
    
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, LuciqUnifiedHandler)
        
        project_root = Path(__file__).parent.parent
        print(f"🏗️  Serving from: {project_root}")
        print(f"🌐 Access at: http://localhost:{port}")
        print(f"🎯 Enterprise-grade routing active")
        print()
        
        print("📋 Available Routes:")
        print("   Core Pages:")
        print(f"     http://localhost:{port}/          → Landing Page")
        print(f"     http://localhost:{port}/dashboard → Trial Dashboard")
        print(f"     http://localhost:{port}/discovery → Discovery Viewer")
        print(f"     http://localhost:{port}/home      → Home Page")
        print(f"     http://localhost:{port}/performance → Performance Showcase")
        print()
        print("   PS2-Themed Enterprise Features:")
        print(f"     http://localhost:{port}/discover  → PS2 Discovery Engine")
        print(f"     http://localhost:{port}/my-ideas  → PS2 Ideas Manager")
        print(f"     http://localhost:{port}/trends    → PS2 Trends Analysis")
        print(f"     http://localhost:{port}/quality   → PS2 Quality Dashboard")
        print(f"     http://localhost:{port}/ps2-dashboard → PS2 Main Dashboard")
        print(f"     http://localhost:{port}/ps2-showcase → PS2 Component Showcase")
        print(f"     http://localhost:{port}/ai-terminal → PS2 AI Terminal (ARIA)")
        print(f"     http://localhost:{port}/orchestration-client → Orchestration API Client")
        print()
        print("💡 This unified server eliminates platform duplication entropy")
        print("🔧 Enterprise-grade architecture with cross-platform compatibility")
        print("Press Ctrl+C to stop")
        print()
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()
    except OSError as e:
        if e.errno == 10048:  # Windows: Address already in use
            print(f"❌ Port {port} is already in use. Try a different port or stop the existing server.")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main entry point with argument parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Luciq Unified Frontend Server - Enterprise-grade cross-platform frontend'
    )
    parser.add_argument(
        '--port', '-p', 
        type=int, 
        default=3000, 
        help='Port to run the server on (default: 3000)'
    )
    parser.add_argument(
        '--info', 
        action='store_true', 
        help='Show platform information and exit'
    )
    
    args = parser.parse_args()
    
    if args.info:
        platform_info = detect_platform()
        print("🔍 Platform Information:")
        for key, value in platform_info.items():
            print(f"   {key}: {value}")
        return
    
    print("🎯 Starting Luciq Unified Frontend Server...")
    print("💼 Enterprise-grade business intelligence platform")
    print("🌟 Disrupting $10B+ market with sophisticated UX")
    print()
    
    run_unified_server(args.port)

if __name__ == '__main__':
    main() 