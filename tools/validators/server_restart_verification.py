#!/usr/bin/env python3
"""
Server Restart Verification
Confirms both frontend and backend servers are running with optimized dashboard
"""

import requests
import time
import subprocess
import sys

class ServerVerifier:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:8000"
        self.dashboard_url = f"{self.frontend_url}/pages/core/trial-dashboard.html"
        
    def check_backend_health(self):
        """Check if FastAPI backend is running"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend (Port 8000): HEALTHY")
                return True
            else:
                print(f"⚠️ Backend (Port 8000): Status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Backend (Port 8000): NOT RESPONDING - {e}")
            return False
    
    def check_frontend_server(self):
        """Check if frontend HTTP server is running"""
        try:
            response = requests.get(self.dashboard_url, timeout=5)
            if response.status_code == 200:
                print("✅ Frontend (Port 3000): SERVING CONTENT")
                return True
            else:
                print(f"⚠️ Frontend (Port 3000): Status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Frontend (Port 3000): NOT RESPONDING - {e}")
            return False
    
    def verify_dashboard_optimizations(self):
        """Verify the dashboard contains our optimizations"""
        try:
            response = requests.get(self.dashboard_url, timeout=5)
            content = response.text
            
            print("\n🔍 VERIFYING DASHBOARD OPTIMIZATIONS:")
            
            # Check for multiple opportunities
            opportunity_count = content.count('opportunity-card')
            print(f"   📊 Opportunity Cards: {opportunity_count} (Target: 3+)")
            
            # Check for trust signals
            has_testimonials = "Found my $2M" in content
            has_ssl_badge = "SSL Secured" in content
            has_user_count = "500+ Active Users" in content
            
            print(f"   🛡️ Testimonials: {'✅' if has_testimonials else '❌'}")
            print(f"   🔒 SSL Badge: {'✅' if has_ssl_badge else '❌'}")
            print(f"   👥 User Count: {'✅' if has_user_count else '❌'}")
            
            # Check for single upgrade CTA
            upgrade_buttons = content.count('Upgrade to Professional')
            print(f"   🎯 Upgrade CTAs: {upgrade_buttons} (Target: 1)")
            
            # Check for FontAwesome
            has_fontawesome = "font-awesome" in content
            print(f"   🎨 FontAwesome Icons: {'✅' if has_fontawesome else '❌'}")
            
            # Check for enhanced styling
            has_btn_secondary = "btn-secondary" in content
            has_hover_effects = "hover" in content
            print(f"   💫 Enhanced Styling: {'✅' if has_btn_secondary and has_hover_effects else '❌'}")
            
            optimizations_score = sum([
                opportunity_count >= 3,
                has_testimonials,
                has_ssl_badge,
                has_user_count,
                upgrade_buttons == 1,
                has_fontawesome,
                has_btn_secondary and has_hover_effects
            ])
            
            print(f"\n🏆 OPTIMIZATION SCORE: {optimizations_score}/7 ({optimizations_score/7*100:.1f}%)")
            
            return optimizations_score >= 6
            
        except Exception as e:
            print(f"❌ Dashboard Verification Failed: {e}")
            return False
    
    def check_port_availability(self):
        """Check if ports are being used"""
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, shell=True)
            output = result.stdout
            
            port_3000_active = ':3000' in output and 'LISTENING' in output
            port_8000_active = ':8000' in output and 'LISTENING' in output
            
            print(f"🔌 Port 3000 (Frontend): {'✅ ACTIVE' if port_3000_active else '❌ INACTIVE'}")
            print(f"🔌 Port 8000 (Backend): {'✅ ACTIVE' if port_8000_active else '❌ INACTIVE'}")
            
            return port_3000_active and port_8000_active
            
        except Exception as e:
            print(f"❌ Port Check Failed: {e}")
            return False
    
    def run_complete_verification(self):
        """Run complete server and optimization verification"""
        print("🚀 SERVER RESTART VERIFICATION")
        print("=" * 50)
        
        # Check ports
        ports_ok = self.check_port_availability()
        print()
        
        # Check backend
        backend_ok = self.check_backend_health()
        
        # Check frontend
        frontend_ok = self.check_frontend_server()
        
        # Verify optimizations
        optimizations_ok = self.verify_dashboard_optimizations()
        
        # Overall status
        print("\n" + "=" * 50)
        print("📊 VERIFICATION SUMMARY:")
        print(f"   🔌 Ports Active: {'✅' if ports_ok else '❌'}")
        print(f"   🔧 Backend Health: {'✅' if backend_ok else '❌'}")
        print(f"   🌐 Frontend Serving: {'✅' if frontend_ok else '❌'}")
        print(f"   🎯 Optimizations: {'✅' if optimizations_ok else '❌'}")
        
        all_systems_go = all([ports_ok, backend_ok, frontend_ok, optimizations_ok])
        
        if all_systems_go:
            print("\n🎉 ALL SYSTEMS GO! 🎉")
            print("✅ Both servers are running")
            print("✅ Dashboard optimizations are live")
            print("✅ Ready for user testing")
            print("\n🔗 ACCESS URLS:")
            print(f"   📱 Optimized Dashboard: {self.dashboard_url}")
            print(f"   🏠 Landing Page: {self.frontend_url}/pages/landing.html")
            print(f"   🔧 API Health: {self.backend_url}/health")
        else:
            print("\n⚠️ ISSUES DETECTED")
            print("Some systems need attention before full operation")
        
        return all_systems_go

if __name__ == "__main__":
    verifier = ServerVerifier()
    success = verifier.run_complete_verification() 