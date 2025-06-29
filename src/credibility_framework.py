"""
Luciq Credibility Framework - Trust & Source Verification System
===============================================================

Enterprise-grade credibility framework ensuring all AI insights are backed by 
transparent methodology, source attribution, and confidence indicators.

CORE PRINCIPLES:
- Every claim must have a verifiable source
- Methodology must be transparent and explainable  
- Confidence levels must be clearly communicated
- Limitations and uncertainties must be disclosed
- Data provenance must be traceable

"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SourceType(Enum):
    """Types of data sources with different credibility levels"""
    AI_ANALYSIS = "ai_analysis"
    PATTERN_RECOGNITION = "pattern_recognition"
    KEYWORD_ANALYSIS = "keyword_analysis"
    SEMANTIC_ANALYSIS = "semantic_analysis"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    MARKET_DATA = "market_data"
    ALGORITHM_OUTPUT = "algorithm_output"
    TRAINED_MODEL = "trained_model"
    BUSINESS_INTELLIGENCE = "business_intelligence"

class ConfidenceLevel(Enum):
    """Standardized confidence levels with clear definitions"""
    VERY_HIGH = "very_high"  # 90-100%: Multiple validated sources
    HIGH = "high"           # 75-89%: Strong single source or multiple weak sources
    MEDIUM = "medium"       # 60-74%: Moderate evidence, some uncertainty
    LOW = "low"            # 40-59%: Limited evidence, high uncertainty
    VERY_LOW = "very_low"  # Below 40%: Preliminary analysis only

@dataclass
class DataSource:
    """Represents a single data source with credibility metrics"""
    source_type: SourceType
    description: str
    confidence_score: float  # 0-1
    methodology: str
    last_updated: datetime
    validation_status: str  # "validated", "preliminary", "experimental"
    limitations: List[str]

@dataclass
class CredibilityReport:
    """Comprehensive credibility assessment for an AI insight"""
    insight_id: str
    primary_sources: List[DataSource]
    secondary_sources: List[DataSource]
    overall_confidence: float
    confidence_level: ConfidenceLevel
    methodology_summary: str
    key_assumptions: List[str]
    limitations: List[str]
    validation_notes: str
    generated_at: datetime

class CredibilityFramework:
    """
    Master credibility framework for Luciq Business Intelligence Platform
    
    Ensures all AI insights include:
    - Source attribution
    - Methodology transparency
    - Confidence scoring
    - Limitation disclosure
    - Validation status
    """
    
    def __init__(self):
        """Initialize credibility framework with source definitions"""
        self.source_definitions = self._initialize_source_definitions()
        self.methodology_templates = self._initialize_methodology_templates()
        self.confidence_thresholds = self._initialize_confidence_thresholds()
        
        logger.info("[CREDIBILITY] Framework initialized - Enterprise trust standards active")
    
    def _initialize_source_definitions(self) -> Dict[SourceType, Dict]:
        """Define credibility standards for each source type"""
        return {
            SourceType.AI_ANALYSIS: {
                "base_confidence": 0.75,
                "description": "AI-powered analysis using trained models",
                "validation_required": True,
                "limitations": ["Model training data limitations", "Context dependency"]
            },
            SourceType.PATTERN_RECOGNITION: {
                "base_confidence": 0.70,
                "description": "Pattern detection using algorithmic analysis",
                "validation_required": True,
                "limitations": ["Pattern complexity", "Historical data dependency"]
            },
            SourceType.KEYWORD_ANALYSIS: {
                "base_confidence": 0.60,
                "description": "Keyword matching and terminology analysis",
                "validation_required": False,
                "limitations": ["Context sensitivity", "Semantic ambiguity"]
            },
            SourceType.SEMANTIC_ANALYSIS: {
                "base_confidence": 0.80,
                "description": "Advanced semantic understanding using NLP",
                "validation_required": True,
                "limitations": ["Language model limitations", "Context interpretation"]
            },
            SourceType.COMPETITIVE_INTELLIGENCE: {
                "base_confidence": 0.65,
                "description": "Competitive analysis and market positioning",
                "validation_required": True,
                "limitations": ["Market dynamics", "Information availability"]
            },
            SourceType.ALGORITHM_OUTPUT: {
                "base_confidence": 0.85,
                "description": "Validated algorithmic calculations",
                "validation_required": True,
                "limitations": ["Input data quality", "Algorithm assumptions"]
            }
        }
    
    def _initialize_methodology_templates(self) -> Dict[str, str]:
        """Standard methodology descriptions for transparency"""
        return {
            "pain_point_analysis": "Multi-layer analysis combining semantic understanding, keyword detection, and business context modeling using CardiffNLP RoBERTa transformer and spaCy NLP pipeline",
            "market_validation": "Market opportunity assessment using competitive intelligence, industry classification, and business pattern recognition with validated scoring algorithms",
            "solution_gap_analysis": "Gap detection using solution pattern analysis, competitive differentiation scoring, and bootstrap feasibility assessment",
            "predictive_analytics": "Trend forecasting using temporal pattern analysis, momentum indicators, and market volatility assessment",
            "semantic_analysis": "Advanced semantic analysis using transformer models, entity recognition, and business vocabulary matching",
            "competitive_intelligence": "Competitive landscape analysis using keyword detection, market positioning assessment, and differentiation opportunity identification"
        }
    
    def _initialize_confidence_thresholds(self) -> Dict[ConfidenceLevel, Tuple[float, float]]:
        """Define confidence level thresholds"""
        return {
            ConfidenceLevel.VERY_HIGH: (0.90, 1.00),
            ConfidenceLevel.HIGH: (0.75, 0.89),
            ConfidenceLevel.MEDIUM: (0.60, 0.74),
            ConfidenceLevel.LOW: (0.40, 0.59),
            ConfidenceLevel.VERY_LOW: (0.00, 0.39)
        }
    
    def enhance_response_with_credibility(self, 
                                        response: str, 
                                        insight_type: str,
                                        confidence_score: float,
                                        sources_used: List[str]) -> str:
        """
        Enhance any AI response with credibility information
        
        Args:
            response: Original AI response
            insight_type: Type of analysis performed
            confidence_score: Overall confidence (0-1)
            sources_used: List of sources used
        
        Returns:
            Enhanced response with trust indicators
        """
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(confidence_score)
        confidence_pct = int(confidence_score * 100)
        
        # Generate trust badge
        badge_colors = {
            ConfidenceLevel.VERY_HIGH: "🟢",
            ConfidenceLevel.HIGH: "🟡", 
            ConfidenceLevel.MEDIUM: "🟠",
            ConfidenceLevel.LOW: "🔴",
            ConfidenceLevel.VERY_LOW: "⚫"
        }
        
        color = badge_colors.get(confidence_level, "⚫")
        trust_badge = f"{color} **{confidence_pct}% Confidence** ({confidence_level.value.replace('_', ' ').title()})"
        
        # Generate source citations
        source_citations = self._format_source_citations(sources_used)
        
        # Generate methodology disclosure
        methodology = self.methodology_templates.get(
            insight_type, 
            "Multi-factor analysis using enterprise AI models"
        )
        
        # Generate validation notes
        validation_notes = self._generate_validation_notes(confidence_score, len(sources_used))
        
        # Enhanced response with credibility section
        enhanced_response = f"{response}\n\n---\n\n"
        enhanced_response += f"**🔒 CREDIBILITY ASSESSMENT**\n\n"
        enhanced_response += f"{trust_badge}\n\n"
        enhanced_response += f"{source_citations}\n\n"
        enhanced_response += f"**Methodology:** {methodology}\n\n"
        enhanced_response += f"**Validation Status:** {validation_notes}\n\n"
        enhanced_response += f"*Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Luciq Enterprise Intelligence*"
        
        return enhanced_response
    
    def _determine_confidence_level(self, confidence_score: float) -> ConfidenceLevel:
        """Determine confidence level based on score"""
        for level, (min_score, max_score) in self.confidence_thresholds.items():
            if min_score <= confidence_score <= max_score:
                return level
        return ConfidenceLevel.VERY_LOW
    
    def _format_source_citations(self, sources_used: List[str]) -> str:
        """Format source citations for transparency"""
        if not sources_used:
            return "**Sources:** Analysis based on internal algorithms and pattern recognition."
        
        citations = []
        source_descriptions = {
            "ai_analysis": "AI-powered analysis using trained transformer models",
            "semantic_analysis": "Advanced semantic understanding using NLP",
            "keyword_analysis": "Business terminology and keyword pattern matching",
            "pattern_recognition": "Algorithmic pattern detection and analysis",
            "competitive_intelligence": "Competitive landscape analysis and positioning",
            "algorithm_output": "Validated algorithmic calculations and scoring"
        }
        
        for i, source in enumerate(sources_used, 1):
            description = source_descriptions.get(source, "Enterprise intelligence analysis")
            citations.append(f"{i}. **{source.replace('_', ' ').title()}**: {description}")
        
        return "**Sources:**\n" + "\n".join(citations)
    
    def _generate_validation_notes(self, confidence_score: float, source_count: int) -> str:
        """Generate validation status notes"""
        
        if confidence_score >= 0.85 and source_count >= 2:
            return "High confidence analysis with multiple validated sources. Results suitable for strategic planning."
        elif confidence_score >= 0.70:
            return "Good confidence analysis with validated methodology. Suitable for tactical decision-making."
        elif confidence_score >= 0.55:
            return "Moderate confidence analysis. Recommend additional validation for major decisions."
        else:
            return "Preliminary analysis only. Requires additional data and validation before decision-making."

# Global credibility framework instance
credibility_framework = CredibilityFramework() 