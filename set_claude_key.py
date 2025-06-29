#!/usr/bin/env python3
"""
Quick script to set Claude API key as environment variable
Run this before starting the API for maximum intelligence
"""

import os

def set_claude_key():
    print("🧠 LUCIQ INTELLIGENCE ENHANCEMENT")
    print("=" * 50)
    
    claude_key = input("Enter your Claude API key: ").strip()
    
    if claude_key:
        # Set environment variable for current session
        os.environ['ANTHROPIC_API_KEY'] = claude_key
        print("✅ Claude API key set!")
        print("🚀 Now restart the API to activate enhanced intelligence")
        
        # Also create a batch file for persistence
        with open('set_env.bat', 'w') as f:
            f.write(f'set ANTHROPIC_API_KEY={claude_key}\n')
            f.write('echo Claude API key configured!\n')
        
        print("📝 Created set_env.bat for future use")
    else:
        print("❌ No API key provided")

if __name__ == "__main__":
    set_claude_key() 