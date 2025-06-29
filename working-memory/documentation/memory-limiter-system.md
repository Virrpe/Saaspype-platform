# Background Memory Limiter System
# Intelligent context management to prevent overloading while preserving functionality

## Purpose
The memory limiter system ensures optimal performance by:
1. Preventing context window overload through intelligent compression
2. Maintaining essential information while reducing memory footprint
3. Providing background reference to full data when needed
4. Enabling seamless operation within context constraints

## Context Limit Management Strategy

### 1. Tiered Information Architecture
```javascript
// Information priority tiers for context inclusion
const informationTiers = {
  CRITICAL: {
    priority: 1,
    alwaysInclude: true,
    examples: [
      'current_phase',
      'active_agent', 
      'next_suggested_action',
      'system_status'
    ]
  },
  
  IMPORTANT: {
    priority: 2,
    includeWhenSpace: true,
    examples: [
      'recent_deliverables',
      'agent_coordination_chain',
      'phase_progress',
      'last_10_events_summary'
    ]
  },
  
  REFERENCE: {
    priority: 3,
    backgroundReference: true,
    examples: [
      'full_event_log',
      'complete_session_history',
      'detailed_agent_logs',
      'comprehensive_roadmap'
    ]
  }
};
```

### 2. Dynamic Context Compression
```javascript
function compressContextForLimits(contextData, maxTokens) {
  const compressed = {
    // Always include critical information
    critical: extractCriticalInfo(contextData),
    
    // Include important info if space allows
    important: includeIfSpace(contextData.important, maxTokens * 0.3),
    
    // Reference background data
    references: createBackgroundReferences(contextData.reference)
  };
  
  return compressed;
}

function createBackgroundReferences(fullData) {
  return {
    event_log: `${fullData.events.length} events logged (see working-memory/event-log.jsonl)`,
    session_history: `${fullData.sessions.length} sessions tracked (see memory/session-history.json)`,
    agent_logs: `${fullData.agent_actions.length} agent actions (see memory/agent-log.jsonl)`,
    roadmap: `6 phases defined, 2 completed (see roadmap.yaml)`
  };
}
```

## Memory Optimization Techniques

### 1. Summary-Based Context Loading
```markdown
**Instead of Full Logs**:
```json
{
  "event_1": {"timestamp": "...", "actor": "...", "details": "..."},
  "event_2": {"timestamp": "...", "actor": "...", "details": "..."},
  // ... 90 more events
}
```

**Use Compressed Summaries**:
```markdown
**Recent Activity**: 90 events logged. Last 10: memory-architect implementing persistence system, reflexive continuity layer completed, auto-welcome system active. Full log: working-memory/event-log.jsonl
```

### 2. Reference Pattern Implementation
```javascript
// Reference pattern for large data structures
function createSmartReference(dataType, fullData) {
  const references = {
    event_log: {
      summary: `${fullData.length} events logged`,
      recent: fullData.slice(-3), // Last 3 events only
      file_reference: 'working-memory/event-log.jsonl',
      access_pattern: 'background_reference'
    },
    
    roadmap: {
      summary: `6 phases: 2 completed, 1 active, 3 planned`,
      current_focus: fullData.current_focus,
      file_reference: 'roadmap.yaml',
      access_pattern: 'background_reference'
    },
    
    agent_status: {
      summary: `11 agents: 3 active, 8 ready`,
      priority_agents: fullData.filter(agent => agent.priority === 'HIGH'),
      file_reference: 'working-memory/current-context.json',
      access_pattern: 'inline_summary'
    }
  };
  
  return references[dataType];
}
```

### 3. Intelligent Context Switching
```javascript
function adaptContextForOperation(operationType, availableTokens) {
  switch(operationType) {
    case 'GREETING':
      return {
        include: ['current_phase', 'last_action', 'next_suggestion'],
        reference: ['full_history', 'detailed_roadmap'],
        maxTokens: availableTokens * 0.2
      };
      
    case 'AGENT_HANDOFF':
      return {
        include: ['agent_coordination', 'current_deliverables', 'dependencies'],
        reference: ['event_history', 'session_logs'],
        maxTokens: availableTokens * 0.4
      };
      
    case 'PHASE_TRANSITION':
      return {
        include: ['roadmap_status', 'completed_deliverables', 'next_phase_requirements'],
        reference: ['detailed_history', 'agent_logs'],
        maxTokens: availableTokens * 0.6
      };
  }
}
```

## Background Reference Strategies

### 1. File-Based References
```markdown
**Pattern**: Never inline large data, always reference

**Example**:
❌ **Don't do this**:
```json
{
  "full_event_log": [
    {"event": 1, "details": "..."},
    {"event": 2, "details": "..."},
    // ... 88 more events
  ]
}
```

✅ **Do this instead**:
```markdown
**Memory Status**: 90 events logged, last 10 summarized. Full log available at `working-memory/event-log.jsonl`
```

### 2. Progressive Disclosure
```javascript
// Load information progressively based on need
function loadContextProgressively(userRequest, currentContext) {
  // Start with minimal context
  let context = {
    phase: currentContext.current_phase,
    status: currentContext.system_status,
    next_action: currentContext.next_suggestion
  };
  
  // Add more context based on request type
  if (userRequest.includes('history')) {
    context.recent_summary = loadRecentSummary();
  }
  
  if (userRequest.includes('detailed')) {
    context.file_references = createFileReferences();
  }
  
  return context;
}
```

