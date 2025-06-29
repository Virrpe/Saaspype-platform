#!/usr/bin/env python3
"""
Update Claude API key with the new valid key
"""

def update_claude_key():
    print("🔧 Updating Claude API key...")
    
    # Read the file
    with open('master_luciq_api.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace both instances
    old_key = "sk-ant-api03-JG_B6x8OqMBQmJ0_qD7TKCz1t-IhgVJcwSPklPKGm5CCj5wZ_-2CwkL4Hp5MUCQxH_5CXX8JuMXcLq7Dw2H7mg-Ib47_AAA"
    new_key = "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"
    
    # Count replacements
    count = content.count(old_key)
    print(f"📊 Found {count} instances to replace")
    
    # Replace all instances
    new_content = content.replace(old_key, new_key)
    
    # Write back
    with open('master_luciq_api.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Replaced {count} instances with new valid Claude key")
    print("🚀 Ready to test real Claude API calls with token costs!")

if __name__ == "__main__":
    update_claude_key() 