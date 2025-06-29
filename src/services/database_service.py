"""
Luciq Database Service
Extracted from master_luciq_api.py - Phase 2 Core Architecture Refactoring

Handles all database operations with SQLite backend
"""

import sqlite3
import aiosqlite
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class MasterDatabaseService:
    """
    Master database service for Luciq platform
    Handles user management, session tracking, and data persistence
    """
    
    def __init__(self, db_path: str = "luciq_master.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with all required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Discovery sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS discovery_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    user_id INTEGER,
                    subreddit TEXT NOT NULL,
                    posts_analyzed INTEGER DEFAULT 0,
                    pain_points_found INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Pain points table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pain_points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    post_id TEXT,
                    title TEXT,
                    description TEXT,
                    domain TEXT,
                    market_size_score INTEGER,
                    urgency_score INTEGER,
                    solution_gap_score INTEGER,
                    monetization_score INTEGER,
                    total_score INTEGER,
                    confidence_score REAL,
                    target_market TEXT,
                    opportunity_description TEXT,
                    validation_signals TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES discovery_sessions (session_id)
                )
            ''')
            
            # Intelligence sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS intelligence_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    user_id INTEGER,
                    analysis_type TEXT,
                    content_analyzed TEXT,
                    platforms TEXT,
                    results TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Streaming sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS streaming_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    user_id INTEGER,
                    platforms TEXT,
                    keywords TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Chat sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    user_id INTEGER,
                    message_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Chat messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_id INTEGER,
                    message TEXT NOT NULL,
                    response TEXT,
                    intent_detected TEXT,
                    analysis_results TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def create_user(self, username: str, email: str, password_hash: str) -> Optional[int]:
        """Create a new user"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash)
                )
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM users WHERE username = ? AND is_active = 1",
                    (username,)
                )
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None
    
    async def save_discovery_session(self, session_id: str, user_id: int, subreddit: str, posts_analyzed: int, pain_points_found: int):
        """Save discovery session"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO discovery_sessions (session_id, user_id, subreddit, posts_analyzed, pain_points_found) VALUES (?, ?, ?, ?, ?)",
                    (session_id, user_id, subreddit, posts_analyzed, pain_points_found)
                )
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to save discovery session: {e}")
    
    async def save_pain_point(self, session_id: str, pain_point: Dict):
        """Save pain point data"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT INTO pain_points (
                        session_id, post_id, title, description, domain,
                        market_size_score, urgency_score, solution_gap_score, monetization_score,
                        total_score, confidence_score, target_market, opportunity_description,
                        validation_signals
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    pain_point.get('post_id'),
                    pain_point.get('title'),
                    pain_point.get('description'),
                    pain_point.get('domain'),
                    pain_point.get('market_size_score'),
                    pain_point.get('urgency_score'),
                    pain_point.get('solution_gap_score'),
                    pain_point.get('monetization_score'),
                    pain_point.get('total_score'),
                    pain_point.get('confidence_score'),
                    pain_point.get('target_market'),
                    pain_point.get('opportunity_description'),
                    str(pain_point.get('validation_signals', []))
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to save pain point: {e}")
    
    async def save_chat_message(self, session_id: str, user_id: int, message: str, response: str, intent: str = None, analysis: str = None):
        """Save chat message and response"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT INTO chat_messages (session_id, user_id, message, response, intent_detected, analysis_results)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (session_id, user_id, message, response, intent, analysis))
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to save chat message: {e}")
    
    async def get_user_chat_history(self, user_id: int, limit: int = 10) -> list:
        """Get user's recent chat history"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute('''
                    SELECT message, response, intent_detected, created_at
                    FROM chat_messages
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (user_id, limit))
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get chat history: {e}")
            return [] 