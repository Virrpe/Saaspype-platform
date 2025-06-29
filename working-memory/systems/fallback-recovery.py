#!/usr/bin/env python3
"""
Fallback Recovery System
Rebuilds system state from event logs when autosave.json is missing or corrupted
"""

import json
import yaml
from datetime import datetime, timezone
from pathlib import Path

def load_event_log():
    """Load and parse the event log"""
    try:
        events = []
        with open('working-memory/event-log.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
        return events
    except FileNotFoundError:
        print("⚠️ Event log not found - cannot recover state")
        return []
    except Exception as e:
        print(f"⚠️ Error loading event log: {e}")
        return []

def load_roadmap():
    """Load the project roadmap"""
    try:
        with open('roadmap.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("⚠️ Roadmap not found - using minimal state")
        return {"current_focus": {"active_phase": "unknown"}}
    except Exception as e:
        print(f"⚠️ Error loading roadmap: {e}")
        return {"current_focus": {"active_phase": "unknown"}}

def rebuild_autosave_from_events(events, roadmap):
    """Rebuild autosave.json from event log and roadmap"""
    
    # Find the most recent events
    recent_events = events[-10:] if len(events) >= 10 else events
    
    # Extract key information from recent events
    last_event = events[-1] if events else {}
    last_agent = last_event.get('agent', 'unknown')
    last_action = last_event.get('details', 'System initialization')
    
    # Get current phase from roadmap
    current_phase = roadmap.get('current_focus', {}).get('active_phase', 'initialization')
    
    # Count completed phases
    phases_completed = 0
    if 'phases' in roadmap:
        for phase in roadmap['phases']:
            if phase.get('status') == 'COMPLETED':
                phases_completed += 1
    
    # Rebuild autosave structure
    rebuilt_autosave = {
        "autosave_metadata": {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "session_id": f"LUCIQ_RECOVERY_{datetime.now().strftime('%Y%m%d')}",
            "autosave_version": "1.0.0-recovery",
            "context_preservation_mode": "RECOVERY",
            "rehydration_ready": True,
            "recovery_source": "event_log_rebuild"
        },
        
        "active_session_state": {
            "current_phase": current_phase,
            "phase_progress": "unknown",
            "last_major_action": last_action,
            "active_agent": last_agent,
            "next_suggested_agent": "orchestrator",
            "session_duration": "recovered",
            "tasks_completed_this_session": len(recent_events)
        },
        
        "active_file_paths": {
            "primary_focus": [
                "working-memory/event-log.jsonl",
                "working-memory/current-context.json",
                "roadmap.yaml"
            ],
            "recently_modified": [
                "working-memory/fallback-recovery.py"
            ],
            "next_likely_targets": [
                "working-memory/autosave.json"
            ]
        },
        
        "current_agent_focus": {
            "active_agent": last_agent,
            "agent_status": "RECOVERED",
            "last_action": last_action,
            "next_task": "Resume from recovery state",
            "coordination_chain": [last_agent, "orchestrator"]
        },
        
        "system_outputs": {
            "last_deliverable": "System state recovery",
            "current_deliverable": "Restored session continuity",
            "deliverables_in_progress": [
                "autosave.json recovery",
                "session state restoration"
            ],
            "quality_score": "85%",
            "user_satisfaction": "RECOVERY_MODE"
        },
        
        "next_suggestions": {
            "immediate_next_step": "Validate recovered state and continue",
            "suggested_agent": "orchestrator",
            "suggested_task": "Coordinate system validation and resume operations",
            "estimated_duration": "5-10 minutes",
            "dependencies": ["state validation", "memory integrity check"],
            "user_guidance": "System recovered from event logs - ready to continue"
        },
        
        "conversation_context": {
            "user_last_request": "System recovery initiated",
            "user_intent": "Restore session continuity",
            "user_preference": "Autonomous operation with recovery",
            "conversation_flow": "Recovery → Validation → Resume",
            "user_engagement_level": "RECOVERY"
        },
        
        "memory_summary": {
            "total_events_logged": len(events),
            "phases_completed": phases_completed,
            "agents_coordinated": len(set(event.get('agent', 'unknown') for event in events)),
            "deliverables_generated": "recovered",
            "autonomous_cycles_completed": "recovered",
            "system_health": "RECOVERED",
            "last_10_events_summary": f"Recovered from {len(recent_events)} recent events"
        },
        
        "rehydration_data": {
            "greeting_template": "Welcome back to Luciq! System recovered from event logs. Last active: {active_agent} working on {current_deliverable}. Phase: {current_phase}. Next suggestion: {next_suggested_agent} - {suggested_task}.",
            "context_loading_priority": ["autosave.json", "current-context.json", "event-log.jsonl", "roadmap.yaml"],
            "recovery_mode": "EVENT_LOG_REBUILD",
            "user_orientation_needed": True
        },
        
        "background_limits": {
            "max_events_in_context": 10,
            "summary_mode": "RECOVERY",
            "full_log_reference": "working-memory/event-log.jsonl",
            "context_optimization": "ENABLED",
            "memory_compression": "RECOVERY"
        }
    }
    
    return rebuilt_autosave

def rebuild_current_context_from_events(events, roadmap):
    """Rebuild current-context.json from event log and roadmap"""
    
    last_event = events[-1] if events else {}
    last_agent = last_event.get('agent', 'unknown')
    
    # Get current phase info
    current_phase = roadmap.get('current_focus', {}).get('active_phase', 'initialization')
    
    rebuilt_context = {
        "session_metadata": {
            "session_id": f"LUCIQ_RECOVERY_{datetime.now().strftime('%Y%m%d')}",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "framework_version": "Shelli DevKit v1.0.1+",
            "system_status": "RECOVERED",
            "autonomous_mode": "RECOVERY"
        },
        
        "project_state": {
            "active_project": "Luciq",
            "project_description": "Reflexive SaaS opportunity discovery and scaling platform",
            "current_phase": current_phase,
            "phase_status": "RECOVERED",
            "completion_percentage": 0,
            "last_major_milestone": "System recovery completed",
            "next_milestone": "Resume normal operations"
        },
        
        "recent_activity": {
            "last_action": "System state recovered from event logs",
            "last_agent_active": last_agent,
            "last_deliverable": "Recovery state",
            "last_handoff": f"{last_agent} → orchestrator (recovery)",
            "session_duration": "recovery",
            "tasks_completed_today": len(events[-10:]) if len(events) >= 10 else len(events)
        },
        
        "next_actions": {
            "immediate_priority": "Validate recovered state and resume operations",
            "next_suggested_agent": "orchestrator",
            "suggested_task": "Coordinate system validation and continue development",
            "estimated_duration": "5-10 minutes",
            "dependencies": ["state validation", "memory integrity check"]
        },
        
        "boot_sequence": {
            "auto_welcome_enabled": True,
            "context_loading_required": True,
            "roadmap_reference_active": True,
            "agent_status_check_required": True,
            "next_action_suggestion_enabled": True,
            "recovery_mode": True
        }
    }
    
    return rebuilt_context

def execute_fallback_recovery():
    """Execute the complete fallback recovery process"""
    print("🔄 Initiating fallback recovery from event logs...")
    
    # Load source data
    events = load_event_log()
    roadmap = load_roadmap()
    
    if not events:
        print("❌ Cannot recover - no event log available")
        return False
    
    print(f"📊 Found {len(events)} events in log")
    
    # Rebuild autosave.json
    try:
        rebuilt_autosave = rebuild_autosave_from_events(events, roadmap)
        with open('working-memory/autosave.json', 'w', encoding='utf-8') as f:
            json.dump(rebuilt_autosave, f, indent=2)
        print("✅ Rebuilt autosave.json from event log")
    except Exception as e:
        print(f"❌ Failed to rebuild autosave.json: {e}")
        return False
    
    # Rebuild current-context.json if missing
    if not Path('working-memory/current-context.json').exists():
        try:
            rebuilt_context = rebuild_current_context_from_events(events, roadmap)
            with open('working-memory/current-context.json', 'w', encoding='utf-8') as f:
                json.dump(rebuilt_context, f, indent=2)
            print("✅ Rebuilt current-context.json from event log")
        except Exception as e:
            print(f"❌ Failed to rebuild current-context.json: {e}")
            return False
    
    # Log recovery event
    try:
        recovery_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "fallback_recovery_completed",
            "agent": "fallback-recovery-system",
            "status": "SUCCESS",
            "details": f"System state rebuilt from {len(events)} events",
            "context": {
                "recovery_source": "event_log",
                "events_processed": len(events),
                "files_rebuilt": ["autosave.json", "current-context.json"],
                "recovery_mode": "FALLBACK"
            }
        }
        
        with open('working-memory/event-log.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(recovery_event) + '\n')
        
        print("✅ Recovery event logged")
    except Exception as e:
        print(f"⚠️ Failed to log recovery event: {e}")
    
    print("🎯 Fallback recovery completed successfully!")
    print("💡 System ready for auto-boot with recovered state")
    return True

if __name__ == "__main__":
    execute_fallback_recovery() 