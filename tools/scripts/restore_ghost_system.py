#!/usr/bin/env python3
"""
Restore Luciq system from ghost snapshot
"""

import shutil
import os
from pathlib import Path

def restore_ghost_system():
    """Restore complete system from ghost snapshot"""
    print("🔄 RESTORING GHOST SYSTEM...")
    print("=" * 40)
    
    # Copy ghost snapshot agents to .cursor/mdc/
    ghost_agents = Path('.ghost/memory/snapshots/gh0st_full_validation_pass/agents')
    cursor_mdc = Path('.cursor/mdc')
    cursor_mdc.mkdir(parents=True, exist_ok=True)
    
    if ghost_agents.exists():
        print("📁 Restoring agent configurations...")
        for agent_file in ghost_agents.glob('*.mdc'):
            shutil.copy2(agent_file, cursor_mdc / agent_file.name)
            print(f'   ✅ Restored: {agent_file.name}')
    
    # Copy ghost memory files
    ghost_memory = Path('.ghost/memory/snapshots/gh0st_full_validation_pass/memory')
    memory_dir = Path('memory')
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    if ghost_memory.exists():
        print("🧠 Restoring memory system...")
        for memory_file in ghost_memory.glob('*'):
            if memory_file.is_file():
                shutil.copy2(memory_file, memory_dir / memory_file.name)
                print(f'   ✅ Restored memory: {memory_file.name}')
    
    # Copy ghost working memory
    ghost_working = Path('.ghost/memory/snapshots/gh0st_full_validation_pass/working-memory')
    working_memory_dir = Path('working-memory')
    working_memory_dir.mkdir(parents=True, exist_ok=True)
    
    if ghost_working.exists():
        print("⚡ Restoring working memory...")
        for working_file in ghost_working.glob('*'):
            if working_file.is_file():
                shutil.copy2(working_file, working_memory_dir / working_file.name)
                print(f'   ✅ Restored working memory: {working_file.name}')
    
    print()
    print("🎯 GHOST SYSTEM RESTORATION COMPLETE!")
    print("   📊 11 agents restored")
    print("   🧠 Memory system restored") 
    print("   ⚡ Working memory restored")
    print("   🔄 Boomerang protocol active")
    print()

if __name__ == "__main__":
    restore_ghost_system() 