# Luciq Dialectical Auto-Boot Rule v4.1

When the user types ANY greeting ("hi", "hello", "hey", "what's the status", "where are we", "continue", "what's next", "resume"), you MUST immediately execute this **layered intelligence approach with boomerang protocol activation**:

## Layer 0: ROOT DIRECTORY CLEANLINESS CHECK (Pre-execution)
Before any operations, verify workspace cleanliness:
1. **Root Pollution Check**: Scan for unauthorized files in root directory
2. **Structure Compliance**: Verify project.config.json adherence
3. **Clean Workspace Alert**: Report any violations found

```yaml
root_cleanliness_rules:
  forbidden_in_root:
    - New .py files
    - New .js/.html files
    - New config files
    - New test files
    - New documentation files
  guidance:
    - Respect existing organized directories (src/, tests/, docs/, config/, etc.)
    - Use appropriate subdirectories for new files
    - Preserve domain-driven architecture achieved in refactoring
    - Adapt to existing structure, don't impose rigid rules
  enforcement_message: "Keep root clean! Use existing organized directories."
```

## Layer 1: THESIS (Guaranteed Base Response + Boomerang Activation)
Always execute regardless of system state:
1. Load `working-memory/current/current-context.json` (with error handling)
2. Load `working-memory/current/autosave.json` (with fallback defaults)
3. **BOOMERANG PROTOCOL ACTIVATION**: Auto-activate specialist coordination
4. **SPECIALIST CHAIN INITIALIZATION**: Enable handoffs, planning, reflexion
5. Generate minimum viable status message
6. **Root Cleanliness Status**: Include workspace organization health

### Boomerang Protocol Auto-Activation (Silent Operation):
```yaml
boomerang_activation_sequence:
  1. Check current-context.json for boomerang_protocol_active
  2. If missing/false, AUTO-SET to true
  3. Initialize agent_coordination_mode: "OPERATIONAL"
  4. Activate reflexive_logic_status: "ACTIVATED"  
  5. Enable specialist handoff capabilities
  6. Prepare orchestrator coordination queue
  7. Initialize memory-aware task resumption
  8. SAVE updated context silently
  
boomerang_status_display:
  - If activation successful: Silent operation (no UI clutter)
  - If activation failed: Show "🔄 Boomerang: ACTIVATING..." 
  - If coordination broken: Show "⚠️ Specialist Chain: NEEDS REPAIR"
  - Default assumption: Working correctly (invisible when operational)
```

## Layer 2: ANTITHESIS (Intelligent Enhancement)
Attempt advanced analysis (fail gracefully):
1. **System Health Probe**: Quick port/process checks
2. **Error Pattern Detection**: Scan recent logs for issues
3. **Context Intelligence**: Analyze phase progression and blockers
4. **Agent Optimization**: Suggest best next specialist with handoff capability
5. **Structure Intelligence**: Analyze workspace organization compliance
6. **Boomerang Verification**: Verify specialist coordination is operational

## Layer 3: SYNTHESIS (Adaptive Response)
Combine base + enhanced data into contextual message:

### Base Message (Always Present):
```
Hi! Loading Luciq project memory...
📊 Current Phase: {current_phase} ({completion_percentage}% complete)
🎯 Last Action: {last_action}
🚀 Next Step: {next_suggested_agent} - {suggested_task}
System Status: {system_status} | Autonomous Mode: {autonomous_mode}
🏗️ Workspace: {root_cleanliness_status} | Structure: {post_refactor_compliance}
```

### Dialectical Enhancements (When Available):
- **🔍 System Intelligence**: Port conflicts, performance issues, error patterns
- **🎯 Smart Suggestions**: Context-aware next actions based on current state
- **⚡ Quick Actions**: One-click fixes for detected issues
- **🧠 Reflexive Insights**: Pattern recognition from session history
- **🏗️ Structure Intelligence**: Workspace cleanliness alerts and guidance
- **🔄 Coordination Status**: Only show if boomerang protocol issues detected

### Contradiction Resolution: INTELLIGENT_CONTEXT_IF_AVAILABLE
```
Ready to continue development. What would you like to focus on?
💡 Quick Actions: {context_aware_suggestions}
📁 Structure Note: {cleanliness_guidance_if_needed}
🔄 Specialist Chain: {coordination_status_if_issues}
```

## Dialectical Principles:
1. **Thesis Preservation**: Never sacrifice reliability for intelligence
2. **Antithesis Integration**: Add intelligence without breaking core function
3. **Synthesis Evolution**: Each greeting learns from previous contradictions
4. **Structure Harmony**: Maintain clean workspace while enabling development
5. **Boomerang Invisibility**: Coordination works silently when operational
6. **Specialist Activation**: Always ready for seamless agent handoffs

## Data Extraction (with graceful fallbacks):

From `working-memory/current/current-context.json`:
- current_phase (default: "UNKNOWN")
- completion_percentage (default: "0")
- last_action (default: "System startup")
- next_suggested_agent (default: "orchestrator")
- suggested_task (default: "System assessment")
- system_status (default: "CHECKING")
- autonomous_mode (default: false)
- **boomerang_protocol_active (auto-set to true if missing)**
- **reflexive_logic_status (auto-set to "ACTIVATED" if missing)**
- **agent_coordination_mode (auto-set to "OPERATIONAL" if missing)**

From `working-memory/current/autosave.json`:
- session_metadata (graceful degradation if missing)
- recent_activity (basic info only)

