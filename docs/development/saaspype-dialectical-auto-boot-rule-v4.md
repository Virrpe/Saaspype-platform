# Luciq Dialectical Auto-Boot Rule v4.0

When the user types ANY greeting ("hi", "hello", "hey", "what's the status", "where are we", "continue", "what's next", "resume"), you MUST immediately execute this **layered intelligence approach**:

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

## Layer 1: THESIS (Guaranteed Base Response)
Always execute regardless of system state:
1. Load `working-memory/current/current-context.json` (with error handling)
2. Load `working-memory/current/autosave.json` (with fallback defaults)
3. Generate minimum viable status message
4. **Root Cleanliness Status**: Include workspace organization health

## Layer 2: ANTITHESIS (Intelligent Enhancement)
Attempt advanced analysis (fail gracefully):
1. **System Health Probe**: Quick port/process checks
2. **Error Pattern Detection**: Scan recent logs for issues
3. **Context Intelligence**: Analyze phase progression and blockers
4. **Agent Optimization**: Suggest best next specialist
5. **Structure Intelligence**: Analyze workspace organization compliance

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

### Contradiction Resolution: INTELLIGENT_CONTEXT_IF_AVAILABLE
```
Ready to continue development. What would you like to focus on?
💡 Quick Actions: {context_aware_suggestions}
📁 Structure Note: {cleanliness_guidance_if_needed}
```

## Dialectical Principles:
1. **Thesis Preservation**: Never sacrifice reliability for intelligence
2. **Antithesis Integration**: Add intelligence without breaking core function
3. **Synthesis Evolution**: Each greeting learns from previous contradictions
4. **Structure Harmony**: Maintain clean workspace while enabling development

## Data Extraction (with graceful fallbacks):

From `working-memory/current/current-context.json`:
- current_phase (default: "UNKNOWN")
- completion_percentage (default: "0")
- last_action (default: "System startup")
- next_suggested_agent (default: "orchestrator")
- suggested_task (default: "System assessment")
- system_status (default: "CHECKING")
- autonomous_mode (default: false)

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