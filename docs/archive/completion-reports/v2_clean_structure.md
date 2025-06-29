# Luciq V2 Clean Project Structure
**Post-Cleanup Architecture - Discovery Engine Focus**

```
luciq/
├── 📁 apps/                           # Core application
│   ├── 📁 frontend/                   # Clean V2 frontend
│   │   ├── 📁 pages/                  # Core discovery pages
│   │   │   ├── index.html             # Landing page with system ideas
│   │   │   ├── auth.html              # Login/Registration
│   │   │   ├── dashboard.html         # User dashboard
│   │   │   ├── discover.html          # Discovery interface
│   │   │   └── my-ideas.html          # Saved ideas management
│   │   ├── 📁 components/             # Essential components only
│   │   │   ├── 📁 foundation/         # Basic UI components
│   │   │   ├── 📁 data-display/       # Discovery-specific displays
│   │   │   └── 📁 advanced/           # Advanced components
│   │   │       └── NotificationSystem.js  # Keep only this
│   │   ├── 📁 js/                     # Core JavaScript
│   │   │   └── main.js                # Discovery functionality only
│   │   ├── 📁 styles/                 # Clean CSS
│   │   └── 📁 assets/                 # Static assets
│   └── 📁 src/                        # Backend source
│       ├── 📁 api/                    # Discovery API
│       │   ├── main.py                # Core discovery API (port 8001)
│       │   └── 📁 utils/              # API utilities
│       └── 📁 prompts/                # LLM prompts
│           └── 📁 discovery/          # Discovery-specific prompts
│
├── 📁 luciq/                       # Agent system
│   ├── 📁 src/agents/                 # Consolidated agents
│   │   ├── opportunity_ranker_fixed.py    # Keep this version
│   │   ├── advanced_discovery_engine.py  # Core discovery logic
│   │   ├── concept_generator.py           # SaaS concept generation
│   │   ├── orchestrator_coordinator.py   # Agent coordination
│   │   └── mock_pain_point_generator.py  # Testing utilities
│   ├── 📁 memory/                     # Discovery memory
│   ├── 📁 docs/                       # Agent documentation
│   └── 📁 scripts/                    # Agent scripts
│
├── 📁 working-memory/                 # Active session data
│   ├── current-context.json          # Current project state
│   ├── autosave.json                  # Session autosave
│   └── *.json                         # Session files
│
├── 📁 memory/                         # Core discovery memory
│   └── 📁 snapshots/                  # Memory snapshots
│
├── 📁 ClaudeAgents/                   # Agent system configuration
│   ├── orchestrator.mdc              # Orchestrator agent
│   ├── *.mdc                          # Other agent configs
│   └── *.md                           # Agent documentation
│
├── 📁 tools/                          # Essential tools only
│   ├── 📁 discovery/                  # Discovery-specific tools
│   │   ├── run_enhanced_discovery.py # Enhanced discovery runner
│   │   ├── business_problem_analyzer.py # Problem analysis
│   │   ├── mega_opportunity_scan.py   # Opportunity scanning
│   │   └── intensive_opportunity_scan.py # Intensive scanning
│   └── 📁 deployment/                 # Deployment tools
│       ├── start_server.py            # Simple server starter
│       ├── check_env.py               # Environment validation
│       └── complete_rehydration.py    # System rehydration
│
├── 📁 data/                           # Data storage
│   ├── 📁 backups/                    # Database backups
│   └── 📁 logs/                       # Essential logs only
│
├── 📁 docs/                           # Essential documentation
│   ├── 📁 architecture/               # System architecture
│   ├── 📁 deployment/                 # Deployment guides
│   └── 📁 reports/                    # System reports
│
├── 📁 backups/                        # System backups
├── 📁 .vscode/                        # VS Code configuration
├── 📁 .cursor/                        # Cursor configuration
│
├── 📄 luciq_discovery.db           # Single source of truth database
├── 📄 fix_database.py                 # Database management utility
├── 📄 migrate_discovery_data.py       # Data migration utility
│
├── 📄 README.md                       # Project documentation
├── 📄 PRD.md                          # Product requirements
├── 📄 ROADMAP_V2.md                   # V2 roadmap
├── 📄 .cursorrules                    # Cursor rules
├── 📄 cursor-user-rules.md            # User rules
│
└── 📄 AGENT_ACTIVATION_GUIDE.md       # Agent activation guide
```

## 🎯 **V2 Architecture Principles**

### **Single Purpose Focus**
- **Discovery Engine Only**: Reddit scraping + LLM analysis + idea management
- **No Analytics**: Zero revenue tracking, A/B testing, or performance monitoring
- **No Admin Panel**: Simple user authentication and idea management only

### **Clean API Structure**
- **Single API**: `apps/src/api/main.py` on port 8001
- **Discovery Endpoints**: `/api/discover`, `/api/save-idea`, `/api/my-ideas`
- **System Ideas**: `/api/system-ideas` for pre-generated opportunities
- **Authentication**: Simple JWT-based auth for user sessions

### **Consolidated Agents**
- **Core Agents**: 5 essential agents for discovery workflow
- **No Duplication**: Single `opportunity_ranker_fixed.py` implementation
- **Memory Integration**: All agents use unified memory system

### **Essential Tools Only**
- **Discovery Tools**: Business analysis and opportunity scanning
- **Deployment Tools**: Simple server management and environment checks
- **No Monitoring**: Removed all analytics and performance monitoring scripts

### **Clean Frontend**
- **5 Core Pages**: Landing, auth, dashboard, discover, my-ideas
- **Essential Components**: Foundation + data-display + notifications only
- **Single JS File**: `main.js` with discovery functionality only

## 📊 **V2 Cleanup Impact**

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| **Files** | ~300 | ~180 | 40% |
| **Code Lines** | ~45,000 | ~20,000 | 56% |
| **Directories** | ~50 | ~25 | 50% |
| **Database Files** | 7 | 1 | 86% |
| **JavaScript Files** | 8 | 1 | 88% |
| **Python Scripts** | 35+ | 12 | 66% |

## ✅ **V2 Verification Checklist**

- [ ] Frontend serves on port 3000 with 5 core pages
- [ ] API serves on port 8001 with discovery endpoints
- [ ] Single database: `luciq_discovery.db`
- [ ] No analytics references in any file
- [ ] No A/B testing components
- [ ] No performance monitoring
- [ ] No admin panel functionality
- [ ] Agent system consolidated to 5 core agents
- [ ] Tools reduced to discovery and deployment only
- [ ] Documentation focused on discovery mission

## 🚀 **V2 Startup Commands**

```bash
# Frontend (from apps/frontend/)
python -m http.server 3000

# API (from apps/src/api/)
python main.py

# Discovery Tools (from tools/discovery/)
python run_enhanced_discovery.py
```

**Result**: Clean, focused, high-performance SaaS idea discovery engine with zero analytics bloat. 