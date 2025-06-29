#!/usr/bin/env python3
"""
Luciq Data Migration Script
Migrates existing discovery data into the new database structure
"""

import sqlite3
import json
import sys
from datetime import datetime
from pathlib import Path

DATABASE = "luciq_discovery.db"

def create_system_user():
    """Create a system user for system-generated content"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Check if system user already exists
        cursor.execute("SELECT id FROM users WHERE email = 'system@luciq.internal'")
        system_user = cursor.fetchone()
        
        if system_user:
            print(f"ℹ️  System user already exists with ID: {system_user[0]}")
            return system_user[0]
        
        # Create system user
        cursor.execute("""
            INSERT INTO users (email, password_hash, created_at)
            VALUES (?, ?, ?)
        """, (
            'system@luciq.internal',
            'system_generated_content',  # Not a real password
            datetime.now().isoformat()
        ))
        
        system_user_id = cursor.lastrowid
        conn.commit()
        print(f"✅ Created system user with ID: {system_user_id}")
        return system_user_id
        
    except Exception as e:
        print(f"❌ Error creating system user: {e}")
        return None
    finally:
        conn.close()

def add_system_generated_column():
    """Add system_generated column to saved_ideas table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(saved_ideas)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'system_generated' not in columns:
            cursor.execute("ALTER TABLE saved_ideas ADD COLUMN system_generated BOOLEAN DEFAULT FALSE")
            print("✅ Added system_generated column to saved_ideas table")
        else:
            print("ℹ️  system_generated column already exists")
            
        conn.commit()
    except Exception as e:
        print(f"❌ Error adding system_generated column: {e}")
    finally:
        conn.close()

