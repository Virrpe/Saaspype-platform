#!/usr/bin/env python3
"""
Fix Claude API key by hardcoding it directly in the master API file
"""

def fix_claude_key():
    print("🔧 Hardcoding Claude API key...")
    
    # Read the file
    with open('master_luciq_api.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace both instances
    old_pattern = "anthropic_key = os.getenv('ANTHROPIC_API_KEY')"
    new_pattern = 'anthropic_key = "sk-ant-api03-JG_B6x8OqMBQmJ0_qD7TKCz1t-IhgVJcwSPklPKGm5CCj5wZ_-2CwkL4Hp5MUCQxH_5CXX8JuMXcLq7Dw2H7mg-Ib47_AAA"'
    
    # Count replacements
    count = content.count(old_pattern)
    print(f"📊 Found {count} instances to replace")
    
    # Replace all instances
    new_content = content.replace(old_pattern, new_pattern)
    
    # Write back
    with open('master_luciq_api.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Replaced {count} instances with hardcoded Claude key")
    print("🚀 Claude API key is now hardcoded - restart API to test!")

if __name__ == "__main__":
    fix_claude_key() 