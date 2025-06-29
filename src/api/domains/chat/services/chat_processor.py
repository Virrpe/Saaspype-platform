#!/usr/bin/env python3
"""
Chat Processor - NLP Engine for Intelligent Chat Responses
Handles intent recognition, context management, and response generation
"""

import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

from src.services.orchestration.intelligence_orchestrator import get_intelligence_orchestrator, OrchestrationRequest

logger = logging.getLogger(__name__)

class ChatProcessor:
    """
    Advanced NLP chat processor for intelligent conversation handling
    """
    
    def __init__(self):
        self.sessions = {}  # In-memory session storage
        self.intent_patterns = self._initialize_intent_patterns()
        self.response_templates = self._initialize_response_templates()
        
    def _initialize_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize intent recognition patterns"""
        return {
            'save_idea': [
                r'save.*idea.*about\s+(.+)',
                r'remember.*idea.*(.+)',
                r'store.*concept.*(.+)',
                r'add.*idea.*(.+)',
                r'new.*idea.*(.+)',
                r'i.*have.*idea.*about\s+(.+)',
                r'my.*idea.*is\s+(.+)',
                r'save\s+(.+)',
                r'remember\s+(.+)'
            ],
            'generate_ideas': [
                r'generate.*ideas?.*about\s+(.+)',
                r'create.*ideas?.*for\s+(.+)',
                r'brainstorm.*(.+)',
                r'give.*me.*ideas?.*about\s+(.+)',
                r'suggest.*ideas?.*for\s+(.+)',
                r'ideas?.*for\s+(.+)',
                r'what.*ideas?.*(.+)',
                r'business.*ideas?.*(.+)'
            ],
            'rate_ideas': [
                r'rate.*ideas?',
                r'rating.*ideas?',
                r'score.*ideas?',
                r'rank.*ideas?',
                r'evaluate.*ideas?',
                r'how.*good.*ideas?',
                r'rate.*my.*ideas?'
            ],
            'list_ideas': [
                r'show.*ideas?',
                r'list.*ideas?',
                r'my.*ideas?',
                r'all.*ideas?',
                r'what.*ideas?.*have',
                r'display.*ideas?',
                r'see.*ideas?'
            ],
            'analyze_trends': [
                r'analyze.*trends?',
                r'trend.*analysis',
                r'patterns?.*in.*ideas?',
                r'insights?.*from.*ideas?',
                r'what.*trends?',
                r'analyze.*my.*ideas?',
                r'insights?.*about.*ideas?'
            ],
            'generate_charts': [
                r'generate.*chart',
                r'create.*graph',
                r'show.*visualization',
                r'chart.*of.*ideas?',
                r'graph.*my.*data',
                r'visualize.*ideas?',
                r'plot.*data'
            ],
            'export_data': [
                r'export.*data',
                r'download.*ideas?',
                r'save.*data',
                r'backup.*ideas?',
                r'export.*ideas?'
            ],
            'run_pipeline': [
                r'run.*pipeline',
                r'execute.*pipeline',
                r'start.*analysis',
                r'discover.*ideas?',
                r'find.*opportunities',
                r'analyze.*market'
            ],
            'help': [
                r'help',
                r'what.*can.*do',
                r'how.*work',
                r'commands?',
                r'features?'
            ],
            'greeting': [
                r'hello',
                r'hi',
                r'hey',
                r'good.*morning',
                r'good.*afternoon',
                r'good.*evening'
            ]
        }
    
    def _initialize_response_templates(self) -> Dict[str, List[str]]:
        """Initialize response templates for different intents"""
        return {
            'save_idea': [
                "Great idea! I've saved '{topic}' to your collection. Would you like me to generate related ideas or analyze it further?",
                "Perfect! '{topic}' has been added to your ideas. I can help you develop this concept or find similar opportunities.",
                "Excellent concept! I've stored '{topic}' and can help you explore market potential or create variations."
            ],
            'generate_ideas': [
                "I'm generating business ideas about '{topic}' using our 6-engine intelligence system. This will take a moment...",
                "Analyzing '{topic}' across multiple intelligence engines to create innovative business concepts...",
                "Running deep market analysis for '{topic}' to generate high-potential business ideas..."
            ],
            'rate_ideas': [
                "I'll help you rate your ideas! Here are your saved concepts with rating options:",
                "Let's evaluate your idea collection. I'll show each idea with interactive rating controls:",
                "Time to prioritize! Here are your ideas ready for rating and ranking:"
            ],
            'list_ideas': [
                "Here are your saved ideas organized by category and rating:",
                "Your idea collection is looking great! Here's everything you've saved:",
                "Let me show you all your brilliant concepts:"
            ],
            'analyze_trends': [
                "Analyzing patterns in your idea collection... I'll identify trends, categories, and insights:",
                "Running trend analysis on your ideas to find patterns and opportunities:",
                "Generating insights from your idea data - looking for themes and potential:"
            ],
            'generate_charts': [
                "Creating visual analysis of your ideas... I'll generate charts showing categories, ratings, and trends:",
                "Building interactive visualizations of your idea data:",
                "Generating comprehensive charts and graphs from your idea collection:"
            ],
            'export_data': [
                "Preparing your idea data for export... I can create JSON, CSV, or PDF formats:",
                "Generating export package with all your ideas, ratings, and analysis:",
                "Creating downloadable backup of your complete idea collection:"
            ],
            'run_pipeline': [
                "Launching the full Luciq discovery pipeline... This will analyze Reddit, generate insights, and find new opportunities:",
                "Starting comprehensive market analysis using our 6-engine orchestration system:",
                "Executing real-time discovery pipeline to find fresh business opportunities:"
            ],
            'help': [
                "I'm ARIA, your AI assistant for idea management and business intelligence! I can help you save ideas, generate new concepts, create visualizations, and analyze trends. Try asking me to 'save an idea about AI tools' or 'generate ideas for productivity apps'.",
                "Here's what I can do: 💡 Save and organize ideas, 🚀 Generate new business concepts, 📊 Create charts and visualizations, 📈 Analyze trends and patterns, 💾 Export your data, 🔍 Run market discovery pipelines. What would you like to explore?",
                "I'm your intelligent idea companion! Ask me to save ideas, generate new concepts, create visualizations, or analyze your collection. I can also run the full Luciq pipeline to discover market opportunities."
            ],
            'greeting': [
                "Hello! I'm ARIA, your AI assistant for idea generation and analysis. What brilliant concept shall we explore today?",
                "Hi there! Ready to dive into some innovative thinking? I can help you save ideas, generate new concepts, or analyze your collection.",
                "Hey! Great to see you. I'm here to help with idea management, business intelligence, and creative brainstorming. What's on your mind?"
            ],
            'general': [
                "That's interesting! Could you tell me more about what you'd like to do? I can help with idea generation, analysis, or visualization.",
                "I'm here to help with your ideas and business intelligence needs. Would you like to save an idea, generate new concepts, or analyze your collection?",
                "I can assist with idea management, trend analysis, and business intelligence. What would you like to explore together?"
            ]
        }
    
    async def process_message(
        self, 
        message: str, 
        user_id: str, 
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message and return intelligent response
        """
        try:
            # Create or get session
            if not session_id:
                session_id = str(uuid.uuid4())
            
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'user_id': user_id,
                    'created_at': datetime.now(),
                    'messages': [],
                    'context': {}
                }
            
            session = self.sessions[session_id]
            
            # Add message to session history
            session['messages'].append({
                'type': 'user',
                'content': message,
                'timestamp': datetime.now()
            })
            
            # Analyze intent
            intent, extracted_data = self._analyze_intent(message)
            
            # Generate response based on intent
            response_data = await self._generate_response(
                intent=intent,
                message=message,
                extracted_data=extracted_data,
                user_id=user_id,
                session=session,
                context=context
            )
            
            # Add AI response to session
            session['messages'].append({
                'type': 'ai',
                'content': response_data['response'],
                'timestamp': datetime.now(),
                'intent': intent,
                'actions': response_data.get('actions', [])
            })
            
            return {
                'response': response_data['response'],
                'intent': intent,
                'actions': response_data.get('actions', []),
                'data': response_data.get('data'),
                'session_id': session_id
            }
            
        except Exception as e:
            logger.error(f"Chat processing error: {e}")
            return {
                'response': "I encountered an error processing your message. Please try again.",
                'intent': 'error',
                'actions': [],
                'data': None,
                'session_id': session_id or str(uuid.uuid4())
            }
    
    def _analyze_intent(self, message: str) -> tuple[str, Dict[str, Any]]:
        """Analyze message intent using pattern matching"""
        message_lower = message.lower().strip()
        extracted_data = {}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message_lower)
                if match:
                    if match.groups():
                        extracted_data['topic'] = match.group(1).strip()
                    return intent, extracted_data
        
        return 'general', extracted_data
    
    async def _generate_response(
        self,
        intent: str,
        message: str,
        extracted_data: Dict[str, Any],
        user_id: str,
        session: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate intelligent response based on intent"""
        
        actions = []
        data = None
        
        if intent == 'save_idea':
            response = await self._handle_save_idea(extracted_data, user_id, actions)
            
        elif intent == 'generate_ideas':
            response = await self._handle_generate_ideas(extracted_data, user_id, actions)
            
        elif intent == 'rate_ideas':
            response, data = await self._handle_rate_ideas(user_id, actions)
            
        elif intent == 'list_ideas':
            response, data = await self._handle_list_ideas(user_id, actions)
            
        elif intent == 'analyze_trends':
            response, data = await self._handle_analyze_trends(user_id, actions)
            
        elif intent == 'generate_charts':
            response, data = await self._handle_generate_charts(user_id, actions)
            
        elif intent == 'export_data':
            response = await self._handle_export_data(user_id, actions)
            
        elif intent == 'run_pipeline':
            response = await self._handle_run_pipeline(extracted_data, user_id, actions)
            
        elif intent == 'help':
            response = self._get_random_template('help')
            
        elif intent == 'greeting':
            response = self._get_random_template('greeting')
            
        else:
            response = self._get_random_template('general')
        
        return {
            'response': response,
            'actions': actions,
            'data': data
        }
    
    async def _handle_save_idea(self, extracted_data: Dict[str, Any], user_id: str, actions: List) -> str:
        """Handle save idea intent"""
        topic = extracted_data.get('topic', 'New Idea')
        
        # Add action to save the idea
        actions.append({
            'type': 'save_idea',
            'data': {
                'title': topic,
                'description': f"Idea about {topic}",
                'category': 'chat_generated'
            }
        })
        
        template = self._get_random_template('save_idea')
        return template.format(topic=topic)
    
    async def _handle_generate_ideas(self, extracted_data: Dict[str, Any], user_id: str, actions: List) -> str:
        """Handle generate ideas intent - Actually execute idea generation"""
        topic = extracted_data.get('topic', 'business opportunities')
        
        try:
            # Get orchestrator instance
            orchestrator = get_intelligence_orchestrator()
            
            # Create orchestration request for idea generation
            orchestration_request = OrchestrationRequest(
                request_type="business_idea_generation",
                data={
                    "content": f"Generate business ideas for {topic}",
                    "focus": "saas_solutions",
                    "target_market": "SMB and Enterprise",
                    "analysis_depth": "comprehensive"
                },
                session_id=f"chat_{user_id}_{int(datetime.now().timestamp())}",
                priority="high",
                timeout_seconds=45
            )
            
            # Execute the orchestration
            logger.info(f"🚀 Generating ideas for topic: {topic}")
            result = await orchestrator.analyze_intelligence(orchestration_request)
            
            if result.success:
                # Extract business ideas from the result
                business_ideas = []
                if "business_ideas" in result.results:
                    business_ideas = result.results["business_ideas"]
                elif hasattr(result, 'business_ideas'):
                    business_ideas = result.business_ideas
                else:
                    # Try to extract from orchestration API format
                    from src.services.orchestration.orchestration_api import _extract_business_ideas_from_result
                    business_ideas = await _extract_business_ideas_from_result(result)
                
                logger.info(f"✅ Generated {len(business_ideas)} ideas for {topic}")
                
                # Add actions for each generated idea
                for idea in business_ideas[:3]:  # Limit to 3 ideas for chat interface
                    actions.append({
                        'type': 'save_idea',
                        'data': {
                            'title': idea.get('idea_title', 'Generated Business Idea'),
                            'description': idea.get('solution_approach', 'AI-generated business idea'),
                            'category': 'ai_generated',
                            'confidence_score': idea.get('confidence_score', 0.8),
                            'revenue_potential': idea.get('revenue_potential', 'Medium'),
                            'problem_statement': idea.get('problem_statement', ''),
                            'target_market': idea.get('target_market', ''),
                            'business_model': idea.get('business_model', '')
                        }
                    })
                
                # Add generate ideas action for UI feedback
                actions.append({
                    'type': 'generate_ideas',
                    'data': {
                        'topic': topic,
                        'count': len(business_ideas),
                        'processing_time_ms': result.processing_time_ms,
                        'engines_used': result.engines_used,
                        'success': True
                    }
                })
                
                return f"✅ Generated {len(business_ideas)} business ideas for '{topic}'! Processing time: {result.processing_time_ms:.0f}ms. The top {min(3, len(business_ideas))} ideas have been automatically saved to your collection."
                
            else:
                logger.error(f"❌ Idea generation failed for topic: {topic}")
                actions.append({
                    'type': 'generate_ideas',
                    'data': {
                        'topic': topic,
                        'success': False,
                        'error': 'Idea generation failed'
                    }
                })
                return f"❌ Failed to generate ideas for '{topic}'. Please try again or try a different topic."
                
        except Exception as e:
            logger.error(f"❌ Idea generation error: {e}")
            actions.append({
                'type': 'generate_ideas',
                'data': {
                    'topic': topic,
                    'success': False,
                    'error': str(e)
                }
            })
            return f"❌ Idea generation encountered an error: {str(e)}. Please try again."
    
    async def _handle_rate_ideas(self, user_id: str, actions: List) -> tuple[str, Dict]:
        """Handle rate ideas intent"""
        # Add action to show rating interface
        actions.append({
            'type': 'show_rating_interface',
            'data': {}
        })
        
        # Mock user ideas for now (will be replaced with real data)
        ideas_data = {
            'ideas': [
                {'id': '1', 'title': 'AI-powered productivity app', 'rating': None},
                {'id': '2', 'title': 'Smart home automation', 'rating': 4},
                {'id': '3', 'title': 'Blockchain marketplace', 'rating': None}
            ]
        }
        
        template = self._get_random_template('rate_ideas')
        return template, ideas_data
    
    async def _handle_list_ideas(self, user_id: str, actions: List) -> tuple[str, Dict]:
        """Handle list ideas intent"""
        actions.append({
            'type': 'show_ideas_list',
            'data': {}
        })
        
        # Mock ideas data
        ideas_data = {
            'ideas': [
                {
                    'id': '1',
                    'title': 'AI-powered productivity app',
                    'category': 'productivity',
                    'rating': 5,
                    'created_at': '2024-01-15'
                },
                {
                    'id': '2',
                    'title': 'Smart home automation',
                    'category': 'iot',
                    'rating': 4,
                    'created_at': '2024-01-14'
                }
            ],
            'total': 2,
            'categories': ['productivity', 'iot']
        }
        
        template = self._get_random_template('list_ideas')
        return template, ideas_data
    
    async def _handle_analyze_trends(self, user_id: str, actions: List) -> tuple[str, Dict]:
        """Handle analyze trends intent"""
        actions.append({
            'type': 'show_trend_analysis',
            'data': {}
        })
        
        # Mock trend data
        trend_data = {
            'top_categories': [
                {'name': 'AI/ML', 'count': 5},
                {'name': 'Productivity', 'count': 3},
                {'name': 'IoT', 'count': 2}
            ],
            'rating_distribution': [
                {'rating': 5, 'count': 3},
                {'rating': 4, 'count': 2},
                {'rating': 3, 'count': 1}
            ],
            'insights': [
                'You have a strong focus on AI/ML solutions',
                'Most of your ideas are highly rated (4+ stars)',
                'Consider exploring more diverse categories'
            ]
        }
        
        template = self._get_random_template('analyze_trends')
        return template, trend_data
    
    async def _handle_generate_charts(self, user_id: str, actions: List) -> tuple[str, Dict]:
        """Handle generate charts intent"""
        actions.append({
            'type': 'show_charts',
            'data': {
                'chart_types': ['category_distribution', 'rating_trends', 'idea_timeline']
            }
        })
        
        # Mock chart data
        chart_data = {
            'category_chart': {
                'type': 'pie',
                'data': [
                    {'label': 'AI/ML', 'value': 50},
                    {'label': 'Productivity', 'value': 30},
                    {'label': 'IoT', 'value': 20}
                ]
            },
            'rating_chart': {
                'type': 'bar',
                'data': [
                    {'label': '5 stars', 'value': 3},
                    {'label': '4 stars', 'value': 2},
                    {'label': '3 stars', 'value': 1}
                ]
            }
        }
        
        template = self._get_random_template('generate_charts')
        return template, chart_data
    
    async def _handle_export_data(self, user_id: str, actions: List) -> str:
        """Handle export data intent"""
        actions.append({
            'type': 'export_data',
            'data': {
                'formats': ['json', 'csv', 'pdf']
            }
        })
        
        template = self._get_random_template('export_data')
        return template
    
    async def _handle_run_pipeline(self, extracted_data: Dict[str, Any], user_id: str, actions: List) -> str:
        """Handle run pipeline intent - Actually execute the orchestration system"""
        topic = extracted_data.get('topic', 'business opportunities')
        
        try:
            # Get orchestrator instance
            orchestrator = get_intelligence_orchestrator()
            
            # Create orchestration request for idea generation
            orchestration_request = OrchestrationRequest(
                request_type="business_idea_generation",
                data={
                    "content": f"Generate business ideas for {topic}",
                    "focus": "saas_solutions",
                    "target_market": "SMB and Enterprise",
                    "analysis_depth": "comprehensive"
                },
                session_id=f"chat_{user_id}_{int(datetime.now().timestamp())}",
                priority="high",
                timeout_seconds=60
            )
            
            # Execute the orchestration
            logger.info(f"🚀 Executing pipeline for topic: {topic}")
            result = await orchestrator.analyze_intelligence(orchestration_request)
            
            if result.success:
                # Extract business ideas from the result
                business_ideas = []
                if "business_ideas" in result.results:
                    business_ideas = result.results["business_ideas"]
                elif hasattr(result, 'business_ideas'):
                    business_ideas = result.business_ideas
                else:
                    # Try to extract from orchestration API format
                    from src.services.orchestration.orchestration_api import _extract_business_ideas_from_result
                    business_ideas = await _extract_business_ideas_from_result(result)
                
                logger.info(f"✅ Pipeline generated {len(business_ideas)} ideas")
                
                # Add actions for each generated idea
                for idea in business_ideas[:5]:  # Limit to 5 ideas for chat interface
                    actions.append({
                        'type': 'save_idea',
                        'data': {
                            'title': idea.get('idea_title', 'Generated Business Idea'),
                            'description': idea.get('solution_approach', 'AI-generated business idea'),
                            'category': 'pipeline_generated',
                            'confidence_score': idea.get('confidence_score', 0.8),
                            'revenue_potential': idea.get('revenue_potential', 'Medium'),
                            'problem_statement': idea.get('problem_statement', ''),
                            'target_market': idea.get('target_market', ''),
                            'business_model': idea.get('business_model', '')
                        }
                    })
                
                # Add pipeline execution action for UI feedback
                actions.append({
                    'type': 'run_pipeline',
                    'data': {
                        'pipeline_type': 'full_discovery',
                        'topic': topic,
                        'ideas_generated': len(business_ideas),
                        'processing_time_ms': result.processing_time_ms,
                        'engines_used': result.engines_used,
                        'success': True
                    }
                })
                
                return f"✅ Pipeline execution complete! Generated {len(business_ideas)} business ideas for '{topic}'. Processing time: {result.processing_time_ms:.0f}ms using {len(result.engines_used)} intelligence engines. Ideas have been automatically saved to your collection."
                
            else:
                logger.error(f"❌ Pipeline execution failed")
                actions.append({
                    'type': 'run_pipeline',
                    'data': {
                        'pipeline_type': 'full_discovery',
                        'topic': topic,
                        'success': False,
                        'error': 'Pipeline execution failed'
                    }
                })
                return f"❌ Pipeline execution failed for topic '{topic}'. Please try again or contact support."
                
        except Exception as e:
            logger.error(f"❌ Pipeline execution error: {e}")
            actions.append({
                'type': 'run_pipeline',
                'data': {
                    'pipeline_type': 'full_discovery',
                    'topic': topic,
                    'success': False,
                    'error': str(e)
                }
            })
            return f"❌ Pipeline execution encountered an error: {str(e)}. Please try again."
    
    def _get_random_template(self, intent: str) -> str:
        """Get a random response template for the given intent"""
        import random
        templates = self.response_templates.get(intent, self.response_templates['general'])
        return random.choice(templates) 