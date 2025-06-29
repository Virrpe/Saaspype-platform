#!/usr/bin/env python3
"""
Ideas Service - Handle all idea-related operations
"""

import logging
from typing import List, Dict, Any, Optional
from src.shared.database.connection import db_service

logger = logging.getLogger(__name__)

class IdeasService:
    """Service for managing user ideas and system-generated ideas"""
    
    def save_idea(self, user_id: int, idea_title: str, idea_description: str, 
                  pain_point_source: str, market_potential: str, 
                  concept_data: Optional[Dict] = None) -> Dict[str, str]:
        """Save a user's discovered idea"""
        try:
            conn = db_service.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO saved_ideas (user_id, idea_title, idea_description, pain_point_source, market_potential, concept_data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                idea_title,
                idea_description,
                pain_point_source,
                market_potential,
                str(concept_data) if concept_data else None
            ))
            conn.commit()
            conn.close()
            
            logger.info(f"Idea saved for user {user_id}: {idea_title}")
            return {"message": "Idea saved successfully"}
            
        except Exception as e:
            logger.error(f"Error saving idea: {e}")
            raise Exception("Database error while saving idea")
    
    def get_user_ideas(self, user_id: int) -> Dict[str, List[Dict]]:
        """Get all ideas saved by a specific user"""
        try:
            conn = db_service.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, idea_title, idea_description, pain_point_source, market_potential, saved_at
                FROM saved_ideas
                WHERE user_id = ?
                ORDER BY saved_at DESC
            """, (user_id,))
            ideas = cursor.fetchall()
            conn.close()
            
            return {
                "ideas": [
                    {
                        "id": idea[0],
                        "title": idea[1],
                        "description": idea[2],
                        "source": idea[3],
                        "market_potential": idea[4],
                        "saved_at": idea[5]
                    }
                    for idea in ideas
                ]
            }
        except Exception as e:
            logger.error(f"Error fetching user ideas: {e}")
            raise Exception("Database error while fetching user ideas")
    
    def get_system_ideas(self, limit: int = 10) -> Dict[str, List[Dict]]:
        """Get system-generated ideas"""
        try:
            conn = db_service.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT idea_title, idea_description, pain_point_source, market_potential 
                FROM saved_ideas 
                WHERE system_generated = 1 
                ORDER BY saved_at DESC 
                LIMIT ?
            """, (limit,))
            ideas = cursor.fetchall()
            conn.close()
            
            return {
                "system_ideas": [
                    {
                        "idea_title": idea[0],
                        "idea_description": idea[1],
                        "pain_point_source": idea[2],
                        "market_potential": idea[3],
                        "enhanced_score": 7.5,  # Default score for display
                        "confidence_score": 0.8,  # Default confidence
                        "concept_data": {
                            "domain": "business",
                            "score": 7.5,
                            "reddit_data": {
                                "subreddit": "entrepreneur",
                                "score": 100
                            }
                        }
                    }
                    for idea in ideas
                ]
            }
        except Exception as e:
            logger.error(f"Error fetching system ideas: {e}")
            raise Exception("Database error while fetching system ideas")
    
    def get_discovery_history(self, limit: int = 20) -> Dict[str, List[Dict]]:
        """Get discovery session history"""
        try:
            conn = db_service.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT subreddit, posts_analyzed, pain_points_found, created_at
                FROM discovery_sessions
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            sessions = cursor.fetchall()
            conn.close()
            
            return {
                "sessions": [
                    {
                        "subreddit": session[0],
                        "posts_analyzed": session[1],
                        "pain_points_found": session[2],
                        "created_at": session[3]
                    }
                    for session in sessions
                ]
            }
        except Exception as e:
            logger.error(f"Error fetching discovery history: {e}")
            raise Exception("Database error while fetching discovery history")

# Create service instance
ideas_service = IdeasService() 