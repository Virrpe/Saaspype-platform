#!/usr/bin/env python3
"""
🔮 Complete Phase 4 Predictive Analytics & Learning System Demo
Comprehensive demonstration of ALL new Phase 4 enhancements
"""

import requests
import json
import time
from datetime import datetime

class CompleteLearningDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        print("🔮 COMPLETE Phase 4 Predictive Analytics & Learning System Demo")
        print("=" * 70)
    
    def check_server(self):
        """Check server status"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            print("✅ API Server Status: ONLINE")
            return True
        except:
            print("❌ API Server Status: OFFLINE")
            return False
    
    def demo_1_predictive_analytics(self):
        """Demo 1: Enhanced Predictive Analytics with Content-Specific Intelligence"""
        print("\n🎯 DEMO 1: Enhanced Predictive Analytics")
        print("-" * 50)
        
        test_content = """
        Our fintech startup is facing challenges in the competitive SaaS market. 
        We're seeing high customer acquisition costs but strong retention in the 
        enterprise segment. The AI-powered solution shows promise for disruptive 
        innovation, but market timing is critical for success.
        """
        
        payload = {
            "content": test_content,
            "platform": "reddit",
            "context": {"analysis_type": "comprehensive"}
        }
        
        try:
            print("📊 Running enhanced predictive analytics...")
            response = requests.post(
                f"{self.base_url}/api/intelligence/predictive-analytics",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis Complete!")
                
                # Show enhanced forecasting
                if 'results' in result and 'trend_forecasting' in result['results']:
                    forecasting = result['results']['trend_forecasting']
                    print(f"\n📈 Multi-Horizon Forecasting:")
                    print(f"   30-day trend: {forecasting.get('trend_forecast_30d', 0):.1%}")
                    print(f"   90-day trend: {forecasting.get('trend_forecast_90d', 0):.1%}")
                    print(f"   12-month trend: {forecasting.get('trend_forecast_12m', 0):.1%}")
                    print(f"   Momentum score: {forecasting.get('momentum_score', 0):.1%}")
                    print(f"   Volatility index: {forecasting.get('volatility_index', 0):.1%}")
                    print(f"   Opportunity window: {forecasting.get('opportunity_window', 'N/A')}")
                
                # Show automated insights
                if 'automated_insights' in result['results']:
                    insights = result['results']['automated_insights']
                    print(f"\n🧠 Automated Insights ({len(insights)} generated):")
                    for i, insight in enumerate(insights[:2], 1):
                        print(f"   {i}. {insight.get('insight_type', 'Unknown').upper()}: {insight.get('insight_description', 'N/A')[:80]}...")
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Demo 1 failed: {str(e)}")
            return False
    
    def demo_2_learning_system(self):
        """Demo 2: Real-time Learning System Status"""
        print("\n🧠 DEMO 2: Real-time Learning System")
        print("-" * 50)
        
        try:
            print("📊 Fetching learning system status...")
            response = requests.get(
                f"{self.base_url}/api/intelligence/learning-system-status",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Learning System Active!")
                
                if 'learning_system_status' in result:
                    status = result['learning_system_status']
                    print(f"\n🔄 System Status:")
                    print(f"   Learning Active: {status.get('learning_system_active', False)}")
                    print(f"   Model Version: {status.get('model_version', 'Unknown')}")
                    print(f"   Feedback Integration: {status.get('feedback_integration_enabled', False)}")
                    
                    if 'learning_metrics' in status:
                        metrics = status['learning_metrics']
                        print(f"\n📈 Performance Metrics:")
                        print(f"   Total Feedback Processed: {metrics.get('total_feedback_processed', 0)}")
                        print(f"   Avg Accuracy Improvement: {metrics.get('average_accuracy_improvement', 0):.1%}")
                        print(f"   Model Updates This Month: {metrics.get('model_updates_this_month', 0)}")
                        print(f"   Trend: {metrics.get('prediction_confidence_trend', 'Unknown')}")
                    
                    if 'learning_priorities' in status:
                        priorities = status['learning_priorities']
                        print(f"\n🎯 Learning Priorities:")
                        for i, priority in enumerate(priorities, 1):
                            print(f"   {i}. {priority}")
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Demo 2 failed: {str(e)}")
            return False
    
    def demo_3_feedback_integration(self):
        """Demo 3: Feedback Integration System"""
        print("\n🔄 DEMO 3: Feedback Integration")
        print("-" * 50)
        
        # Test feedback scenario
        feedback_data = {
            "prediction_id": "demo_prediction_001",
            "actual_outcome": {
                "predicted_confidence": 0.75,
                "actual_success": True,
                "business_impact": "high",
                "prediction_accuracy": 0.82
            },
            "feedback_type": "outcome_validation"
        }
        
        try:
            print("📝 Submitting prediction feedback...")
            response = requests.post(
                f"{self.base_url}/api/intelligence/predictive-feedback",
                params={
                    "prediction_id": feedback_data["prediction_id"],
                    "feedback_type": feedback_data["feedback_type"]
                },
                json=feedback_data["actual_outcome"],
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Feedback processed successfully!")
                
                if 'feedback_result' in result:
                    feedback = result['feedback_result']
                    print(f"\n🔧 Model Updates:")
                    print(f"   Prediction ID: {feedback.get('prediction_id', 'Unknown')}")
                    print(f"   Accuracy Improvement: +{feedback.get('accuracy_improvement', 0):.1%}")
                    print(f"   Next Confidence: {feedback.get('next_prediction_confidence', 0):.1%}")
                    
                    if 'model_adjustments' in feedback:
                        adjustments = feedback['model_adjustments']
                        print(f"\n⚙️  Adjustments Made ({len(adjustments)}):")
                        for adj in adjustments:
                            print(f"   • {adj}")
                    
                    if 'learning_insights' in feedback:
                        insights = feedback['learning_insights']
                        print(f"\n💡 Learning Insights:")
                        for insight in insights:
                            print(f"   • {insight}")
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Demo 3 failed: {str(e)}")
            return False
    
    def demo_4_enhanced_capabilities(self):
        """Demo 4: Enhanced Capabilities"""
        print("\n🚀 DEMO 4: Enhanced Capabilities")
        print("-" * 50)
        
        try:
            print("📋 Fetching enhanced capabilities...")
            response = requests.get(
                f"{self.base_url}/api/intelligence/predictive-analytics-capabilities",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Capabilities Retrieved!")
                
                if 'capabilities' in result:
                    caps = result['capabilities']
                    print(f"\n🎯 Engine Information:")
                    print(f"   Name: {caps.get('engine_name', 'Unknown')}")
                    print(f"   Version: {caps.get('version', 'Unknown')}")
                    print(f"   Phase: {caps.get('phase', 'Unknown')}")
                    
                    if 'capabilities' in caps:
                        features = caps['capabilities']
                        print(f"\n🔧 Core Features ({len(features)} total):")
                        for feature in features[:4]:
                            print(f"   • {feature}")
                        if len(features) > 4:
                            print(f"   • ... and {len(features) - 4} more")
                    
                    if 'accuracy_metrics' in caps:
                        metrics = caps['accuracy_metrics']
                        print(f"\n📊 Accuracy Metrics:")
                        for metric, value in metrics.items():
                            clean_name = metric.replace('_', ' ').title()
                            print(f"   • {clean_name}: {value}")
                    
                    if 'competitive_advantage' in caps:
                        advantage = caps['competitive_advantage']
                        print(f"\n💰 Market Position:")
                        print(f"   {advantage.get('market_position', 'N/A')}")
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Demo 4 failed: {str(e)}")
            return False
    
    def run_complete_demo(self):
        """Run all demonstrations"""
        print(f"🕐 Started: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.check_server():
            print("❌ Server not available")
            return False
        
        # Run all demos
        results = []
        results.append(self.demo_1_predictive_analytics())
        results.append(self.demo_2_learning_system())
        results.append(self.demo_3_feedback_integration())
        results.append(self.demo_4_enhanced_capabilities())
        
        # Summary
        success_count = sum(results)
        print("\n" + "=" * 70)
        print("🎉 PHASE 4 COMPLETE DEMO RESULTS")
        print("=" * 70)
        print(f"✅ Successful Demos: {success_count}/4")
        
        if success_count == 4:
            print("🚀 ALL PHASE 4 ENHANCEMENTS WORKING PERFECTLY!")
            print("   • Enhanced Predictive Analytics ✅")
            print("   • Real-time Learning System ✅")
            print("   • Feedback Integration ✅")
            print("   • Advanced Capabilities ✅")
        else:
            print("⚠️  Some features need attention")
        
        print(f"🕐 Completed: {datetime.now().strftime('%H:%M:%S')}")
        return success_count == 4

if __name__ == "__main__":
    demo = CompleteLearningDemo()
    demo.run_complete_demo() 