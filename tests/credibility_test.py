from credibility_framework import credibility_framework

# Test the credibility framework
print("🔒 Testing Luciq Credibility Framework...")

original = "This is a basic business analysis response."
enhanced = credibility_framework.enhance_response_with_credibility(
    response=original,
    insight_type='general',
    confidence_score=0.75,
    sources_used=['semantic_analysis', 'business_intelligence']
)

print("✅ Credibility framework working!")
print("\nOriginal:", original)
print("\n" + "="*50)
print("ENHANCED WITH CREDIBILITY ASSESSMENT:")
print("="*50)
print(enhanced) 