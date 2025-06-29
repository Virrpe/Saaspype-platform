#!/usr/bin/env python3
"""
Idea Manager - Persistent Storage and Management for User Ideas
Handles saving, retrieving, rating, and organizing user ideas
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

class IdeaManager:
    """
    Manages persistent storage and operations for user ideas
    """
    
    def __init__(self, db_path: str = "luciq_discovery.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the ideas database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create ideas table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_ideas (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT DEFAULT 'general',
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    tags TEXT, -- JSON array of tags
                    metadata TEXT, -- JSON metadata
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create idea analytics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS idea_analytics (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    idea_id TEXT NOT NULL,
                    event_type TEXT NOT NULL, -- 'created', 'rated', 'viewed', 'updated'
                    event_data TEXT, -- JSON event data
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (idea_id) REFERENCES user_ideas (id)
                )
            """)
            
            # Create user preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id TEXT PRIMARY KEY,
                    preferences TEXT, -- JSON preferences
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_ideas_user_id ON user_ideas (user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_ideas_category ON user_ideas (category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_ideas_rating ON user_ideas (rating)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_idea_analytics_user_id ON idea_analytics (user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_idea_analytics_idea_id ON idea_analytics (idea_id)")
            
            conn.commit()
            conn.close()
            
            logger.info("Ideas database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    async def save_idea(
        self,
        user_id: str,
        title: str,
        description: str = "",
        category: str = "general",
        rating: Optional[int] = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Save a new idea to the database"""
        try:
            idea_id = str(uuid.uuid4())
            tags_json = json.dumps(tags or [])
            metadata_json = json.dumps(metadata or {})
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_ideas (
                    id, user_id, title, description, category, rating, tags, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (idea_id, user_id, title, description, category, rating, tags_json, metadata_json))
            
            # Log analytics event
            await self._log_analytics_event(
                cursor, user_id, idea_id, 'created',
                {'title': title, 'category': category}
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Idea saved: {idea_id} for user {user_id}")
            return idea_id
            
        except Exception as e:
            logger.error(f"Save idea error: {e}")
            raise
    
    async def get_user_ideas(
        self,
        user_id: str,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get user's ideas with optional filtering"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT id, title, description, category, rating, tags, metadata, 
                       created_at, updated_at
                FROM user_ideas 
                WHERE user_id = ?
            """
            params = [user_id]
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            ideas = []
            for row in rows:
                idea = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'category': row[3],
                    'rating': row[4],
                    'tags': json.loads(row[5]) if row[5] else [],
                    'metadata': json.loads(row[6]) if row[6] else {},
                    'created_at': row[7],
                    'updated_at': row[8]
                }
                ideas.append(idea)
            
            conn.close()
            return ideas
            
        except Exception as e:
            logger.error(f"Get user ideas error: {e}")
            raise
    
    async def rate_idea(self, idea_id: str, user_id: str, rating: int) -> bool:
        """Rate an idea (1-5 stars)"""
        try:
            if not 1 <= rating <= 5:
                raise ValueError("Rating must be between 1 and 5")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Update the idea rating
            cursor.execute("""
                UPDATE user_ideas 
                SET rating = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND user_id = ?
            """, (rating, idea_id, user_id))
            
            if cursor.rowcount == 0:
                conn.close()
                return False
            
            # Log analytics event
            await self._log_analytics_event(
                cursor, user_id, idea_id, 'rated',
                {'rating': rating}
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Idea {idea_id} rated {rating} stars by user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Rate idea error: {e}")
            raise
    
    async def get_idea_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get analytics data for user's ideas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get basic stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_ideas,
                    COUNT(CASE WHEN rating IS NOT NULL THEN 1 END) as rated_ideas,
                    AVG(CASE WHEN rating IS NOT NULL THEN rating END) as avg_rating,
                    COUNT(DISTINCT category) as categories_count
                FROM user_ideas 
                WHERE user_id = ?
            """, (user_id,))
            
            stats = cursor.fetchone()
            
            # Get category distribution
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM user_ideas 
                WHERE user_id = ?
                GROUP BY category
                ORDER BY count DESC
            """, (user_id,))
            
            categories = [{'name': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # Get rating distribution
            cursor.execute("""
                SELECT rating, COUNT(*) as count
                FROM user_ideas 
                WHERE user_id = ? AND rating IS NOT NULL
                GROUP BY rating
                ORDER BY rating DESC
            """, (user_id,))
            
            ratings = [{'rating': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # Get recent activity
            cursor.execute("""
                SELECT event_type, COUNT(*) as count
                FROM idea_analytics 
                WHERE user_id = ? AND timestamp >= datetime('now', '-7 days')
                GROUP BY event_type
            """, (user_id,))
            
            recent_activity = [{'event': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            conn.close()
            
            return {
                'total_ideas': stats[0] or 0,
                'rated_ideas': stats[1] or 0,
                'avg_rating': round(stats[2] or 0, 1),
                'categories_count': stats[3] or 0,
                'category_distribution': categories,
                'rating_distribution': ratings,
                'recent_activity': recent_activity
            }
            
        except Exception as e:
            logger.error(f"Get idea analytics error: {e}")
            raise
    
    async def export_user_data(self, user_id: str, format: str = "json") -> Dict[str, Any]:
        """Export user's ideas and data"""
        try:
            # Get all user ideas
            ideas = await self.get_user_ideas(user_id, limit=1000)
            
            # Get analytics
            analytics = await self.get_idea_analytics(user_id)
            
            export_data = {
                'user_id': user_id,
                'export_timestamp': datetime.now().isoformat(),
                'total_ideas': len(ideas),
                'ideas': ideas,
                'analytics': analytics
            }
            
            if format == "csv":
                # Convert to CSV format
                import csv
                import io
                
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=[
                    'id', 'title', 'description', 'category', 'rating', 'created_at'
                ])
                writer.writeheader()
                
                for idea in ideas:
                    writer.writerow({
                        'id': idea['id'],
                        'title': idea['title'],
                        'description': idea['description'],
                        'category': idea['category'],
                        'rating': idea['rating'],
                        'created_at': idea['created_at']
                    })
                
                export_data['csv_data'] = output.getvalue()
                output.close()
            
            return export_data
            
        except Exception as e:
            logger.error(f"Export user data error: {e}")
            raise
    
    async def search_ideas(
        self,
        user_id: str,
        query: str,
        category: Optional[str] = None,
        min_rating: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search user's ideas by text query"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            sql_query = """
                SELECT id, title, description, category, rating, tags, metadata, 
                       created_at, updated_at
                FROM user_ideas 
                WHERE user_id = ? AND (
                    title LIKE ? OR description LIKE ?
                )
            """
            params = [user_id, f"%{query}%", f"%{query}%"]
            
            if category:
                sql_query += " AND category = ?"
                params.append(category)
            
            if min_rating:
                sql_query += " AND rating >= ?"
                params.append(min_rating)
            
            sql_query += " ORDER BY created_at DESC"
            
            cursor.execute(sql_query, params)
            rows = cursor.fetchall()
            
            ideas = []
            for row in rows:
                idea = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'category': row[3],
                    'rating': row[4],
                    'tags': json.loads(row[5]) if row[5] else [],
                    'metadata': json.loads(row[6]) if row[6] else {},
                    'created_at': row[7],
                    'updated_at': row[8]
                }
                ideas.append(idea)
            
            conn.close()
            return ideas
            
        except Exception as e:
            logger.error(f"Search ideas error: {e}")
            raise
    
    async def _log_analytics_event(
        self,
        cursor,
        user_id: str,
        idea_id: str,
        event_type: str,
        event_data: Dict[str, Any]
    ):
        """Log an analytics event"""
        try:
            event_id = str(uuid.uuid4())
            event_data_json = json.dumps(event_data)
            
            cursor.execute("""
                INSERT INTO idea_analytics (
                    id, user_id, idea_id, event_type, event_data
                ) VALUES (?, ?, ?, ?, ?)
            """, (event_id, user_id, idea_id, event_type, event_data_json))
            
        except Exception as e:
            logger.error(f"Log analytics event error: {e}")
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT preferences FROM user_preferences WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return json.loads(row[0])
            else:
                # Return default preferences
                return {
                    'default_category': 'general',
                    'auto_save': True,
                    'notification_preferences': {
                        'idea_reminders': True,
                        'trend_alerts': True
                    }
                }
                
        except Exception as e:
            logger.error(f"Get user preferences error: {e}")
            return {}
    
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences"""
        try:
            preferences_json = json.dumps(preferences)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO user_preferences (
                    user_id, preferences, updated_at
                ) VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (user_id, preferences_json))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Update user preferences error: {e}")
            return False 