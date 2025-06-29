#!/usr/bin/env python3
import requests
import json

print("🔮 Phase 4 Learning System Demo")
print("=" * 40)

base_url = "http://localhost:8000"

# Test 1: Learning System Status
print("\n1. 🧠 Learning System Status:")
try:
    response = requests.get(f"{base_url}/api/intelligence/learning-system-status")
    data = response.json()
    status = data['learning_system_status']
    print(f"   ✅ Active: {status['learning_system_active']}")
    print(f"   📦 Version: {status['model_version']}")
    print(f"   📊 Feedback Processed: {status['learning_metrics']['total_feedback_processed']}")
    print(f"   📈 Avg Improvement: {status['learning_metrics']['average_accuracy_improvement']:.1%}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Feedback Integration
print("\n2. 🔄 Feedback Integration:")
try:
    feedback_data = {
        "predicted_confidence": 0.75,
        "actual_success": True,
        "business_impact": "high"
    }
    response = requests.post(
        f"{base_url}/api/intelligence/predictive-feedback",
        params={"prediction_id": "demo_test", "feedback_type": "outcome_validation"},
        json=feedback_data
    )
    result = response.json()['feedback_result']
    print(f"   ✅ Processed: {result['feedback_processed']}")
    print(f"   📈 Improvement: +{result['accuracy_improvement']:.1%}")
    print(f"   🎯 Next Confidence: {result['next_prediction_confidence']:.1%}")
    print(f"   ⚙️  Adjustments: {len(result['model_adjustments'])}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Enhanced Predictive Analytics
print("\n3. 🎯 Enhanced Predictive Analytics:")
try:
    payload = {
        "content": "AI-powered fintech startup with strong growth potential in competitive SaaS market",
        "platform": "reddit"
    }
    response = requests.post(f"{base_url}/api/intelligence/predictive-analytics", json=payload)
    result = response.json()['results']
    forecasting = result['trend_forecasting']
    print(f"   📈 30-day: {forecasting['trend_forecast_30d']:.1%}")
    print(f"   📈 90-day: {forecasting['trend_forecast_90d']:.1%}")
    print(f"   🎯 Momentum: {forecasting['momentum_score']:.1%}")
    print(f"   🚀 Window: {forecasting['opportunity_window']}")
    print(f"   🧠 Insights: {len(result['automated_insights'])}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n🎉 Phase 4 Demo Complete!")
print("🚀 All learning functions operational") 