### 3. Smart Summarization
```javascript
function createIntelligentSummary(fullData, maxLength) {
  const summary = {
    // Key metrics only
    metrics: {
      total_events: fullData.events.length,
      phases_completed: fullData.phases.filter(p => p.status === 'COMPLETED').length,
      active_agents: fullData.agents.filter(a => a.status === 'ACTIVE').length,
      system_health: fullData.system.health_score
    },
    
    // Recent activity (compressed)
    recent_activity: fullData.events.slice(-5).map(event => ({
      actor: event.actor,
      action: event.event.substring(0, 50) + '...',
      phase: event.phase
    })),
    
    // Next actions only
    next_actions: {
      immediate: fullData.next_suggestions.immediate_next_step,
      agent: fullData.next_suggestions.suggested_agent,
      priority: fullData.next_suggestions.priority
    }
  };
  
  return summary;
}
```

## Context Window Monitoring

### 1. Real-Time Token Tracking
```javascript
function monitorContextUsage(currentContext) {
  const usage = {
    estimated_tokens: estimateTokenCount(currentContext),
    critical_info_tokens: estimateTokenCount(currentContext.critical),
    summary_tokens: estimateTokenCount(currentContext.summaries),
    reference_tokens: estimateTokenCount(currentContext.references),
    
    optimization_opportunities: identifyOptimizations(currentContext)
  };
  
  return usage;
}

function identifyOptimizations(context) {
  const optimizations = [];
  
  if (context.full_logs_included) {
    optimizations.push('Replace full logs with summaries');
  }
  
  if (context.redundant_information) {
    optimizations.push('Remove duplicate information');
  }
  
  if (context.detailed_history_included) {
    optimizations.push('Use background references for history');
  }
  
  return optimizations;
}
```

### 2. Automatic Compression Triggers
```javascript
function autoCompressOnLimit(contextData, tokenLimit) {
  const currentTokens = estimateTokenCount(contextData);
  
  if (currentTokens > tokenLimit * 0.8) {
    // Approaching limit - start compression
    return {
      action: 'COMPRESS',
      strategy: 'summary_based',
      target_reduction: '50%',
      preserve: ['critical_info', 'next_actions']
    };
  }
  
  if (currentTokens > tokenLimit * 0.9) {
    // Near limit - aggressive compression
    return {
      action: 'AGGRESSIVE_COMPRESS',
      strategy: 'reference_only',
      target_reduction: '70%',
      preserve: ['current_phase', 'immediate_next_step']
    };
  }
  
  return { action: 'NO_COMPRESSION_NEEDED' };
}
```

## Implementation Examples

### Example 1: Greeting with Memory Limits
```markdown
**Without Memory Limiter** (❌ Too much context):
```json
{
  "full_event_log": [90 events...],
  "complete_roadmap": [detailed 6 phases...],
  "all_agent_status": [11 agents with full details...],
  "session_history": [complete history...]
}
```

**With Memory Limiter** (✅ Optimized):
```markdown
**Context**: 90 events logged, backend_infrastructure phase (65%), memory-architect active
**Recent**: Persistence system implementation, reflexive continuity completed
**Next**: backend-specialist - A/B testing API development
**References**: Full logs at working-memory/event-log.jsonl, roadmap at roadmap.yaml
```

### Example 2: Agent Handoff with Compression
```markdown
**Handoff Context** (Compressed):
- **Current**: memory-architect → backend-specialist
- **Task**: A/B testing API infrastructure implementation  
- **Dependencies**: CONVERSION_OPTIMIZATION_PLAN.md, persistence system
- **Priority**: HIGH
- **Background**: 90 events logged, 2 phases completed, system operational

**Full Details**: Available in working-memory/current-context.json
```

### Example 3: Phase Transition with References
```markdown
**Phase Transition** (Reference-Based):
- **Completing**: backend_infrastructure (95% complete)
- **Next**: monetization_strategy phase
- **Deliverables**: ✅ A/B testing API, ✅ Analytics system, ✅ Security audit
- **Agents Ready**: monetization-agent, growth-hacker, product-strategist

**Detailed History**: See working-memory/last-10-events-summary.md
**Full Roadmap**: See roadmap.yaml
```

## Reflexion Integration

### Quality Monitoring
- Monitor context compression effectiveness
- Validate information preservation during compression
- Track user satisfaction with compressed context
- Ensure critical information never lost

### Self-Optimization
- Learn optimal compression ratios for different operations
- Improve summary quality over time
- Optimize reference patterns based on usage
- Enhance context switching efficiency

## Success Metrics

### Memory Efficiency
- **Context Size Reduction**: Target 80-90% compression
- **Information Preservation**: Target 100% critical info retained
- **Performance Impact**: Target <5% response time increase
- **User Experience**: Target no degradation in functionality

### System Performance
- **Token Usage**: Stay within 80% of context limits
- **Compression Speed**: Target <1 second compression time
- **Reference Accuracy**: Target 100% correct file references
- **Recovery Success**: Target 100% successful context recovery

This memory limiter system ensures Luciq operates efficiently within context constraints while maintaining full functionality and zero information loss through intelligent compression and background referencing. 