def migrate_pain_points_to_discovery_sessions(system_user_id):
    """Migrate top 10 pain points from pain-points-database.json to discovery_sessions table"""
    
    # Load pain points data
    pain_points_file = Path("luciq/memory/pain-points-database.json")
    if not pain_points_file.exists():
        print(f"❌ Pain points file not found: {pain_points_file}")
        return False
    
    with open(pain_points_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pain_points = data.get('pain_points', [])
    if not pain_points:
        print("❌ No pain points found in data")
        return False
    
    # Take top 10 pain points (sorted by score)
    top_pain_points = sorted(pain_points, key=lambda x: x.get('score', 0), reverse=True)[:10]
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Group by subreddit for realistic session data
        subreddit_groups = {}
        for point in top_pain_points:
            subreddit = point.get('subreddit', 'unknown')
            if subreddit not in subreddit_groups:
                subreddit_groups[subreddit] = []
            subreddit_groups[subreddit].append(point)
        
        sessions_created = 0
        for subreddit, points in subreddit_groups.items():
            session_data = {
                "source": "historical_migration",
                "pain_points": points,
                "migration_timestamp": datetime.now().isoformat()
            }
            
            pain_points_found = len([p for p in points if p.get('pain_point_indicators')])
            
            cursor.execute("""
                INSERT INTO discovery_sessions (user_id, subreddit, posts_analyzed, pain_points_found, session_data, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                system_user_id,  # Use system user ID
                subreddit,
                len(points),
                pain_points_found,
                json.dumps(session_data),
                datetime.now().isoformat()
            ))
            sessions_created += 1
        
        conn.commit()
        print(f"✅ Migrated {len(top_pain_points)} pain points into {sessions_created} discovery sessions")
        return True
        
    except Exception as e:
        print(f"❌ Error migrating pain points: {e}")
        return False
    finally:
        conn.close()

def migrate_ranked_opportunities_to_saved_ideas(system_user_id):
    """Migrate top 20 ranked opportunities to saved_ideas table with system_generated=true"""
    
    # Load ranked opportunities data
    ranked_file = Path("luciq/memory/ranked-opportunities.json")
    if not ranked_file.exists():
        print(f"❌ Ranked opportunities file not found: {ranked_file}")
        return False
    
    with open(ranked_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    opportunities = data.get('ranked_opportunities', [])
    if not opportunities:
        print("❌ No ranked opportunities found in data")
        return False
    
    # Take top 20 opportunities (already sorted by rank)
    top_opportunities = opportunities[:20]
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        ideas_created = 0
        for opp in top_opportunities:
            # Extract key information
            title = opp.get('title', 'Untitled Opportunity')
            
            # Create description from original data
            original_data = opp.get('original_data', {})
            selftext = original_data.get('selftext', '')
            description = selftext[:500] + "..." if len(selftext) > 500 else selftext
            
            if not description:
                description = f"Pain point identified from r/{opp.get('subreddit', 'unknown')} with {opp.get('score', 0)} opportunity score"
            
            # Pain point source
            permalink = opp.get('permalink', '')
            pain_point_source = f"Reddit: {permalink}" if permalink else f"r/{opp.get('subreddit', 'unknown')}"
            
            # Market potential based on score and business potential
            score = opp.get('score', 0)
            business_potential = opp.get('business_potential', 'unknown')
            market_potential = f"{business_potential.title()} (Score: {score}/10)"
            
            # Concept data with all the analysis
            concept_data = {
                "rank": opp.get('rank'),
                "score": score,
                "domain": opp.get('domain'),
                "scoring_breakdown": opp.get('scoring_breakdown', {}),
                "pain_point_indicators": opp.get('pain_point_indicators', []),
                "reddit_data": {
                    "author": opp.get('author'),
                    "subreddit": opp.get('subreddit'),
                    "permalink": permalink,
                    "score": original_data.get('score', 0),
                    "num_comments": original_data.get('num_comments', 0)
                },
                "migration_source": "ranked_opportunities_migration"
            }
            
            cursor.execute("""
                INSERT INTO saved_ideas (user_id, idea_title, idea_description, pain_point_source, market_potential, concept_data, system_generated, saved_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                system_user_id,  # Use system user ID instead of None
                title,
                description,
                pain_point_source,
                market_potential,
                json.dumps(concept_data),
                True,  # system_generated = true
                datetime.now().isoformat()
            ))
            ideas_created += 1
        
        conn.commit()
        print(f"✅ Migrated {ideas_created} ranked opportunities to saved_ideas with system_generated=true")
        return True
        
    except Exception as e:
        print(f"❌ Error migrating ranked opportunities: {e}")
        return False
    finally:
        conn.close()

def verify_migration():
    """Verify the migration was successful"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Check discovery sessions
        cursor.execute("SELECT COUNT(*) FROM discovery_sessions")
        sessions_count = cursor.fetchone()[0]
        
        # Check system-generated ideas
        cursor.execute("SELECT COUNT(*) FROM saved_ideas WHERE system_generated = 1")
        system_ideas_count = cursor.fetchone()[0]
        
        # Check total ideas
        cursor.execute("SELECT COUNT(*) FROM saved_ideas")
        total_ideas_count = cursor.fetchone()[0]
        
        print(f"\n📊 Migration Summary:")
        print(f"   Discovery Sessions: {sessions_count}")
        print(f"   System-Generated Ideas: {system_ideas_count}")
        print(f"   Total Ideas: {total_ideas_count}")
        
        # Show sample system-generated ideas
        cursor.execute("""
            SELECT idea_title, market_potential 
            FROM saved_ideas 
            WHERE system_generated = 1 
            ORDER BY saved_at DESC 
            LIMIT 5
        """)
        
        sample_ideas = cursor.fetchall()
        if sample_ideas:
            print(f"\n🔥 Top System-Generated Ideas:")
            for i, (title, market_potential) in enumerate(sample_ideas, 1):
                print(f"   {i}. {title[:60]}... ({market_potential})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False
    finally:
        conn.close()

def main():
    """Run the complete migration process"""
    print("🚀 Starting Luciq Data Migration...")
    print("=" * 60)
    
    # Step 0: Create system user
    print("\n0️⃣ Creating system user...")
    system_user_id = create_system_user()
    if not system_user_id:
        print("❌ Failed to create system user")
        return False
    
    # Step 1: Update database schema
    print("\n1️⃣ Updating database schema...")
    add_system_generated_column()
    
    # Step 2: Migrate pain points to discovery sessions
    print("\n2️⃣ Migrating pain points to discovery sessions...")
    if not migrate_pain_points_to_discovery_sessions(system_user_id):
        print("❌ Failed to migrate pain points")
        return False
    
    # Step 3: Migrate ranked opportunities to saved ideas
    print("\n3️⃣ Migrating ranked opportunities to saved ideas...")
    if not migrate_ranked_opportunities_to_saved_ideas(system_user_id):
        print("❌ Failed to migrate ranked opportunities")
        return False
    
    # Step 4: Verify migration
    print("\n4️⃣ Verifying migration...")
    if not verify_migration():
        print("❌ Migration verification failed")
        return False
    
    print("\n✅ Migration completed successfully!")
    print("🎉 Luciq discovery data is now integrated into the new database")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 