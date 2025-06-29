#!/usr/bin/env python3
"""
Working Master API Demo - Shows Real Data Generation
Tests actual working endpoints and demonstrates valid data output
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

class WorkingAPIDemo:
    def __init__(self):
        self.session = requests.Session()
        
    def show_api_health(self):
        """Show API health with system status"""
        print("🏥 API HEALTH & SYSTEM STATUS")
        print("=" * 50)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/health")
            if response.status_code == 200:
                data = response.json()
                print("✅ Master API is HEALTHY")
                print(f"📊 Version: {data['version']}")
                print(f"⏰ Timestamp: {data['timestamp']}")
                
                print("\n🔧 Component Status:")
                for component, status in data['components'].items():
                    print(f"  • {component}: {status}")
                
                print(f"\n💻 System Resources:")
                resources = data['system_resources']
                print(f"  • CPU: {resources['cpu_percent']}%")
                print(f"  • Memory: {resources['memory_percent']}%")
                print(f"  • Disk: {resources['disk_percent']}%")
                
                print(f"\n🚀 Consolidated Services:")
                for service, status in data['consolidated_systems'].items():
                    print(f"  • {service}: {status}")
                
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def show_system_capabilities(self):
        """Show system capabilities and active services"""
        print("\n🎯 SYSTEM CAPABILITIES")
        print("=" * 50)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/system/stats")
            if response.status_code == 200:
                data = response.json()
                
                print("✅ Active Services:")
                for service, description in data['active_services'].items():
                    print(f"  • {service}: {description}")
                
                print(f"\n📈 Performance Metrics:")
                metrics = data['performance_metrics']
                for metric, value in metrics.items():
                    print(f"  • {metric}: {value}")
                
                return data
            else:
                print(f"❌ System stats failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ System stats error: {e}")
            return None
    
    def test_intelligence_engine_working(self):
        """Test intelligence engine with correct parameters"""
        print("\n🧠 INTELLIGENCE ENGINE DEMO")
        print("=" * 50)
        
        # Try with correct parameter structure
        test_texts = [
            {
                "content": "Our startup is struggling with customer acquisition costs. We need a better way to reach potential customers without spending too much on advertising.",
                "description": "Customer Acquisition Pain Point"
            },
            {
                "content": "The SaaS market is growing rapidly. Companies are looking for better business intelligence tools that don't cost $50,000 per year like existing solutions.",
                "description": "Market Opportunity Analysis"
            }
        ]
        
        working_results = []
        
        for i, test_case in enumerate(test_texts):
            print(f"\n📝 Test Case {i+1}: {test_case['description']}")
            print(f"💬 Input: {test_case['content'][:100]}...")
            
            try:
                # Try different parameter combinations to find what works
                for attempt, params in enumerate([
                    {"content": test_case["content"]},
                    {"text": test_case["content"]},
                    {"content": test_case["content"], "analysis_type": "full"},
                    {"message": test_case["content"]}
                ]):
                    
                    response = self.session.post(
                        f"{BASE_URL}/api/intelligence/analyze",
                        json=params,
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✅ SUCCESS with parameters: {list(params.keys())}")
                        
                        # Show real results
                        if 'sentiment' in data:
                            sentiment = data['sentiment']
                            print(f"📊 Sentiment: {sentiment.get('label', 'N/A')} (score: {sentiment.get('compound', 'N/A')})")
                        
                        if 'entities' in data:
                            entities = data['entities'][:3]
                            print(f"🏷️  Key Entities: {[e.get('text', e) for e in entities]}")
                        
                        if 'business_keywords' in data:
                            keywords = data['business_keywords'][:5]
                            print(f"💼 Business Keywords: {keywords}")
                        
                        if 'opportunities' in data:
                            opportunities = data['opportunities'][:2]
                            print(f"🎯 Opportunities: {opportunities}")
                        
                        working_results.append({
                            "test_case": test_case['description'],
                            "params": params,
                            "result": data
                        })
                        break
                    else:
                        if attempt == 0:  # Only show first failure
                            print(f"⚠️  Attempt {attempt+1} failed: {response.status_code}")
                            if response.text:
                                error_data = response.text[:200]
                                print(f"   Error: {error_data}")
                
            except Exception as e:
                print(f"❌ Error in test case {i+1}: {e}")
        
        return working_results
    
    def test_mega_scraper_demo(self):
        """Test mega scraper functionality"""
        print("\n🕸️ MEGA SCRAPER DEMO")
        print("=" * 50)
        
        test_queries = [
            {"keywords": ["business automation"], "platforms": ["reddit"], "limit": 2},
            {"keywords": ["saas startup"], "platforms": ["hackernews"], "limit": 2},
            {"query": "business intelligence tools", "limit": 3}
        ]
        
        working_results = []
        
        for i, query in enumerate(test_queries):
            print(f"\n🔍 Test Query {i+1}: {query}")
            
            try:
                response = self.session.post(
                    f"{BASE_URL}/api/scraper/mega-scan",
                    json=query,
                    timeout=20
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ SUCCESS - Mega Scraper Response:")
                    print(f"📊 Data keys: {list(data.keys())}")
                    
                    if 'results' in data and data['results']:
                        print(f"📝 Results found: {len(data['results'])}")
                        sample = data['results'][0]
                        print(f"📄 Sample result: {str(sample)[:150]}...")
                    
                    if 'platforms_scanned' in data:
                        print(f"🌐 Platforms scanned: {data['platforms_scanned']}")
                    
                    working_results.append(data)
                else:
                    print(f"⚠️  Query failed: {response.status_code}")
                    if response.text:
                        print(f"   Response: {response.text[:200]}")
                
            except Exception as e:
                print(f"❌ Error in query {i+1}: {e}")
        
        return working_results
    
    def test_discovery_endpoints(self):
        """Test discovery service endpoints"""
        print("\n🔍 DISCOVERY SERVICE DEMO")
        print("=" * 50)
        
        # Try different discovery endpoints
        endpoints_to_test = [
            {"url": "/api/discovery/subreddits", "method": "GET", "description": "Available Subreddits"},
            {"url": "/api/discovery/analyze", "method": "POST", "data": {"subreddit": "entrepreneur", "limit": 3}, "description": "Reddit Analysis"},
            {"url": "/api/discovery/overnight/status", "method": "GET", "description": "Overnight Status"}
        ]
        
        working_results = []
        
        for endpoint in endpoints_to_test:
            print(f"\n🎯 Testing: {endpoint['description']}")
            print(f"🔗 {endpoint['method']} {endpoint['url']}")
            
            try:
                if endpoint['method'] == 'GET':
                    response = self.session.get(f"{BASE_URL}{endpoint['url']}")
                else:
                    response = self.session.post(
                        f"{BASE_URL}{endpoint['url']}", 
                        json=endpoint.get('data', {}),
                        timeout=20
                    )
                
                print(f"📊 Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ SUCCESS - Response preview:")
                    print(f"📝 Keys: {list(data.keys()) if isinstance(data, dict) else 'List data'}")
                    
                    if isinstance(data, dict):
                        for key, value in list(data.items())[:3]:
                            print(f"   • {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
                    elif isinstance(data, list):
                        print(f"   • List with {len(data)} items")
                        if data:
                            print(f"   • Sample item: {str(data[0])[:100]}...")
                    
                    working_results.append({
                        "endpoint": endpoint['url'],
                        "method": endpoint['method'],
                        "data": data
                    })
                else:
                    print(f"⚠️  Failed with status {response.status_code}")
                    if response.text:
                        print(f"   Error: {response.text[:200]}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return working_results
    
    def run_working_demo(self):
        """Run comprehensive working demonstration"""
        print("🚀 LUCIQ MASTER API - WORKING DATA GENERATION DEMO")
        print("=" * 70)
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 API URL: {BASE_URL}")
        
        all_results = {}
        
        # 1. Health Check
        if self.show_api_health():
            all_results['health'] = "✅ OPERATIONAL"
        
        # 2. System Capabilities
        capabilities = self.show_system_capabilities()
        if capabilities:
            all_results['capabilities'] = capabilities
        
        # 3. Intelligence Engine
        intelligence_results = self.test_intelligence_engine_working()
        if intelligence_results:
            all_results['intelligence'] = intelligence_results
        
        # 4. Mega Scraper
        scraper_results = self.test_mega_scraper_demo()
        if scraper_results:
            all_results['mega_scraper'] = scraper_results
        
        # 5. Discovery Service
        discovery_results = self.test_discovery_endpoints()
        if discovery_results:
            all_results['discovery'] = discovery_results
        
        # Summary
        print("\n" + "=" * 70)
        print("📋 DEMO SUMMARY")
        print("=" * 70)
        
        working_count = len([k for k, v in all_results.items() if v])
        total_tests = 5
        
        print(f"✅ Working Services: {working_count}/{total_tests}")
        print(f"📊 Success Rate: {(working_count/total_tests)*100:.1f}%")
        
        for service, result in all_results.items():
            status = "✅ WORKING" if result else "❌ NOT WORKING"
            print(f"   • {service}: {status}")
        
        # Save results
        with open("working_api_demo_results.json", "w") as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"\n📁 Detailed results saved to: working_api_demo_results.json")
        
        return all_results

def main():
    """Main demo function"""
    demo = WorkingAPIDemo()
    return demo.run_working_demo()

if __name__ == "__main__":
    main() 