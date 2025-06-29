#!/usr/bin/env python3
"""
Database Service
Centralized database management for Luciq
"""

from src.shared.database.connection import db_service as shared_db_service
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    """API-layer database service that wraps the shared database service"""
    
    def __init__(self):
        self.db = shared_db_service
    
    def get_connection(self):
        """Get database connection"""
        return self.db.get_connection()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a query and return results as list of dictionaries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description] if cursor.description else []
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
        finally:
            conn.close()
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute an insert query and return the last row ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update/delete query and return affected rows"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        results = self.execute_query("SELECT id, email FROM users WHERE email = ?", (email,))
        return results[0] if results else None
    
    def get_user_ideas(self, user_id: int) -> List[Dict]:
        """Get all ideas for a user"""
        return self.execute_query(
            "SELECT * FROM saved_ideas WHERE user_id = ? ORDER BY saved_at DESC",
            (user_id,)
        )
    
    def get_discovery_sessions(self, user_id: Optional[int] = None) -> List[Dict]:
        """Get discovery sessions, optionally filtered by user"""
        if user_id:
            return self.execute_query(
                "SELECT * FROM discovery_sessions WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
        else:
            return self.execute_query(
                "SELECT * FROM discovery_sessions ORDER BY created_at DESC"
            )
    
    def health_check(self) -> bool:
        """Check database health"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

# Global database service instance
database_service = DatabaseService() 