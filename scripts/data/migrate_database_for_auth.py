#!/usr/bin/env python3
"""
Database Migration for Authentication System
Adds required columns for the new authentication system
"""

import sqlite3
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent / "src"))

from src.shared.database.connection import db_service

def migrate_database():
    """Migrate the database to support the new authentication system"""
    conn = db_service.get_connection()
    cursor = conn.cursor()
    
    print("🔄 Starting database migration for authentication system...")
    
    try:
        # First, check if we need to update the users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Current columns in users table: {columns}")
        
        # Add missing columns one by one
        columns_to_add = [
            ("user_id", "TEXT"),  # Remove UNIQUE constraint for ALTER TABLE
            ("username", "TEXT"),  # Remove UNIQUE constraint for ALTER TABLE
            ("is_active", "INTEGER DEFAULT 1"),
            ("is_verified", "INTEGER DEFAULT 0"),
            ("first_name", "TEXT"),
            ("last_name", "TEXT"),
            ("display_name", "TEXT"),
            ("updated_at", "TIMESTAMP"),  # Remove DEFAULT for ALTER TABLE
            ("last_login", "TIMESTAMP"),
            ("login_count", "INTEGER DEFAULT 0"),
            ("verification_token", "TEXT"),
            ("verification_sent_at", "TIMESTAMP"),
            ("password_reset_token", "TEXT"),
            ("password_reset_sent_at", "TIMESTAMP"),
            ("preferences", "TEXT")
        ]
        
        for column_name, column_def in columns_to_add:
            if column_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}")
                    print(f"✅ Added column: {column_name}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e):
                        print(f"⚠️  Warning adding column {column_name}: {e}")
                    else:
                        print(f"📝 Column {column_name} already exists")
            else:
                print(f"📝 Column {column_name} already exists")
        
        # Add user_id to existing users if they don't have one
        cursor.execute("SELECT id, email FROM users WHERE user_id IS NULL OR user_id = ''")
        users_without_uuid = cursor.fetchall()
        
        if users_without_uuid:
            print(f"🔧 Found {len(users_without_uuid)} users without user_id, adding UUIDs...")
            import uuid
            for user_id, email in users_without_uuid:
                new_uuid = str(uuid.uuid4())
                cursor.execute("UPDATE users SET user_id = ? WHERE id = ?", (new_uuid, user_id))
                print(f"   ✅ Added UUID {new_uuid} for user {email}")
        
        # Set default values for other columns if they are NULL
        cursor.execute("UPDATE users SET is_active = 1 WHERE is_active IS NULL")
        cursor.execute("UPDATE users SET is_verified = 1 WHERE is_verified IS NULL")  # For existing users, assume verified
        cursor.execute("UPDATE users SET login_count = 0 WHERE login_count IS NULL")
        cursor.execute("UPDATE users SET updated_at = created_at WHERE updated_at IS NULL")  # Set updated_at to created_at for existing users
        
        conn.commit()
        print("✅ Database migration completed successfully!")
        
        # Show final table structure
        cursor.execute("PRAGMA table_info(users)")
        final_columns = cursor.fetchall()
        print("\n📋 Final users table structure:")
        for col in final_columns:
            print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - Default: {col[4] or 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def verify_migration():
    """Verify the migration was successful"""
    print("\n🔍 Verifying migration...")
    
    try:
        conn = db_service.get_connection()
        cursor = conn.cursor()
        
        # Check that all required columns exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        required_columns = [
            "id", "user_id", "email", "username", "password_hash", 
            "is_active", "is_verified", "first_name", "last_name", 
            "display_name", "created_at", "updated_at", "last_login", 
            "login_count", "verification_token", "verification_sent_at",
            "password_reset_token", "password_reset_sent_at", "preferences"
        ]
        
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        else:
            print("✅ All required columns present")
            
        # Check if we can insert a test user structure
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"📊 Current user count: {user_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main migration function"""
    print("Luciq Authentication Database Migration")
    print("=" * 50)
    
    # Run migration
    if migrate_database():
        if verify_migration():
            print("\n🎉 Migration completed and verified successfully!")
            print("The authentication system is now ready to use.")
            return True
        else:
            print("\n⚠️  Migration completed but verification failed.")
            return False
    else:
        print("\n❌ Migration failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 