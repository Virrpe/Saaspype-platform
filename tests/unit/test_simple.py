import requests
import time

print("🔍 Testing Simple API Server...")

try:
    response = requests.get('http://127.0.0.1:8002/health', timeout=5)
    print(f"✅ Health Check Status: {response.status_code}")
    print(f"📊 Response: {response.json()}")
except Exception as e:
    print(f"❌ Connection failed: {e}")

try:
    response = requests.get('http://127.0.0.1:8002/', timeout=5)
    print(f"✅ Root Endpoint Status: {response.status_code}")
    print(f"📊 Response: {response.json()}")
except Exception as e:
    print(f"❌ Root endpoint failed: {e}")

try:
    response = requests.get('http://127.0.0.1:8002/docs', timeout=5)
    print(f"✅ Docs Status: {response.status_code}")
    print(f"📄 Docs Size: {len(response.content)} bytes")
except Exception as e:
    print(f"❌ Docs failed: {e}") 