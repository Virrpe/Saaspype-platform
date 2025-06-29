#!/usr/bin/env python3
"""
Test script for Source Credibility API endpoints
"""

import requests
import json

def test_credibility_api():
    """Test the credibility API endpoints"""
    base_url = "http://localhost:8000"
    
    try:
        print("🌐 Testing Source Credibility API Endpoints")
        print("=" * 55)
        
        # Test credibility report endpoint
        print("\n📊 Testing /api/credibility/report...")
        response = requests.get(f"{base_url}/api/credibility/report")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Credibility report endpoint working!")
            
            if data['status'] == 'success':
                report = data['data']
                print(f"  📈 Total platforms: {report['total_platforms']}")
                print(f"  📊 Average credibility: {report['summary']['average_credibility']:.3f}")
                
                if report['summary']['highest_credibility']:
                    best = report['summary']['highest_credibility']
                    print(f"  🏆 Highest: {best['platform']} ({best['score']:.3f})")
            else:
                print(f"❌ Error in response: {data['message']}")
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
        
        # Test specific platform endpoint
        print(f"\n🔍 Testing /api/credibility/platform/reddit...")
        response = requests.get(f"{base_url}/api/credibility/platform/reddit")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Platform credibility endpoint working!")
            
            if data['status'] == 'success':
                platform_data = data['data']
                score = platform_data['credibility_score']['overall_score']
                weight = platform_data['weight_multiplier']
                print(f"  🎯 Reddit credibility: {score:.3f}")
                print(f"  ⚖️ Weight multiplier: {weight:.2f}x")
            else:
                print(f"❌ Error in response: {data['message']}")
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
        
        print(f"\n🎉 API endpoint tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Is it running on port 8000?")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_credibility_api()
    exit(0 if success else 1) 