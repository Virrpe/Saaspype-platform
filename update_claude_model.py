#!/usr/bin/env python3
"""
Update Claude model to current version in master API
"""

def update_claude_model():
    print("🔧 Updating Claude model to current version...")
    
    # Read the file
    with open('master_luciq_api.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace both instances
    old_model = 'model="claude-3-sonnet-20240229"'
    new_model = 'model="claude-3-5-sonnet-20241022"'
    
    # Count replacements
    count = content.count(old_model)
    print(f"📊 Found {count} instances to replace")
    
    # Replace all instances
    new_content = content.replace(old_model, new_model)
    
    # Write back
    with open('master_luciq_api.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Replaced {count} instances with current Claude 3.5 Sonnet model")
    print("🚀 Ready to restart API with working Claude integration!")

if __name__ == "__main__":
    update_claude_model() 