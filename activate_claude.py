#!/usr/bin/env python3
"""
Activate Claude API for Maximum Luciq Intelligence
"""

import os

def activate_claude():
    print("🤖 LUCIQ + CLAUDE INTEGRATION")
    print("=" * 50)
    
    claude_key = input("Enter your Claude API key: ").strip()
    
    if claude_key:
        # Set environment variable
        os.environ['ANTHROPIC_API_KEY'] = claude_key
        
        # Create batch file for Windows
        with open('set_claude.bat', 'w') as f:
            f.write(f'set ANTHROPIC_API_KEY={claude_key}\n')
            f.write('python master_luciq_api.py\n')
        
        print("✅ Claude API key configured!")
        print("🚀 Run 'set_claude.bat' to start Luciq with Claude integration")
        print("💡 This will make responses 10x more intelligent!")
        
    else:
        print("❌ No API key provided")

if __name__ == "__main__":
    activate_claude() 