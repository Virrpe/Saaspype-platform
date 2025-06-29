#!/usr/bin/env python3
"""
Test Credibility Integration in Updated ChatService
==================================================
"""

import asyncio
from master_luciq_api import ChatService, DialecticalMultimodalFusionEngine, CREDIBILITY_ENABLED

async def test_chat_service_credibility():
    """Test that ChatService now includes credibility enhancement"""
    
    print("🔒 Testing ChatService Credibility Integration")
    print("=" * 50)
    
    # Initialize chat service
    intelligence_engine = DialecticalMultimodalFusionEngine()
    chat_service = ChatService(intelligence_engine)
    
    print(f"✅ CREDIBILITY_ENABLED: {CREDIBILITY_ENABLED}")
    
    # Test message that should trigger pain point analysis
    test_message = "I'm struggling with customer retention in my SaaS product"
    
    try:
        # Process the message
        response = await chat_service.process_chat_message(test_message, user_id=1)
        
        print(f"\n📝 Response Structure:")
        for key in response.keys():
            print(f"   • {key}")
        
        ai_response = response.get('ai_response', '')
        conversation_context = response.get('conversation_context', {})
        
        print(f"\n🎯 Detected Intent: {conversation_context.get('detected_intent', 'Not set')}")
        print(f"📊 Confidence: {conversation_context.get('confidence', 'Not set')}")
        
        # Check for credibility indicators in the response
        credibility_indicators = [
            'CREDIBILITY ASSESSMENT',
            'Confidence',
            'Sources:',
            'Methodology:',
            'Validation Status:'
        ]
        
        found_indicators = []
        for indicator in credibility_indicators:
            if indicator in ai_response:
                found_indicators.append(indicator)
        
        print(f"\n🔍 Credibility Indicators Found: {len(found_indicators)}/{len(credibility_indicators)}")
        for indicator in found_indicators:
            print(f"   ✅ {indicator}")
        
        missing_indicators = [i for i in credibility_indicators if i not in found_indicators]
        for indicator in missing_indicators:
            print(f"   ❌ {indicator}")
        
        print(f"\n📋 Response Preview (first 300 chars):")
        print(ai_response[:300])
        print("...")
        
        if len(found_indicators) > 0:
            print(f"\n✅ SUCCESS: Credibility framework is working!")
        else:
            print(f"\n❌ ISSUE: No credibility indicators found")
            print(f"Response length: {len(ai_response)} characters")
            
    except Exception as e:
        print(f"❌ Error testing chat service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat_service_credibility()) 