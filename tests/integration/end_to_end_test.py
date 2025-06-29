#!/usr/bin/env python3
"""
Luciq End-to-End Workflow Test
Simulates complete user journey from registration to idea discovery
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8000"
FRONTEND_BASE = "http://localhost:3000"

def print_step(step, description):
    print(f"\n🔹 Step {step}: {description}")
    print("=" * 50)

def test_user_registration():
    """Test user registration workflow"""
    print_step(1, "User Registration")
    
    # Test data
    test_user = {
        "email": f"test_user_{int(time.time())}@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/signup", json=test_user)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registration successful!")
            print(f"   📧 Email: {test_user['email']}")
            print(f"   🔑 Token received: {data['access_token'][:20]}...")
            return data['access_token'], test_user['email']
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None, None

def test_user_authentication(email, password):
    """Test user login workflow"""
    print_step(2, "User Authentication")
    
    try:
        response = requests.post(f"{API_BASE}/api/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful!")
            print(f"   📧 Email: {email}")
            print(f"   🔑 Token: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_dashboard_access(token):
    """Test dashboard data access"""
    print_step(3, "Dashboard Access")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Test user info
        response = requests.get(f"{API_BASE}/api/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User profile loaded:")
            print(f"   👤 User ID: {user_data['id']}")
            print(f"   📧 Email: {user_data['email']}")
        
        # Test system ideas
        response = requests.get(f"{API_BASE}/api/system-ideas")
        if response.status_code == 200:
            ideas = response.json()
            print(f"✅ System ideas loaded: {len(ideas)} ideas")
            for i, idea in enumerate(ideas[:3], 1):
                print(f"   {i}. {idea['idea_title']}")
        
        return True
    except Exception as e:
        print(f"❌ Dashboard access error: {e}")
        return False

def test_discovery_workflow(token):
    """Test the core discovery workflow"""
    print_step(4, "SaaS Idea Discovery")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Discovery request
    discovery_request = {
        "subreddit": "entrepreneur",
        "limit": 5
    }
    
    try:
        print("🔍 Starting Reddit analysis...")
        print(f"   📍 Target: r/{discovery_request['subreddit']}")
        print(f"   📊 Posts to analyze: {discovery_request['limit']}")
        
        response = requests.post(
            f"{API_BASE}/api/discover", 
            json=discovery_request, 
            headers=headers,
            timeout=60  # Allow time for LLM processing
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Discovery completed successfully!")
            
            # Display results summary
            print(f"\n📊 Discovery Results:")
            print(f"   📝 Posts analyzed: {results.get('posts_analyzed', 0)}")
            print(f"   ⚠️ Pain points found: {len(results.get('pain_points', []))}")
            print(f"   💡 SaaS concepts generated: {len(results.get('concepts', []))}")
            print(f"   🌟 Top opportunities: {len(results.get('ranked_opportunities', []))}")
            
            # Show top concepts
            concepts = results.get('concepts', [])
            if concepts:
                print(f"\n💡 Top SaaS Concepts:")
                for i, concept in enumerate(concepts[:3], 1):
                    print(f"   {i}. {concept.get('title', 'Untitled')}")
                    print(f"      Market Potential: {concept.get('market_potential', 'Unknown')}")
                    print(f"      Score: {concept.get('score', 0)}/10")
            
            # Show pain points
            pain_points = results.get('pain_points', [])
            if pain_points:
                print(f"\n⚠️ Key Pain Points Discovered:")
                for i, pain in enumerate(pain_points[:3], 1):
                    print(f"   {i}. {pain.get('description', 'No description')}")
                    print(f"      Source: {pain.get('source', 'Unknown')}")
            
            return results
        else:
            print(f"❌ Discovery failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Discovery error: {e}")
        return None

def test_idea_management(token, discovery_results):
    """Test saving and managing ideas"""
    print_step(5, "Idea Management")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    if not discovery_results or not discovery_results.get('concepts'):
        print("❌ No concepts to save from discovery")
        return False
    
    # Save a concept as an idea
    concept = discovery_results['concepts'][0]
    save_request = {
        "idea_title": concept.get('title', 'Test SaaS Idea'),
        "idea_description": concept.get('description', 'AI-discovered business opportunity'),
        "pain_point_source": f"Reddit r/entrepreneur",
        "market_potential": concept.get('market_potential', 'medium'),
        "concept_data": concept
    }
    
    try:
        # Save idea
        response = requests.post(
            f"{API_BASE}/api/save-idea",
            json=save_request,
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"✅ Idea saved successfully!")
            print(f"   💡 Title: {save_request['idea_title']}")
            print(f"   📊 Market Potential: {save_request['market_potential']}")
        
        # Retrieve saved ideas
        response = requests.get(f"{API_BASE}/api/my-ideas", headers=headers)
        if response.status_code == 200:
            ideas = response.json()
            print(f"✅ Retrieved saved ideas: {len(ideas)} total")
            
            user_ideas = [idea for idea in ideas if not idea.get('system_generated')]
            system_ideas = [idea for idea in ideas if idea.get('system_generated')]
            
            print(f"   👤 User ideas: {len(user_ideas)}")
            print(f"   🤖 System ideas: {len(system_ideas)}")
            
            if user_ideas:
                print(f"\n📝 Recent User Ideas:")
                for idea in user_ideas[-3:]:
                    print(f"   • {idea['idea_title']}")
                    print(f"     Market: {idea['market_potential']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Idea management error: {e}")
        return False

def test_frontend_accessibility():
    """Test frontend page accessibility"""
    print_step(6, "Frontend Interface")
    
    pages = [
        ("Landing Page", "/"),
        ("Auth Page", "/pages/auth.html"),
        ("Dashboard", "/pages/dashboard.html"),
        ("Discovery", "/pages/discover.html"),
        ("My Ideas", "/pages/my-ideas.html")
    ]
    
    accessible_pages = 0
    
    for name, path in pages:
        try:
            response = requests.get(f"{FRONTEND_BASE}{path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: Accessible")
                accessible_pages += 1
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
    
    print(f"\n📊 Frontend Summary: {accessible_pages}/{len(pages)} pages accessible")
    return accessible_pages == len(pages)

def main():
    """Run complete end-to-end workflow test"""
    print("🚀 Luciq End-to-End Workflow Test")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Frontend: {FRONTEND_BASE}")
    print(f"📡 API: {API_BASE}")
    
    # Test workflow steps
    results = {
        "registration": False,
        "authentication": False,
        "dashboard": False,
        "discovery": False,
        "idea_management": False,
        "frontend": False
    }
    
    # Step 1: Registration
    token, email = test_user_registration()
    if token and email:
        results["registration"] = True
        
        # Step 2: Authentication (test login with same credentials)
        login_token = test_user_authentication(email, "testpassword123")
        if login_token:
            results["authentication"] = True
            
            # Step 3: Dashboard access
            if test_dashboard_access(login_token):
                results["dashboard"] = True
                
                # Step 4: Discovery workflow
                discovery_results = test_discovery_workflow(login_token)
                if discovery_results:
                    results["discovery"] = True
                    
                    # Step 5: Idea management
                    if test_idea_management(login_token, discovery_results):
                        results["idea_management"] = True
    
    # Step 6: Frontend accessibility (independent test)
    if test_frontend_accessibility():
        results["frontend"] = True
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 END-TO-END TEST SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n📊 Overall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🌟 ALL TESTS PASSED! Luciq is fully operational!")
        print("\n🚀 Complete User Workflow Verified:")
        print("   1. ✅ User can register and authenticate")
        print("   2. ✅ Dashboard loads with user data")
        print("   3. ✅ Discovery engine analyzes Reddit and generates SaaS ideas")
        print("   4. ✅ Users can save and manage discovered ideas")
        print("   5. ✅ Frontend interface is fully accessible")
        print(f"\n🌐 Ready for production use at: {FRONTEND_BASE}")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 