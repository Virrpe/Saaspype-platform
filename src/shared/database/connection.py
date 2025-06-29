#!/usr/bin/env python3
"""
Database Connection - Centralized database connection management
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional
from src.shared.config.settings import DATABASE_PATH

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DATABASE_PATH
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize the database with discovery-focused tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if users table exists and needs migration
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            # Check current schema
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # If missing critical columns, recreate table
            if 'user_id' not in columns or 'username' not in columns:
                logger.info("Recreating users table with proper schema")
                
                # Backup existing data
                cursor.execute("SELECT * FROM users")
                existing_users = cursor.fetchall()
                
                # Drop and recreate table
                cursor.execute("DROP TABLE users")
                
                # Create new table with proper schema
                cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        username TEXT UNIQUE,
                        password_hash TEXT NOT NULL,
                        is_active INTEGER DEFAULT 1,
                        is_verified INTEGER DEFAULT 0,
                        first_name TEXT,
                        last_name TEXT,
                        display_name TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        login_count INTEGER DEFAULT 0,
                        verification_token TEXT,
                        verification_sent_at TIMESTAMP,
                        password_reset_token TEXT,
                        password_reset_sent_at TIMESTAMP,
                        preferences TEXT
                    )
                """)
                
                # Restore data with new schema
                import secrets
                for user_row in existing_users:
                    # Generate user_id if not exists
                    user_id = f"user_{secrets.token_hex(8)}"
                    
                    # Map old data to new schema
                    cursor.execute("""
                        INSERT INTO users (
                            user_id, email, password_hash, is_active, is_verified,
                            created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        user_id,
                        user_row[1] if len(user_row) > 1 else 'unknown@example.com',  # email
                        user_row[2] if len(user_row) > 2 else 'temp_hash',  # password_hash
                        1,  # is_active
                        0,  # is_verified
                        user_row[3] if len(user_row) > 3 else 'CURRENT_TIMESTAMP',  # created_at
                        'CURRENT_TIMESTAMP'  # updated_at
                    ))
                
                conn.commit()
                logger.info("Successfully recreated users table with proper schema")
        else:
            # Create fresh table
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    username TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    is_verified INTEGER DEFAULT 0,
                    first_name TEXT,
                    last_name TEXT,
                    display_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    login_count INTEGER DEFAULT 0,
                    verification_token TEXT,
                    verification_sent_at TIMESTAMP,
                    password_reset_token TEXT,
                    password_reset_sent_at TIMESTAMP,
                    preferences TEXT
                )
            """)
            logger.info("Created fresh users table")
        
        # Saved ideas table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                idea_title TEXT NOT NULL,
                idea_description TEXT,
                pain_point_source TEXT,
                market_potential TEXT,
                concept_data TEXT,
                system_generated INTEGER DEFAULT 0,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Discovery sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discovery_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subreddit TEXT NOT NULL,
                posts_analyzed INTEGER DEFAULT 0,
                pain_points_found INTEGER DEFAULT 0,
                session_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        
        # Migration: Add missing columns to existing users table
        try:
            # Check if user_id column exists
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'user_id' not in columns:
                logger.info("Adding user_id column to existing users table")
                cursor.execute('ALTER TABLE users ADD COLUMN user_id TEXT')
                
                # Generate user_ids for existing users
                cursor.execute('SELECT id, email FROM users WHERE user_id IS NULL')
                existing_users = cursor.fetchall()
                
                for user_id, email in existing_users:
                    import secrets
                    new_user_id = f"user_{secrets.token_hex(8)}"
                    cursor.execute('UPDATE users SET user_id = ? WHERE id = ?', (new_user_id, user_id))
                
                # Make user_id unique after populating
                cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)')
                conn.commit()
                logger.info("Successfully migrated existing users with user_id")
            
            # Add other missing columns if they don't exist
            missing_columns = {
                'username': 'TEXT UNIQUE',
                'is_active': 'INTEGER DEFAULT 1',
                'is_verified': 'INTEGER DEFAULT 0',
                'first_name': 'TEXT',
                'last_name': 'TEXT',
                'display_name': 'TEXT',
                'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'last_login': 'TIMESTAMP',
                'login_count': 'INTEGER DEFAULT 0',
                'verification_token': 'TEXT',
                'verification_sent_at': 'TIMESTAMP',
                'password_reset_token': 'TEXT',
                'password_reset_sent_at': 'TIMESTAMP',
                'preferences': 'TEXT'
            }
            
            for column_name, column_def in missing_columns.items():
                if column_name not in columns:
                    try:
                        cursor.execute(f'ALTER TABLE users ADD COLUMN {column_name} {column_def}')
                        logger.info(f"Added {column_name} column to users table")
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" not in str(e):
                            logger.warning(f"Could not add {column_name} column: {e}")
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error during database migration: {e}")
        
        # Ensure system_generated column exists (for existing databases)
        try:
            cursor.execute('ALTER TABLE saved_ideas ADD COLUMN system_generated INTEGER DEFAULT 0')
            conn.commit()
            logger.info("Added system_generated column to existing database")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                logger.warning(f"Could not add system_generated column: {e}")
        
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

# Global database instance
db_service = DatabaseService() 