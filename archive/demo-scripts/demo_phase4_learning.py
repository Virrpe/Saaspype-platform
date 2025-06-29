#!/usr/bin/env python3
"""
🔮 Phase 4 Predictive Analytics & Learning System Demo
Comprehensive demonstration of all new Phase 4 enhancements
"""

import requests
import json
import time
from datetime import datetime

class Phase4LearningDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        print("🔮 Phase 4 Predictive Analytics & Learning System Demo")
        print("=" * 60)
    
    def check_server_status(self):
        """Check if the API server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ API Server Status: ONLINE")
                return True
            else:
                print("❌ API Server Status: ERROR")
                return False
        except Exception as e:
            print(f"❌ API Server Status: OFFLINE - {str(e)}")
            return False
    
    def demo_learning_system_status(self):
        """Demo: Real-time Learning System Status"""
        print("\n🧠 DEMO: Real-time Learning System Status")
        print("-" * 40)
        
        try:
            print("📊 Fetching learning system metrics...")
            response = requests.get(
                f"{self.base_url}/api/intelligence/learning-system-status",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Learning System Status Retrieved!")
                
                if 'learning_system_status' in result:
                    status = result['learning_system_status']
                    print(f"🔄 Learning System Active: {status.get('learning_system_active', 'Unknown')}")
                    print(f"📦 Model Version: {status.get('model_version', 'Unknown')}")
                    print(f"🔧 Feedback Integration: {status.get('feedback_integration_enabled', 'Unknown')}")
                    
                    if 'learning_metrics' in status:
                        metrics = status['learning_metrics']
                        print(f"\n📈 Learning Metrics:")
                        print(f"   Total Feedback Processed: {metrics.get('total_feedback_processed', 0)}")
                        print(f"   Average Accuracy Improvement: {metrics.get('average_accuracy_improvement', 0):.1%}")
                        print(f"   Model Updates This Month: {metrics.get('model_updates_this_month', 0)}")
                        print(f"   Prediction Confidence Trend: {metrics.get('prediction_confidence_trend', 'Unknown')}")
                
                return result
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Demo failed: {str(e)}")
            return None
    
    def run_demo(self):
        """Run the demonstration"""
        print(f"🕐 Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check server status first
        if not self.check_server_status():
            print("❌ Cannot proceed - API server is not responding")
            return False
        
        # Run demo
        result = self.demo_learning_system_status()
        
        if result:
            print("\n🎉 Phase 4 Learning System Demo Complete!")
            return True
        else:
            print("\n❌ Demo failed")
            return False

if __name__ == "__main__":
    demo = Phase4LearningDemo()
    demo.run_demo() 