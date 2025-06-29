import sqlite3
import json
from pathlib import Path

# Connect to database
conn = sqlite3.connect('luciq_discovery.db')
cursor = conn.cursor()

# Add system_generated column if it doesn't exist
try:
    cursor.execute('ALTER TABLE saved_ideas ADD COLUMN system_generated INTEGER DEFAULT 0')
    print("Added system_generated column")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("system_generated column already exists")
    else:
        print(f"Error adding column: {e}")

# Check if we have any system ideas
cursor.execute('SELECT COUNT(*) FROM saved_ideas WHERE system_generated = 1')
system_count = cursor.fetchone()[0]
print(f"Current system ideas: {system_count}")

# If no system ideas, add some sample ones
if system_count == 0:
    print("Adding sample system ideas...")
    
    sample_ideas = [
        {
            "title": "AI-Powered Code Review Assistant",
            "description": "Automated code review tool that provides intelligent feedback and suggestions for developers, reducing review time and improving code quality.",
            "source": "r/programming - developers struggling with code review bottlenecks",
            "potential": "High - $50B+ developer tools market",
            "concept_data": {
                "score": 8.5,
                "reddit_data": {"score": 150, "num_comments": 45},
                "pain_point_indicators": ["time-consuming", "inconsistent reviews", "bottleneck"]
            }
        },
        {
            "title": "Smart Meeting Scheduler",
            "description": "AI-powered scheduling tool that automatically finds optimal meeting times across time zones and integrates with multiple calendar systems.",
            "source": "r/productivity - remote teams coordination issues",
            "potential": "Medium-High - $2B+ scheduling software market",
            "concept_data": {
                "score": 7.8,
                "reddit_data": {"score": 89, "num_comments": 32},
                "pain_point_indicators": ["timezone confusion", "scheduling conflicts", "coordination overhead"]
            }
        },
        {
            "title": "Customer Support Ticket Prioritizer",
            "description": "Machine learning system that automatically prioritizes and routes customer support tickets based on urgency and complexity.",
            "source": "r/customerservice - support teams overwhelmed with tickets",
            "potential": "High - $8B+ customer service software market",
            "concept_data": {
                "score": 8.2,
                "reddit_data": {"score": 203, "num_comments": 67},
                "pain_point_indicators": ["ticket overload", "priority confusion", "response delays"]
            }
        },
        {
            "title": "Expense Report Automation",
            "description": "Mobile app that uses OCR and AI to automatically categorize and submit expense reports from receipt photos.",
            "source": "r/accounting - manual expense reporting pain",
            "potential": "Medium - $3B+ expense management market",
            "concept_data": {
                "score": 7.5,
                "reddit_data": {"score": 124, "num_comments": 28},
                "pain_point_indicators": ["manual data entry", "receipt management", "approval delays"]
            }
        },
        {
            "title": "API Documentation Generator",
            "description": "Tool that automatically generates and maintains API documentation from code comments and usage patterns.",
            "source": "r/webdev - outdated API documentation issues",
            "potential": "Medium - $1B+ developer documentation market",
            "concept_data": {
                "score": 7.2,
                "reddit_data": {"score": 95, "num_comments": 23},
                "pain_point_indicators": ["outdated docs", "manual maintenance", "developer confusion"]
            }
        }
    ]
    
    # Create a system user if it doesn't exist
    cursor.execute('SELECT id FROM users WHERE email = ?', ('system@luciq.com',))
    system_user = cursor.fetchone()
    
    if not system_user:
        cursor.execute('''
            INSERT INTO users (email, password_hash) 
            VALUES (?, ?)
        ''', ('system@luciq.com', 'system_user_hash'))
        system_user_id = cursor.lastrowid
    else:
        system_user_id = system_user[0]
    
    # Insert system ideas
    for idea in sample_ideas:
        cursor.execute('''
            INSERT INTO saved_ideas 
            (user_id, idea_title, idea_description, pain_point_source, market_potential, concept_data, system_generated)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (
            system_user_id,
            idea["title"],
            idea["description"],
            idea["source"],
            idea["potential"],
            json.dumps(idea["concept_data"])
        ))
    
    print(f"Added {len(sample_ideas)} system ideas")

# Verify the data
cursor.execute('SELECT COUNT(*) FROM saved_ideas WHERE system_generated = 1')
final_count = cursor.fetchone()[0]
print(f"Final system ideas count: {final_count}")

cursor.execute('SELECT idea_title FROM saved_ideas WHERE system_generated = 1 LIMIT 3')
titles = cursor.fetchall()
print("Sample titles:")
for title in titles:
    print(f"  - {title[0]}")

conn.commit()
conn.close()
print("Database setup complete!") 