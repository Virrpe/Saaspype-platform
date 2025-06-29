#!/usr/bin/env python3
"""
Auto-Boot System Validation Test
Tests the auto-boot and rehydration system components
"""

import json
import yaml
from pathlib import Path

def test_memory_files():
    """Test that all required memory files exist and are valid"""
    print("🧪 Testing memory file integrity...")
    
    required_files = [
        'working-memory/current-context.json',
        'working-memory/autosave.json', 
        'working-memory/last-10-events-summary.md',
        'roadmap.yaml'
    ]
    
    results = {}
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            try:
                if file_path.endswith('.json'):
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    results[file_path] = {"status": "✅ VALID", "size": len(str(data))}
                elif file_path.endswith('.yaml'):
                    with open(path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    results[file_path] = {"status": "✅ VALID", "size": len(str(data))}
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    results[file_path] = {"status": "✅ VALID", "size": len(content)}
            except Exception as e:
                results[file_path] = {"status": f"❌ INVALID: {e}", "size": 0}
        else:
            results[file_path] = {"status": "❌ MISSING", "size": 0}
    
    return results

def test_agent_triggers():
    """Test that agent files have proper activation triggers"""
    print("🧪 Testing agent activation triggers...")
    
    agent_files = [
        '.cursor/mdc/orchestrator.mdc',
        '.cursor/mdc/auto-boot-agent.mdc',
        '.cursor/mdc/reflexion-agent.mdc'
    ]
    
    greeting_triggers = ['hi', 'hello', 'status', 'what\'s the status']
    results = {}
    
    for agent_file in agent_files:
        path = Path(agent_file)
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for activation triggers section
                has_triggers = '<activation_triggers>' in content
                has_greeting_triggers = any(trigger in content for trigger in greeting_triggers)
                
                if has_triggers and has_greeting_triggers:
                    results[agent_file] = "✅ HAS GREETING TRIGGERS"
                elif has_triggers:
                    results[agent_file] = "⚠️ HAS TRIGGERS BUT NO GREETINGS"
                else:
                    results[agent_file] = "❌ NO ACTIVATION TRIGGERS"
                    
            except Exception as e:
                results[agent_file] = f"❌ ERROR: {e}"
        else:
            results[agent_file] = "❌ MISSING"
    
    return results

def test_context_loading():
    """Test context loading from memory files"""
    print("🧪 Testing context loading logic...")
    
    try:
        # Load current context
        with open('working-memory/current-context.json', 'r', encoding='utf-8') as f:
            current_context = json.load(f)
        
        # Load autosave
        with open('working-memory/autosave.json', 'r', encoding='utf-8') as f:
            autosave = json.load(f)
        
        # Load roadmap
        with open('roadmap.yaml', 'r', encoding='utf-8') as f:
            roadmap = yaml.safe_load(f)
        
        # Extract key information for welcome message
        current_phase = current_context.get('project_state', {}).get('current_phase', 'unknown')
        completion_percentage = current_context.get('project_state', {}).get('completion_percentage', 0)
        last_action = current_context.get('recent_activity', {}).get('last_action', 'unknown')
        next_agent = current_context.get('next_actions', {}).get('next_suggested_agent', 'unknown')
        suggested_task = current_context.get('next_actions', {}).get('suggested_task', 'unknown')
        system_status = current_context.get('session_metadata', {}).get('system_status', 'unknown')
        autonomous_mode = current_context.get('session_metadata', {}).get('autonomous_mode', 'unknown')
        
        # Generate test welcome message
        welcome_message = f"""Hi! Loading Luciq project memory...

📊 **Current Phase**: {current_phase} ({completion_percentage}% complete)
🎯 **Last Action**: {last_action}
🚀 **Next Step**: {next_agent} - {suggested_task}

**System Status**: {system_status} | **Autonomous Mode**: {autonomous_mode}
Ready to continue development. What would you like to focus on?"""
        
        return {
            "status": "✅ CONTEXT LOADING SUCCESSFUL",
            "welcome_message": welcome_message,
            "data_loaded": {
                "current_phase": current_phase,
                "completion_percentage": completion_percentage,
                "last_action": last_action,
                "next_agent": next_agent,
                "system_status": system_status
            }
        }
        
    except Exception as e:
        return {
            "status": f"❌ CONTEXT LOADING FAILED: {e}",
            "welcome_message": None,
            "data_loaded": None
        }

def test_fallback_recovery():
    """Test fallback recovery system"""
    print("🧪 Testing fallback recovery system...")
    
    fallback_script = Path('working-memory/fallback-recovery.py')
    event_log = Path('working-memory/event-log.jsonl')
    
    if not fallback_script.exists():
        return "❌ FALLBACK SCRIPT MISSING"
    
    if not event_log.exists():
        return "❌ EVENT LOG MISSING"
    
    # Check if event log has content
    try:
        with open(event_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            return "❌ EVENT LOG EMPTY"
        
        return f"✅ FALLBACK READY ({len(lines)} events available)"
        
    except Exception as e:
        return f"❌ FALLBACK TEST FAILED: {e}"

def run_validation():
    """Run complete auto-boot system validation"""
    print("🎯 Auto-Boot System Validation")
    print("=" * 50)
    
    # Test memory files
    memory_results = test_memory_files()
    print("\n📁 Memory Files:")
    for file_path, result in memory_results.items():
        print(f"  {file_path}: {result['status']}")
    
    # Test agent triggers
    trigger_results = test_agent_triggers()
    print("\n🤖 Agent Triggers:")
    for agent_file, result in trigger_results.items():
        print(f"  {Path(agent_file).name}: {result}")
    
    # Test context loading
    context_result = test_context_loading()
    print(f"\n🔄 Context Loading: {context_result['status']}")
    
    if context_result['welcome_message']:
        print("\n💬 Generated Welcome Message:")
        print("-" * 30)
        print(context_result['welcome_message'])
        print("-" * 30)
    
    # Test fallback recovery
    fallback_result = test_fallback_recovery()
    print(f"\n🔧 Fallback Recovery: {fallback_result}")
    
    # Overall assessment
    print("\n🎯 Overall Assessment:")
    
    memory_ok = all("✅" in result['status'] for result in memory_results.values())
    triggers_ok = all("✅" in result for result in trigger_results.values())
    context_ok = "✅" in context_result['status']
    fallback_ok = "✅" in fallback_result
    
    if memory_ok and triggers_ok and context_ok:
        print("✅ AUTO-BOOT SYSTEM FULLY OPERATIONAL")
        print("💡 System ready to handle greetings and provide context")
    elif memory_ok and context_ok:
        print("⚠️ AUTO-BOOT SYSTEM PARTIALLY OPERATIONAL")
        print("💡 Context loading works, but some agent triggers may need fixes")
    else:
        print("❌ AUTO-BOOT SYSTEM NEEDS REPAIRS")
        print("💡 Critical components missing or broken")
    
    if fallback_ok:
        print("✅ FALLBACK RECOVERY AVAILABLE")
    else:
        print("⚠️ FALLBACK RECOVERY NEEDS ATTENTION")

if __name__ == "__main__":
    run_validation() 