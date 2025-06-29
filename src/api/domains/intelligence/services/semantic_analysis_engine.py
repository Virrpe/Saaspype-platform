#!/usr/bin/env python3
"""
Advanced Semantic Understanding Engine - Phase 2 Implementation
Deep NLP with context understanding, intent recognition, and semantic scoring
"""

import asyncio
import logging
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import numpy as np

# Core NLP libraries
import spacy
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

# Advanced analysis libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim.downloader as api

# Temporal analysis
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

logger = logging.getLogger(__name__)

@dataclass
class SemanticScore:
    """Multi-dimensional semantic scoring for trend signals"""
    overall_score: float = 0.0
    
    # Core semantic dimensions
    context_relevance: float = 0.0      # How relevant to business/trend context
    intent_clarity: float = 0.0         # How clear the intent/purpose is
    sentiment_strength: float = 0.0     # Emotional intensity and direction
    entity_richness: float = 0.0        # Named entities and their importance
    semantic_coherence: float = 0.0     # Internal logical consistency
    innovation_potential: float = 0.0   # Novelty and innovation indicators
    
    # Metadata
    confidence_level: float = 0.0
    processing_time: float = 0.0
    detected_language: str = "en"
    
    # Detailed analysis
    extracted_entities: List[Dict] = field(default_factory=list)
    key_concepts: List[str] = field(default_factory=list)
    sentiment_breakdown: Dict = field(default_factory=dict)
    context_indicators: List[str] = field(default_factory=list)
    intent_classification: str = "unknown"

@dataclass
class ContextualSignal:
    """Enhanced signal with semantic understanding"""
    original_content: str
    processed_content: str
    semantic_score: SemanticScore
    business_context: Dict
    temporal_patterns: Dict
    related_concepts: List[str]
    similarity_cluster: Optional[str] = None

