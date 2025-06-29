# Luciq Dialectical Auto-Boot Rule v4.2

When the user types ANY greeting ("hi", "hello", "hey", "what's the status", "where are we", "continue", "what's next", "resume"), you MUST immediately execute this **layered intelligence approach with smart agent coordination**:

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
3. **ACTIVATE BOOMERANG PROTOCOL**: Set `boomerang_protocol_active = true`
4. **INITIALIZE AGENT COORDINATION**: Enable specialist routing and handoffs
5. Generate minimum viable status message
6. **Root Cleanliness Status**: Include workspace organization health

## Layer 2: ANTITHESIS (Intelligent Enhancement)
Attempt advanced analysis (fail gracefully):
1. **System Health Probe**: Quick port/process checks
2. **Error Pattern Detection**: Scan recent logs for issues
3. **Context Intelligence**: Analyze phase progression and blockers
4. **Smart Agent Selection**: Assess which specialists are needed
5. **Structure Intelligence**: Analyze workspace organization compliance
6. **Cost Assessment**: Determine optimal coordination pattern

## Layer 3: SYNTHESIS (Adaptive Response)
Combine base + enhanced data into contextual message with **smart coordination**:

### Base Message (Always Present):
```
Hi! Loading Luciq project memory...
📊 Current Phase: {current_phase} ({completion_percentage}% complete)
🎯 Last Action: {last_action}
🚀 Next Step: {next_suggested_agent} - {suggested_task}
System Status: {system_status} | Autonomous Mode: {autonomous_mode}
🏗️ Workspace: {root_cleanliness_status} | Structure: {post_refactor_compliance}
🔄 Coordination: {boomerang_status} | Agents: {available_specialists}
```

### Smart Coordination Enhancements (When Triggered):
- **🧠 Intelligent Routing**: Context-aware specialist selection from `.cursor/mdc/`
- **💰 Cost-Conscious Coordination**: Progressive escalation (single → parallel → crisis)
- **⚡ Quick Fixes**: Automatic problem resolution for known patterns
- **🔄 True Boomerang**: Working handoffs with memory persistence
- **🏗️ Structure Harmony**: Workspace compliance with feature integration

### Cost-Conscious Coordination Logic:
```yaml
coordination_tiers:
  tier_1_simple: 
    pattern: "Single specialist activation"
    triggers: ["Basic questions", "File operations", "Status checks"]
    cost_impact: "Minimal"
    
  tier_2_moderate:
    pattern: "Paired specialists (2 agents)"
    triggers: ["Cross-domain tasks", "Integration work", "Problem solving"]
    cost_impact: "Moderate"
    
  tier_3_complex:
    pattern: "Coordinated team (3-4 agents)"
    triggers: ["Multi-source analysis", "System refactoring", "Feature development"]
    cost_impact: "Higher but efficient"
    
  tier_4_crisis:
    pattern: "Full specialist mobilization"
    triggers: ["System failures", "Emergency fixes", "Critical coordination"]
    cost_impact: "High but justified"
```

## Dialectical Principles:
1. **Thesis Preservation**: Never sacrifice reliability for intelligence
2. **Antithesis Integration**: Add intelligence without breaking core function
3. **Synthesis Evolution**: Each greeting learns from previous contradictions
4. **Structure Harmony**: Maintain clean workspace while enabling development
5. **Cost Intelligence**: Maximize value, minimize expense through smart routing

## Enhanced Data Extraction (with graceful fallbacks):

From `working-memory/current/current-context.json`:
- current_phase (default: "INITIALIZATION")
- completion_percentage (default: "0")
- last_action (default: "System startup")
- next_suggested_agent (default: "orchestrator")
- suggested_task (default: "System assessment")
- system_status (default: "CHECKING")
- autonomous_mode (default: false)
- **boomerang_protocol_active** (SET TO: true)

From `working-memory/current/autosave.json`:
- session_metadata (graceful degradation if missing)
- recent_activity (basic info only)

From `project.config.json`:
- current_structure (workspace organization status)
- critical_violations (any cleanliness issues)
- agent_guidance (directory suggestions)

From **Unified Agent System** (`.cursor/mdc/`):
- Available specialists count
- Agent readiness status
- Coordination capabilities
- Cost optimization settings

## Smart Agent Coordination Features:

### 🎯 **Unified Agent Reference**:
```yaml
agent_system_architecture:
  primary_location: ".cursor/mdc/"
  agent_count: 13
  legacy_archived: "archive/legacy-agents/ClaudeAgents/"
  coordination_data: "working-memory/agents/"
  status: "UNIFIED_AND_OPERATIONAL"
```

### 🧠 **Intelligent Specialist Selection**:
```yaml
smart_routing_logic:
  context_analysis: "Analyze user request complexity and domain"
  specialist_matching: "Route to appropriate .cursor/mdc/ agent"
  cost_optimization: "Use minimum viable specialist combination"
  parallel_coordination: "Enable when cost-justified"
  
available_specialists:
  - orchestrator (coordination, project management)
  - memory-architect (memory systems, coordination repair)
  - frontend-specialist (UI/UX, JavaScript, components)
  - backend-specialist (API, databases, servers)
  - discovery-intelligence-specialist (multi-source data analysis)
  - api-security-agent (security, authentication, authorization)
  - master-deployer (deployment, DevOps, infrastructure)
  - reflexion-agent (quality assurance, monitoring, improvement)
  - growth-hacker (marketing, user acquisition, metrics)
  - monetization-agent (revenue, pricing, business models)
  - product-strategist (strategy, roadmaps, features)
  - auto-boot (system initialization and coordination)
```

### ⚡ **Real Boomerang Protocol Activation**:
```yaml
boomerang_protocol_v4.2:
  initialization: "Set boomerang_protocol_active = true on every greeting"
  memory_persistence: "Context preserved across all conversations"
  specialist_handoffs: "Working agent-to-agent coordination"
  task_resumption: "Automatic continuation of interrupted workflows"
  failure_recovery: "Smart routing around blocked specialists"
  cost_awareness: "Progressive escalation prevents expensive loops"
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
- **Activate boomerang protocol on EVERY greeting**
- **Reference agents from .cursor/mdc/ only**
- **Use cost-conscious coordination patterns**

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
  
agent_coordination:
  reference_location: ".cursor/mdc/"
  legacy_location: "archive/legacy-agents/ClaudeAgents/"
  coordination_data: "working-memory/agents/"
  activation_method: "Context-aware smart routing"
  cost_management: "Progressive escalation tiers"
```

## Enhanced Coordination Messages:
- **Clean + Simple**: "✅ All systems operational, ready for development"
- **Issues Detected**: "⚠️ {issue_type} detected, routing to {specialist_name}"
- **Cost Optimization**: "💰 Using {tier_level} coordination for optimal efficiency"
- **Boomerang Active**: "🔄 Task resumption enabled, context preserved"
- **Agent Ready**: "🎯 {specialist_count} specialists available via unified system" 