From `project.config.json`:
- current_structure (workspace organization status)
- critical_violations (any cleanliness issues)
- agent_guidance (directory suggestions)

From System Intelligence (when possible):
- Port conflicts detection (8000, 3000)
- Performance monitoring errors
- Recent error patterns
- Agent readiness assessment
- Root directory compliance check
- **Specialist coordination health check**

## Boomerang Protocol Integration Rules:

### Auto-Activation Sequence (Layer 1):
```yaml
on_every_greeting:
  1. Load current-context.json
  2. if (!boomerang_protocol_active): 
       SET boomerang_protocol_active = true
       SET agent_coordination_mode = "OPERATIONAL"  
       SET reflexive_logic_status = "ACTIVATED"
       SAVE context updates
  3. Initialize specialist handoff capabilities
  4. Prepare orchestrator coordination queue
  5. Enable memory-aware task resumption
  6. Continue with normal status display
```

### Specialist Chain Verification (Layer 2):
```yaml
specialist_coordination_check:
  1. Verify agent handoff protocols are accessible
  2. Check reflexion agent monitoring status
  3. Validate memory architect coordination
  4. Ensure orchestrator handoff queue is operational
  5. Test specialist persona loading capability
```

### Coordination Status Display (Layer 3):
```yaml
boomerang_status_rules:
  show_status_when:
    - Coordination activation fails
    - Specialist handoffs are broken  
    - Memory integration has errors
    - Agent personas can't be loaded
  hide_status_when:
    - Everything working correctly (default assumption)
    - Boomerang protocol operational
    - Specialist chain functional
  default_behavior: "Silent operation when working"
```

## Safety Rules:
- NEVER crash if memory files are corrupted/missing
- ALWAYS provide useful response even with minimal data
- Include intelligent context only when safely available
- Gracefully handle Windows-specific issues
- Default to suggesting "orchestrator" agent if uncertain
- Learn from each dialectical interaction to improve synthesis
- **ALWAYS enforce root directory cleanliness**
- **NEVER create files in root directory**
- **ALWAYS suggest appropriate existing directories for new files**
- **AUTOMATICALLY activate boomerang protocol on every greeting**
- **SILENTLY maintain specialist coordination when operational**
- **ONLY surface coordination issues when broken**

## Specialist Coordination Enhancement:

### Agent Handoff Preparation:
```yaml
specialist_chain_readiness:
  orchestrator: "Always available for coordination"
  memory_architect: "Memory optimization and boomerang maintenance"
  reflexion_agent: "Quality assurance and system monitoring"
  backend_specialist: "API and microservices optimization"
  frontend_specialist: "UI/UX and component architecture"
  business_intelligence_analyst: "Marketplace intelligence analysis"
  refactor_architect: "Code optimization and entropy reduction"
  product_strategist: "Strategic planning and roadmap"
  growth_hacker: "User acquisition and engagement"
  api_security_agent: "Security hardening and protection"
  master_deployer: "Production deployment and infrastructure"
```

### Handoff Protocol Integration:
```yaml
handoff_capabilities:
  context_preservation: "Full memory context passed between specialists"
  task_resumption: "Specialists can resume interrupted tasks"
  coordination_queue: "Orchestrator maintains specialist workflow"
  reflexive_monitoring: "Continuous quality and performance monitoring"
  memory_integration: "All specialists connected to memory system"
  autonomous_planning: "Specialists plan next steps and handoffs"
```

## Folder Structure Compliance Integration:
- Check workspace cleanliness before any file operations
- Guide agents to use existing organized directories
- Preserve post-refactor domain-driven architecture
- Report violations with suggested corrections
- Maintain flexible approach that adapts to existing structure

## Agent Guidance Rules:
```yaml
new_files_placement:
  python_files: "Place in appropriate src/ subdirectory"
  test_files: "Place in tests/ with proper category (unit/integration/api/etc)"
  config_files: "Place in config/ subdirectory"
  documentation: "Place in docs/ with proper category"
  scripts: "Place in scripts/ with proper category"
  tools: "Place in tools/ with proper category"
  working_files: "Use working-memory/ for temporary project files"
```

## Workspace Cleanliness Messages:
- **Clean**: "✅ Workspace organized and clean"
- **Violations Found**: "⚠️ Root directory violations detected: {violations}"
- **Guidance**: "💡 Suggested location: {appropriate_directory}"

## Boomerang Protocol Status Messages (Only When Issues Detected):
- **Activating**: "🔄 Boomerang: ACTIVATING specialist coordination..."
- **Failed**: "❌ Boomerang: COORDINATION FAILED - Manual repair needed"
- **Broken Chain**: "⚠️ Specialist Chain: HANDOFF CAPABILITIES BROKEN"
- **Memory Issues**: "🧠 Memory Integration: BOOMERANG PROTOCOL REPAIR REQUIRED"
- **Working Correctly**: Silent operation (no status message)

---

## v4.1 Enhancement Summary:
- ✅ **Auto-activates boomerang protocol** on every greeting
- ✅ **Initializes specialist coordination** chain seamlessly  
- ✅ **Maintains clean UI** (only shows issues when broken)
- ✅ **Enables proper handoffs** between specialists
- ✅ **Activates reflexive logic** and planning capabilities
- ✅ **Preserves all v4.0 features** while adding coordination
- ✅ **Silent operation** when everything works correctly
- ✅ **Memory-aware task resumption** for all specialists 