class AdvancedSemanticEngine:
    """Revolutionary semantic understanding engine for trend detection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧠 Initializing Advanced Semantic Understanding Engine...")
        
        # Initialize NLP models
        self._initialize_nlp_models()
        
        # Business and trend context knowledge
        self._initialize_business_context()
        
        # Intent classification patterns
        self._initialize_intent_patterns()
        
        # Semantic similarity models
        self._initialize_similarity_models()
        
        # Performance tracking
        self.analysis_stats = {
            'signals_processed': 0,
            'avg_processing_time': 0.0,
            'semantic_accuracy': 0.0,
            'context_detection_rate': 0.0
        }
        
        self.logger.info("✅ Advanced Semantic Engine initialized successfully")
    
    def _initialize_nlp_models(self):
        """Initialize core NLP models and pipelines"""
        try:
            # Load spaCy model for advanced NLP
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("✅ spaCy model loaded")
            
            # VADER sentiment analyzer for social media text
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            self.logger.info("✅ VADER sentiment analyzer loaded")
            
            # Transformers pipeline for advanced understanding
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("✅ Emotion classification pipeline loaded")
            
            # Zero-shot classification for intent detection
            self.intent_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("✅ Intent classification pipeline loaded")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize NLP models: {e}")
            # Fallback to basic models
            self._initialize_fallback_models()
    
    def _initialize_fallback_models(self):
        """Initialize fallback models if advanced models fail"""
        self.logger.warning("🔄 Initializing fallback NLP models...")
        try:
            import en_core_web_sm
            self.nlp = en_core_web_sm.load()
        except:
            self.nlp = None
            self.logger.warning("⚠️ spaCy model unavailable, using basic processing")
        
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.emotion_classifier = None
        self.intent_classifier = None
    
    def _initialize_business_context(self):
        """Initialize business and trend context knowledge"""
        self.business_contexts = {
            'saas_indicators': [
                'software as a service', 'subscription', 'cloud', 'platform',
                'api', 'dashboard', 'analytics', 'automation', 'integration'
            ],
            'pain_point_indicators': [
                'frustrating', 'difficult', 'time consuming', 'manual', 'broken',
                'inefficient', 'expensive', 'complicated', 'annoying', 'lacking'
            ],
            'opportunity_indicators': [
                'need', 'want', 'missing', 'gap', 'solution', 'tool', 'better way',
                'alternative', 'improvement', 'optimization', 'streamline'
            ],
            'market_timing_indicators': {
                'early': ['new', 'emerging', 'early', 'beginning', 'starting'],
                'growing': ['growing', 'increasing', 'trending', 'popular', 'rising'],
                'mature': ['established', 'competitive', 'saturated', 'crowded'],
                'declining': ['dying', 'obsolete', 'replaced', 'outdated']
            },
            'innovation_indicators': [
                'revolutionary', 'breakthrough', 'innovative', 'disruptive',
                'game changing', 'novel', 'unique', 'first', 'cutting edge'
            ]
        }
        
        # Entity importance weights
        self.entity_weights = {
            'ORG': 1.0,      # Organizations/companies
            'PRODUCT': 1.2,   # Products and services
            'MONEY': 0.8,     # Monetary values
            'PERCENT': 0.6,   # Percentages
            'PERSON': 0.4,    # People (less relevant for trends)
            'GPE': 0.3,       # Geographic entities
            'DATE': 0.2       # Dates (context dependent)
        }
    
    def _initialize_intent_patterns(self):
        """Initialize intent classification patterns"""
        self.intent_categories = [
            "problem_identification",      # Identifying problems/pain points
            "solution_seeking",           # Looking for solutions
            "product_discussion",         # Discussing existing products
            "market_analysis",           # Analyzing market opportunities
            "feature_request",           # Requesting new features
            "experience_sharing",        # Sharing experiences
            "recommendation_seeking",    # Seeking recommendations
            "trend_observation",         # Observing market trends
            "competitive_analysis",      # Analyzing competition
            "innovation_discussion"      # Discussing innovations
        ]
        
        # Intent-specific keywords
        self.intent_keywords = {
            "problem_identification": [
                "problem", "issue", "struggle", "frustrating", "broken", "lacking"
            ],
            "solution_seeking": [
                "need", "looking for", "want", "require", "solution", "tool", "help"
            ],
            "product_discussion": [
                "using", "tried", "review", "experience", "features", "product"
            ],
            "market_analysis": [
                "market", "opportunity", "business", "startup", "niche", "demand"
            ]
        }
    
    def _initialize_similarity_models(self):
        """Initialize semantic similarity models"""
        try:
            # Word2Vec model for semantic similarity
            self.word2vec_model = api.load("word2vec-google-news-300")
            self.logger.info("✅ Word2Vec model loaded")
        except:
            self.word2vec_model = None
            self.logger.warning("⚠️ Word2Vec model unavailable")
        
        # TF-IDF vectorizer for document similarity
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 3),
            min_df=2
        )
        
        # Document similarity cache
        self.similarity_cache = {}
        self.document_vectors = {}
    
    async def analyze_semantic_understanding(self, content: str, context: Dict = None) -> SemanticScore:
        """
        Perform comprehensive semantic analysis on content
        
        Args:
            content: Text content to analyze
            context: Additional context information
            
        Returns:
            SemanticScore with detailed semantic analysis
        """
        start_time = datetime.now()
        
        try:
            # Preprocess content
            processed_content = self._preprocess_content(content)
            
            # Core semantic analysis
            semantic_score = SemanticScore()
            
            # 1. Context Relevance Analysis
            semantic_score.context_relevance = await self._analyze_context_relevance(processed_content)
            
            # 2. Intent Classification
            intent_result = await self._classify_intent(processed_content)
            semantic_score.intent_clarity = intent_result['confidence']
            semantic_score.intent_classification = intent_result['intent']
            
            # 3. Sentiment Analysis (multi-dimensional)
            sentiment_result = await self._analyze_advanced_sentiment(processed_content)
            semantic_score.sentiment_strength = sentiment_result['compound_score']
            semantic_score.sentiment_breakdown = sentiment_result
            
            # 4. Entity Extraction and Scoring
            entity_result = await self._extract_and_score_entities(processed_content)
            semantic_score.entity_richness = entity_result['richness_score']
            semantic_score.extracted_entities = entity_result['entities']
            
            # 5. Semantic Coherence Analysis
            semantic_score.semantic_coherence = await self._analyze_semantic_coherence(processed_content)
            
            # 6. Innovation Potential Assessment
            semantic_score.innovation_potential = await self._assess_innovation_potential(processed_content)
            
            # 7. Key Concept Extraction
            semantic_score.key_concepts = await self._extract_key_concepts(processed_content)
            
            # 8. Context Indicators
            semantic_score.context_indicators = await self._detect_context_indicators(processed_content)
            
            # Calculate overall score
            semantic_score.overall_score = self._calculate_overall_semantic_score(semantic_score)
            
            # Metadata
            processing_time = (datetime.now() - start_time).total_seconds()
            semantic_score.processing_time = processing_time
            semantic_score.confidence_level = self._calculate_confidence_level(semantic_score)
            semantic_score.detected_language = self._detect_language(content)
            
            # Update statistics
            self._update_analysis_stats(processing_time, semantic_score)
            
            return semantic_score
            
        except Exception as e:
            self.logger.error(f"❌ Semantic analysis failed: {e}")
            return self._create_fallback_score(content)
    
    def _preprocess_content(self, content: str) -> str:
        """Preprocess content for semantic analysis"""
        if not content:
            return ""
        
        # Basic cleaning
        content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
        content = re.sub(r'@\w+', '', content)  # Remove mentions
        content = re.sub(r'#\w+', '', content)  # Remove hashtags (preserve content)
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        
        return content.strip()
    
    async def _analyze_context_relevance(self, content: str) -> float:
        """Analyze how relevant content is to business/trend context"""
        if not content:
            return 0.0
        
        relevance_score = 0.0
        content_lower = content.lower()
        
        # Check for business context indicators
        for context_type, indicators in self.business_contexts.items():
            if context_type == 'market_timing_indicators':
                continue  # Handle separately
            
            matches = sum(1 for indicator in indicators if indicator in content_lower)
            if matches > 0:
                weight = 0.2 if context_type == 'saas_indicators' else 0.15
                relevance_score += min(matches * weight, 1.0)
        
        # Normalize to 0-1 range
        return min(relevance_score, 1.0)
    
    async def _classify_intent(self, content: str) -> Dict:
        """Classify the intent of the content"""
        if not content or not self.intent_classifier:
            return {'intent': 'unknown', 'confidence': 0.0}
        
        try:
            # Use transformer-based classification
            result = self.intent_classifier(content, self.intent_categories)
            
            return {
                'intent': result['labels'][0],
                'confidence': result['scores'][0],
                'all_scores': dict(zip(result['labels'], result['scores']))
            }
        except Exception as e:
            self.logger.warning(f"Intent classification failed: {e}")
            return self._fallback_intent_classification(content)
    
    def _fallback_intent_classification(self, content: str) -> Dict:
        """Fallback intent classification using keyword matching"""
        content_lower = content.lower()
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            intent_scores[intent] = score / len(keywords)
        
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return {
                'intent': best_intent[0],
                'confidence': best_intent[1],
                'all_scores': intent_scores
            }
        
        return {'intent': 'unknown', 'confidence': 0.0}
    
    async def _analyze_advanced_sentiment(self, content: str) -> Dict:
        """Advanced multi-dimensional sentiment analysis"""
        if not content:
            return {'compound_score': 0.0}
        
        sentiment_result = {}
        
        # VADER sentiment (good for social media)
        vader_scores = self.sentiment_analyzer.polarity_scores(content)
        sentiment_result.update(vader_scores)
        
        # TextBlob sentiment
        blob = TextBlob(content)
        sentiment_result['textblob_polarity'] = blob.sentiment.polarity
        sentiment_result['textblob_subjectivity'] = blob.sentiment.subjectivity
        
        # Emotion classification
        if self.emotion_classifier:
            try:
                emotions = self.emotion_classifier(content)
                sentiment_result['emotions'] = {
                    emotion['label']: emotion['score'] 
                    for emotion in emotions
                }
            except Exception as e:
                self.logger.warning(f"Emotion classification failed: {e}")
        
        # Calculate compound sentiment strength
        vader_compound = abs(vader_scores.get('compound', 0.0))
        textblob_intensity = abs(sentiment_result.get('textblob_polarity', 0.0))
        subjectivity = sentiment_result.get('textblob_subjectivity', 0.5)
        
        sentiment_result['compound_score'] = (vader_compound + textblob_intensity + subjectivity) / 3.0
        
        return sentiment_result
    
    async def _extract_and_score_entities(self, content: str) -> Dict:
        """Extract named entities and calculate richness score"""
        if not content or not self.nlp:
            return {'richness_score': 0.0, 'entities': []}
        
        try:
            doc = self.nlp(content)
            entities = []
            
            for ent in doc.ents:
                entity_info = {
                    'text': ent.text,
                    'label': ent.label_,
                    'description': spacy.explain(ent.label_),
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'weight': self.entity_weights.get(ent.label_, 0.5)
                }
                entities.append(entity_info)
            
            # Calculate richness score
            if entities:
                total_weight = sum(entity['weight'] for entity in entities)
                unique_types = len(set(entity['label'] for entity in entities))
                richness_score = min((total_weight * unique_types) / 10.0, 1.0)
            else:
                richness_score = 0.0
            
            return {
                'richness_score': richness_score,
                'entities': entities,
                'entity_count': len(entities),
                'unique_types': len(set(entity['label'] for entity in entities))
            }
            
        except Exception as e:
            self.logger.warning(f"Entity extraction failed: {e}")
            return {'richness_score': 0.0, 'entities': []}
    
    async def _analyze_semantic_coherence(self, content: str) -> float:
        """Analyze internal semantic coherence of content"""
        if not content:
            return 0.0
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 0.8  # Single sentence assumed coherent
        
        # Calculate semantic similarity between sentences
        coherence_scores = []
        
        if self.nlp:
            try:
                sentence_vectors = []
                for sentence in sentences:
                    doc = self.nlp(sentence)
                    if doc.vector_norm > 0:
                        sentence_vectors.append(doc.vector)
                
                if len(sentence_vectors) >= 2:
                    # Calculate pairwise similarities
                    for i in range(len(sentence_vectors) - 1):
                        similarity = np.dot(sentence_vectors[i], sentence_vectors[i + 1]) / (
                            np.linalg.norm(sentence_vectors[i]) * np.linalg.norm(sentence_vectors[i + 1])
                        )
                        coherence_scores.append(max(0, similarity))  # Ensure non-negative
                
            except Exception as e:
                self.logger.warning(f"Coherence analysis failed: {e}")
        
        # Fallback: keyword overlap analysis
        if not coherence_scores:
            for i in range(len(sentences) - 1):
                words1 = set(sentences[i].lower().split())
                words2 = set(sentences[i + 1].lower().split())
                if words1 and words2:
                    overlap = len(words1.intersection(words2)) / len(words1.union(words2))
                    coherence_scores.append(overlap)
        
        return np.mean(coherence_scores) if coherence_scores else 0.5
    
    async def _assess_innovation_potential(self, content: str) -> float:
        """Assess the innovation potential indicated in content"""
        if not content:
            return 0.0
        
        content_lower = content.lower()
        innovation_score = 0.0
        
        # Check for innovation indicators
        innovation_matches = sum(
            1 for indicator in self.business_contexts['innovation_indicators']
            if indicator in content_lower
        )
        
        # Check for novelty language
        novelty_patterns = [
            r'\b(first|new|novel|unique|revolutionary|breakthrough)\b',
            r'\b(never\s+seen|never\s+done|game\s+chang\w+)\b',
            r'\b(disrupt\w+|transform\w+|reimagin\w+)\b'
        ]
        
        pattern_matches = sum(
            1 for pattern in novelty_patterns
            if re.search(pattern, content_lower)
        )
        
        # Calculate innovation score
        if innovation_matches > 0:
            innovation_score += min(innovation_matches * 0.2, 0.6)
        
        if pattern_matches > 0:
            innovation_score += min(pattern_matches * 0.15, 0.4)
        
        return min(innovation_score, 1.0)
    
    async def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content"""
        if not content:
            return []
        
        key_concepts = []
        
        if self.nlp:
            try:
                doc = self.nlp(content)
                
                # Extract noun phrases
                noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text) > 3]
                key_concepts.extend(noun_phrases[:10])  # Top 10 noun phrases
                
                # Extract important entities
                entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'TECH']]
                key_concepts.extend(entities)
                
            except Exception as e:
                self.logger.warning(f"Key concept extraction failed: {e}")
        
        # Fallback: extract important keywords
        important_words = re.findall(r'\b(?:saas|api|platform|tool|solution|software|app|service|system)\b', content.lower())
        key_concepts.extend(important_words)
        
        # Remove duplicates and return top concepts
        return list(dict.fromkeys(key_concepts))[:15]
    
    async def _detect_context_indicators(self, content: str) -> List[str]:
        """Detect business context indicators in content"""
        if not content:
            return []
        
        content_lower = content.lower()
        indicators = []
        
        # Check each context category
        for context_type, keywords in self.business_contexts.items():
            if context_type == 'market_timing_indicators':
                for timing, timing_keywords in keywords.items():
                    if any(keyword in content_lower for keyword in timing_keywords):
                        indicators.append(f"market_timing_{timing}")
            else:
                if any(keyword in content_lower for keyword in keywords):
                    indicators.append(context_type)
        
        return indicators
    
    def _calculate_overall_semantic_score(self, semantic_score: SemanticScore) -> float:
        """Calculate weighted overall semantic score"""
        weights = {
            'context_relevance': 0.25,
            'intent_clarity': 0.20,
            'sentiment_strength': 0.15,
            'entity_richness': 0.15,
            'semantic_coherence': 0.15,
            'innovation_potential': 0.10
        }
        
        overall_score = (
            semantic_score.context_relevance * weights['context_relevance'] +
            semantic_score.intent_clarity * weights['intent_clarity'] +
            semantic_score.sentiment_strength * weights['sentiment_strength'] +
            semantic_score.entity_richness * weights['entity_richness'] +
            semantic_score.semantic_coherence * weights['semantic_coherence'] +
            semantic_score.innovation_potential * weights['innovation_potential']
        )
        
        return min(overall_score, 1.0)
    
    def _calculate_confidence_level(self, semantic_score: SemanticScore) -> float:
        """Calculate confidence level for the semantic analysis"""
        # Base confidence on completeness of analysis
        components = [
            semantic_score.context_relevance,
            semantic_score.intent_clarity,
            semantic_score.sentiment_strength,
            semantic_score.entity_richness,
            semantic_score.semantic_coherence,
            semantic_score.innovation_potential
        ]
        
        # Confidence is higher when all components are well-analyzed
        non_zero_components = sum(1 for score in components if score > 0.1)
        completeness_ratio = non_zero_components / len(components)
        
        # Factor in processing time (faster = more confident in basic analysis)
        time_factor = max(0.5, 1.0 - (semantic_score.processing_time / 10.0))
        
        return min(completeness_ratio * time_factor, 1.0)
    
    def _detect_language(self, content: str) -> str:
        """Detect the language of content"""
        try:
            from langdetect import detect
            return detect(content)
        except:
            return "en"  # Default to English
    
    def _create_fallback_score(self, content: str) -> SemanticScore:
        """Create fallback semantic score when analysis fails"""
        return SemanticScore(
            overall_score=0.3,
            context_relevance=0.3,
            intent_clarity=0.2,
            sentiment_strength=0.4,
            entity_richness=0.1,
            semantic_coherence=0.5,
            innovation_potential=0.2,
            confidence_level=0.2,
            detected_language="en",
            intent_classification="unknown"
        )
    
    def _update_analysis_stats(self, processing_time: float, semantic_score: SemanticScore):
        """Update performance statistics"""
        self.analysis_stats['signals_processed'] += 1
        
        # Update average processing time
        current_avg = self.analysis_stats['avg_processing_time']
        count = self.analysis_stats['signals_processed']
        self.analysis_stats['avg_processing_time'] = (current_avg * (count - 1) + processing_time) / count
        
        # Update semantic accuracy (based on confidence)
        current_accuracy = self.analysis_stats['semantic_accuracy']
        self.analysis_stats['semantic_accuracy'] = (current_accuracy * (count - 1) + semantic_score.confidence_level) / count
        
        # Update context detection rate
        context_detected = 1.0 if semantic_score.context_relevance > 0.3 else 0.0
        current_rate = self.analysis_stats['context_detection_rate']
        self.analysis_stats['context_detection_rate'] = (current_rate * (count - 1) + context_detected) / count
    
    async def analyze_signal_similarity(self, signals: List[str]) -> Dict:
        """Analyze semantic similarity between signals"""
        if len(signals) < 2:
            return {'similarity_matrix': [], 'clusters': []}
        
        try:
            # Create TF-IDF vectors
            vectors = self.tfidf_vectorizer.fit_transform(signals)
            
            # Calculate similarity matrix
            similarity_matrix = cosine_similarity(vectors).tolist()
            
            # Simple clustering based on similarity threshold
            clusters = self._cluster_similar_signals(similarity_matrix, threshold=0.3)
            
            return {
                'similarity_matrix': similarity_matrix,
                'clusters': clusters,
                'avg_similarity': np.mean(similarity_matrix)
            }
            
        except Exception as e:
            self.logger.error(f"Similarity analysis failed: {e}")
            return {'similarity_matrix': [], 'clusters': []}
    
    def _cluster_similar_signals(self, similarity_matrix: List[List[float]], threshold: float = 0.3) -> List[List[int]]:
        """Cluster signals based on similarity matrix"""
        n = len(similarity_matrix)
        clusters = []
        assigned = set()
        
        for i in range(n):
            if i in assigned:
                continue
            
            cluster = [i]
            assigned.add(i)
            
            for j in range(i + 1, n):
                if j not in assigned and similarity_matrix[i][j] > threshold:
                    cluster.append(j)
                    assigned.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def get_performance_stats(self) -> Dict:
        """Get current performance statistics"""
        return self.analysis_stats.copy()
    
    async def batch_analyze_signals(self, signals: List[str], context: Dict = None) -> List[SemanticScore]:
        """Analyze multiple signals in batch for efficiency"""
        self.logger.info(f"🔄 Batch analyzing {len(signals)} signals...")
        
        tasks = [
            self.analyze_semantic_understanding(signal, context)
            for signal in signals
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = [
            result for result in results
            if isinstance(result, SemanticScore)
        ]
        
        self.logger.info(f"✅ Successfully analyzed {len(valid_results)}/{len(signals)} signals")
        return valid_results

# Global semantic engine instance
_semantic_engine = None

def get_semantic_engine() -> AdvancedSemanticEngine:
    """Get or create the global semantic engine instance"""
    global _semantic_engine
    if _semantic_engine is None:
        _semantic_engine = AdvancedSemanticEngine()
    return _semantic_engine 