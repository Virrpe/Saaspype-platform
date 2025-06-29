#!/usr/bin/env python3
"""
Clean up master_luciq_api.py by removing duplicates and making it Claude-only
"""

def clean_api_file():
    print("🧹 Cleaning up master_luciq_api.py...")
    
    # Read the file
    with open('master_luciq_api.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Original file: {len(lines)} lines")
    
    # Find where the duplication starts (around line 5350)
    # Look for the second occurrence of imports
    duplicate_start = None
    for i, line in enumerate(lines):
        if i > 5000 and 'import feedparser' in line:
            duplicate_start = i
            break
    
    if duplicate_start:
        print(f"🔍 Found duplicate section starting at line {duplicate_start + 1}")
        
        # Keep only the first part (before duplicates)
        clean_lines = lines[:duplicate_start]
        
        # Add proper ending
        clean_lines.append('\n')
        clean_lines.append('# ================================================================================================\n')
        clean_lines.append('# MAIN APPLICATION STARTUP\n')
        clean_lines.append('# ================================================================================================\n')
        clean_lines.append('\n')
        clean_lines.append('if __name__ == "__main__":\n')
        clean_lines.append('    import uvicorn\n')
        clean_lines.append('    uvicorn.run(app, host="0.0.0.0", port=8000)\n')
        
        print(f"✅ Cleaned file: {len(clean_lines)} lines")
        print(f"🗑️ Removed: {len(lines) - len(clean_lines)} duplicate lines")
        
        # Write the clean file
        with open('master_luciq_api.py', 'w', encoding='utf-8') as f:
            f.writelines(clean_lines)
        
        print("✅ File cleaned successfully!")
        return True
    else:
        print("❌ Could not find duplicate section")
        return False

if __name__ == "__main__":
    clean_api_file() 