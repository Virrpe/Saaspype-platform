#!/usr/bin/env python3
"""
Luciq Credibility Framework Demo
===============================

Demonstrates how the new credibility framework enhances AI responses 
with trust indicators, source citations, and methodology transparency.

This addresses the critical need for credible, source-backed insights
in business intelligence platforms.
"""

import asyncio
import json
from datetime import datetime
from credibility_framework import credibility_framework

def test_credibility_enhancement():
    """Test credibility framework with different types of responses"""
    
    print("🔒 LUCIQ CREDIBILITY FRAMEWORK DEMO")
    print("=" * 50)
    print()
    
    # Test 1: Pain Point Analysis Response
    print("1️⃣ PAIN POINT ANALYSIS WITH CREDIBILITY")
    print("-" * 40)
    
    original_response = """**Pain Point Analysis** - Powered by Enterprise AI

🎯 **Detection Confidence**: 85%
📊 **Analysis Method**: Multi-layer AI (CardiffNLP RoBERTa + Semantic Analysis)
🏭 **Industry Context**: SaaS

**Domain**: Software Development
**Urgency Level**: High
**Market Scope**: Mid-market ($10M-1B revenue)

**🔍 Analysis Sources**:
• Natural Language Processing (spaCy + transformers)
• Business Context Modeling (trained vocabularies)
• Pattern Recognition (validated algorithms)
• Sentiment & Intent Analysis (VADER + custom models)

**📈 Confidence Breakdown**:
• Keyword Pattern Match: 90%
• Business Context Score: 82%
• AI Model Consensus: 85%

**Next Steps**: I can validate this with market data analysis, competitive research, or solution gap identification.

*Methodology: Analysis based on enterprise NLP models with SaaS domain training.*"""
    
    # Enhance with credibility assessment
    enhanced_response = credibility_framework.enhance_response_with_credibility(
        response=original_response,
        insight_type="pain_point_analysis", 
        confidence_score=0.85,
        sources_used=['ai_analysis', 'pattern_recognition', 'semantic_analysis']
    )
    
    print(enhanced_response)
    print("\n" + "="*80 + "\n")
    
    # Test 2: Market Research Response
    print("2️⃣ MARKET RESEARCH WITH CREDIBILITY")
    print("-" * 40)
    
    market_response = """**Market Research Analysis** - Enterprise Intelligence Platform

🎯 **Market Validation Confidence**: 78%
📊 **Analysis Engine**: Market Validation AI + Enterprise Intelligence
🏭 **Industry Focus**: Fintech

**Market Size Assessment**: 82%
**Competitive Density**: 5 major players identified

**🔍 Research Sources & Methods**:
• Market Pattern Recognition (business terminology analysis)
• Competitive Intelligence Engine (validated algorithms)
• Industry Classification System (domain-trained models)
• Business Context Analysis (semantic understanding)
• Market Sizing Algorithm (multi-factor scoring)

**📈 Validation Methodology**:
• Market Signal Detection: 83%
• Industry Pattern Match: 75%
• Competitive Analysis: 73%
• Market Timing Score: 68%

**Available Deep Analysis**:
• 📊 Total Addressable Market (TAM) Assessment
• 🏭 Competitive Landscape Mapping
• 📈 Market Growth Rate Analysis
• 🎯 Customer Segment Identification
• ⚡ Market Entry Strategy Recommendations

*Data Sources: Semantic analysis of business patterns, competitive keyword detection, industry classification algorithms, and market opportunity scoring models trained on business intelligence data.*"""
    
    enhanced_market = credibility_framework.enhance_response_with_credibility(
        response=market_response,
        insight_type="market_validation",
        confidence_score=0.78,
        sources_used=['market_data', 'competitive_intelligence', 'algorithm_output']
    )
    
    print(enhanced_market)
    print("\n" + "="*80 + "\n")
    
    # Test 3: General Business Intelligence Response
    print("3️⃣ GENERAL BUSINESS INTELLIGENCE WITH CREDIBILITY")
    print("-" * 40)
    
    general_response = """**Business Intelligence Analysis** - Interesting perspective!

🧠 **AI Analysis Results**:
• Business Relevance: 72% (keyword + context analysis)
• Content Sophistication: 65% (NLP complexity score)
• Business Terms Detected: 8 (vocabulary matching)
• Industry Context: Technology (semantic classification)
• Sentiment Score: 0.15 (VADER + business context)

**🔍 Analysis Sources & Methods**:
• Natural Language Processing (spaCy + CardiffNLP RoBERTa)
• Business Vocabulary Analysis (trained terminology models)
• Sentiment Analysis (VADER + business context weighting)
• Industry Classification (semantic pattern recognition)
• Content Sophistication (dialectical analysis engine)

**Assessment**: This is a great foundational question (complexity: 0.42)

**Available Enterprise Intelligence**:
• 🔍 Business Opportunity Discovery (Pain Point Detection Engine)
• 📊 Market Trend Analysis (Market Validation Engine + competitive intelligence)
• 💡 Pain Point Identification (Advanced semantic analysis + pattern recognition)
• ⚡ Solution Gap Analysis (Bootstrap feasibility assessment + competitive advantage scoring)
• 📈 Predictive Analytics (Trend forecasting + timing optimization)

**📊 Analysis Confidence**: 72% based on business terminology, context understanding, and semantic relevance.

*Methodology: Multi-layered AI analysis combining NLP, sentiment analysis, business intelligence patterns, and industry classification using enterprise-grade algorithms trained on business intelligence data.*

What specific intelligence area would you like to explore in depth?"""
    
    enhanced_general = credibility_framework.enhance_response_with_credibility(
        response=general_response,
        insight_type="general",
        confidence_score=0.72,
        sources_used=['semantic_analysis', 'keyword_analysis', 'business_intelligence']
    )
    
    print(enhanced_general)
    print("\n" + "="*80 + "\n")
    
    # Test 4: Low Confidence Response
    print("4️⃣ LOW CONFIDENCE ANALYSIS (TRANSPARENCY)")
    print("-" * 40)
    
    low_confidence_response = """**Initial Assessment** (45% confidence)

🔍 **Detection Method**: Keyword analysis + business context modeling
📊 **Business Relevance**: 45% based on terminology patterns

**Note**: For deeper analysis with higher confidence, I can run advanced AI models including:
• Pain Point Detection Engine
• Market Validation Analysis  
• Competitive Landscape Scan

*Recommendation*: Run comprehensive analysis for validated insights."""
    
    enhanced_low = credibility_framework.enhance_response_with_credibility(
        response=low_confidence_response,
        insight_type="preliminary_analysis",
        confidence_score=0.45,
        sources_used=['keyword_analysis']
    )
    
    print(enhanced_low)
    print("\n" + "="*80 + "\n")
    
    print("✅ CREDIBILITY FRAMEWORK BENEFITS:")
    print("• **Trust Indicators**: Clear confidence levels with color-coded badges")
    print("• **Source Attribution**: Detailed methodology and data source citations")
    print("• **Transparency**: Validation status and analysis limitations disclosed")
    print("• **Traceability**: Analysis timestamp and methodology documentation")
    print("• **Professional Standards**: Enterprise-grade credibility assessment")
    print()
    print("🎯 **RESULT**: Every AI insight now includes comprehensive credibility assessment")
    print("   making Luciq suitable for business decision-making where trust is critical!")

if __name__ == "__main__":
    test_credibility_enhancement() 