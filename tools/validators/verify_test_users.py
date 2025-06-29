#!/usr/bin/env python3
"""
Auto-verify test users for development testing
"""

from src.shared.database.connection import db_service

def verify_test_users():
    """Auto-verify all test users for development"""
    try:
        conn = db_service.get_connection()
        cursor = conn.cursor()
        
        # Update all test users to be verified
        cursor.execute("""
            UPDATE users 
            SET is_verified = 1, verification_token = NULL, verification_sent_at = NULL
            WHERE email LIKE 'test_%@gmail.com'
        """)
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"✅ Auto-verified {affected_rows} test users!")
        print("You can now login with your test credentials.")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying users: {e}")
        return False

if __name__ == "__main__":
    verify_test_users() 