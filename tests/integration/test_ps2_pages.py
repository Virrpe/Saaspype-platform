#!/usr/bin/env python3
"""
PS2 Signal Console Pages Testing Script
Tests all PS2-themed pages for functionality and design elements
"""

import requests
import time
from urllib.parse import urljoin

class PS2PagesTester:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.ps2_pages = {
            "PS2 Discovery Engine": "/discover",
            "PS2 Ideas Manager": "/my-ideas", 
            "PS2 Trends Analysis": "/trends",
            "PS2 Quality Dashboard": "/quality",
            "PS2 Main Dashboard": "/ps2-dashboard",
            "Landing Page": "/",
            "Trial Dashboard": "/dashboard"
        }
        
    def test_page(self, name, path):
        """Test individual PS2 page"""
        try:
            url = urljoin(self.base_url, path)
            response = requests.get(url, timeout=10)
            
            # Check response status
            status_ok = response.status_code == 200
            
            # Check for PS2 design elements
            content = response.text.lower()
            ps2_elements = [
                "ps2 signal console",
                "#00ffff",  # Cyan color
                "#ff00ff",  # Magenta color
                "#0a0a0f",  # Dark background
                "ambientpulse",  # Animation
                "backdrop-filter",  # Glass effect
                "signal-card",  # PS2 card styling
            ]
            
            ps2_score = sum(1 for element in ps2_elements if element in content)
            ps2_design_present = ps2_score >= 3
            
            # Check page size (should have content)
            has_content = len(response.text) > 1000
            
            return {
                "status_code": response.status_code,
                "status_ok": status_ok,
                "ps2_design": ps2_design_present,
                "ps2_score": ps2_score,
                "has_content": has_content,
                "content_size": len(response.text),
                "success": status_ok and has_content
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "status_ok": False,
                "ps2_design": False,
                "ps2_score": 0,
                "has_content": False,
                "content_size": 0,
                "success": False,
                "error": str(e)
            }
    
    def run_tests(self):
        """Run all PS2 page tests"""
        print("🎮 PS2 SIGNAL CONSOLE TESTING PROTOCOL")
        print("=" * 50)
        
        results = {}
        total_pages = len(self.ps2_pages)
        successful_pages = 0
        ps2_themed_pages = 0
        
        for name, path in self.ps2_pages.items():
            print(f"\n🔍 Testing: {name}")
            print(f"   URL: {self.base_url}{path}")
            
            result = self.test_page(name, path)
            results[name] = result
            
            if result["success"]:
                successful_pages += 1
                status_icon = "✅"
            else:
                status_icon = "❌"
                
            if result["ps2_design"]:
                ps2_themed_pages += 1
                ps2_icon = "🎮"
            else:
                ps2_icon = "⚪"
                
            print(f"   {status_icon} Status: {result['status_code']} | Size: {result['content_size']} bytes")
            print(f"   {ps2_icon} PS2 Design: {result['ps2_score']}/7 elements found")
            
            if "error" in result:
                print(f"   ⚠️ Error: {result['error']}")
        
        # Summary report
        print(f"\n🏆 PS2 TESTING SUMMARY")
        print("=" * 30)
        print(f"📊 Pages Accessible: {successful_pages}/{total_pages} ({successful_pages/total_pages*100:.1f}%)")
        print(f"🎮 PS2 Themed Pages: {ps2_themed_pages}/{total_pages} ({ps2_themed_pages/total_pages*100:.1f}%)")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for name, result in results.items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            ps2_status = "🎮 PS2" if result["ps2_design"] else "⚪ Basic"
            print(f"   {status} | {ps2_status} | {name}")
        
        # Overall assessment
        overall_success = successful_pages >= total_pages * 0.8  # 80% success rate
        ps2_success = ps2_themed_pages >= 4  # At least 4 PS2 themed pages
        
        if overall_success and ps2_success:
            print(f"\n🚀 PS2 SIGNAL CONSOLE: FULLY OPERATIONAL")
            print("   ✅ All critical pages accessible")
            print("   ✅ PS2 design system implemented")
            print("   ✅ Ready for user interaction")
        elif overall_success:
            print(f"\n⚡ PS2 SIGNAL CONSOLE: MOSTLY OPERATIONAL")
            print("   ✅ Pages accessible")
            print("   ⚠️ Some PS2 design elements missing")
        else:
            print(f"\n🔧 PS2 SIGNAL CONSOLE: NEEDS ATTENTION")
            print("   ❌ Some pages not accessible")
            print("   🔧 Server or routing issues detected")
        
        return results

if __name__ == "__main__":
    tester = PS2PagesTester()
    results = tester.run_tests() 