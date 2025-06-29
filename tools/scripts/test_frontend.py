#!/usr/bin/env python3
"""
Test frontend pages accessibility
"""
import requests

def test_url(name, url):
    try:
        response = requests.get(url, timeout=5)
        print(f"{name}: {response.status_code} - {url}")
        return response.status_code == 200
    except Exception as e:
        print(f"{name}: ERROR - {e}")
        return False

def main():
    print("🧪 Testing Frontend Pages")
    print("=" * 40)
    
    base_url = "http://localhost:3000"
    
    # Test frontend pages
    pages = [
        ("Landing Page", f"{base_url}/src/frontend/index.html"),
        ("Dashboard", f"{base_url}/src/frontend/dashboard.html"),
        ("Admin Panel", f"{base_url}/src/frontend/admin.html"),
        ("Component Demo", f"{base_url}/src/components/demo.html")
    ]
    
    for name, url in pages:
        test_url(name, url)
    
    print("\n🎨 Testing V2 Components")
    print("=" * 40)
    
    # Test V2 components
    components = [
        ("Design Tokens", f"{base_url}/src/components/foundation/design-tokens.css"),
        ("Component Library", f"{base_url}/src/components/component-library.js"),
        ("Button Component", f"{base_url}/src/components/foundation/Button.js"),
        ("Input Component", f"{base_url}/src/components/foundation/Input.js"),
        ("MetricCard Component", f"{base_url}/src/components/data-display/MetricCard.js")
    ]
    
    for name, url in components:
        test_url(name, url)

if __name__ == "__main__":
    main() 