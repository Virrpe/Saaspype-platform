# Emergency Refactor Execution Script

## 🚨 CRITICAL ARCHITECTURE REPAIR - Execution Guide

**Based on:** Dialectically verified code duplication and architectural schizophrenia  
**Plan:** `emergency-refactor-plan-v3.json`  
**Status:** READY FOR EXECUTION

---

## ⚡ QUICK START COMMANDS

```bash
# 1. BACKUP (CRITICAL - DO FIRST)
python scripts/development/create_emergency_backup.py

# 2. EXECUTE REFACTOR 
python scripts/development/execute_emergency_refactor.py

# 3. VALIDATE RESULTS
python scripts/development/validate_refactor.py
```

---

## 📋 DETAILED EXECUTION PHASES

### **PHASE 1: EMERGENCY BACKUP (15 min)**

**Commands:**
```bash
# Create timestamped backup
mkdir backups/emergency-refactor-$(date +%Y%m%d-%H%M%S)
cp -r src/ backups/emergency-refactor-$(date +%Y%m%d-%H%M%S)/
cp -r tests/ backups/emergency-refactor-$(date +%Y%m%d-%H%M%S)/

# Verify backup integrity
ls -la backups/emergency-refactor-*/src/api/services/
```

**Validation:**
- [ ] Backup directory created
- [ ] All source files copied
- [ ] Backup size matches original

---

### **PHASE 2: ELIMINATE DUPLICATES (30 min)**

**Critical Deletions:**
```bash
# Delete orphaned domain service duplicates
rm src/api/domains/auth/services/auth_service.py
rm src/api/domains/credibility/services/database_service.py  
rm src/api/domains/credibility/services/metrics_service.py
rm src/api/domains/discovery/services/ideas_service.py

# Remove backup files cluttering main.py area
rm src/api/main_refactored.py
rm src/api/main_original_backup.py
```

**Validation:**
```bash
# Verify no duplicates exist
find src/api -name "*_service.py" -type f | sort
```

**Expected Result:** Each service exists only once

---

### **PHASE 3: REORGANIZE BY DOMAIN (45 min)**

**Service Migrations:**

```bash
# Auth Domain
mv src/api/services/auth_service.py src/api/domains/auth/services/

# Discovery Domain  
mv src/api/services/discovery_service.py src/api/domains/discovery/services/
mv src/api/services/ideas_service.py src/api/domains/discovery/services/
mv src/api/services/reddit_api_client.py src/api/domains/discovery/services/

# Intelligence Domain
mv src/api/services/semantic_analysis_engine.py src/api/domains/intelligence/services/
mv src/api/services/temporal_pattern_engine.py src/api/domains/intelligence/services/
mv src/api/services/semantic_trend_integration.py src/api/domains/intelligence/services/
mv src/api/services/cross_platform_intelligence.py src/api/domains/intelligence/services/
mv src/api/services/market_intelligence_service.py src/api/domains/intelligence/services/
mv src/api/services/graph_trend_detector.py src/api/domains/intelligence/services/

# Streaming Domain
mv src/api/services/streaming_trend_pipeline.py src/api/domains/streaming/services/
mv src/api/services/websocket_broadcaster.py src/api/domains/streaming/services/
mv src/api/services/multimodal_fusion_engine.py src/api/domains/streaming/services/
mv src/api/services/signal_fusion_engine.py src/api/domains/streaming/services/
mv src/api/services/advanced_trend_analyzer.py src/api/domains/streaming/services/

# Credibility Domain
mv src/api/services/source_credibility_engine.py src/api/domains/credibility/services/
mv src/api/services/metrics_service.py src/api/domains/credibility/services/
mv src/api/services/database_service.py src/api/domains/credibility/services/
mv src/api/services/performance_monitor.py src/api/domains/credibility/services/
mv src/api/services/error_handler.py src/api/domains/credibility/services/
```

**Validation:**
```bash
# Check domain organization
for domain in auth discovery intelligence streaming credibility; do
  echo "=== $domain DOMAIN ==="
  ls src/api/domains/$domain/services/
done
```

---

### **PHASE 4: UPDATE ALL IMPORTS (60 min)**

**Critical Import Updates:**

**1. Main Application Files:**
```bash
# Update main.py
sed -i 's/from src.api.services.metrics_service/from src.api.domains.credibility.services.metrics_service/g' src/api/main.py
sed -i 's/from src.api.services.performance_monitor/from src.api.domains.credibility.services.performance_monitor/g' src/api/main.py
```

**2. Domain Routers:**
```bash
# Auth router
sed -i 's/from src.api.services.auth_service/from src.api.domains.auth.services.auth_service/g' src/api/endpoints/auth.py
sed -i 's/from src.api.services.auth_service/from src.api.domains.auth.services.auth_service/g' src/api/domains/auth/endpoints/auth.py

# Discovery router  
sed -i 's/from src.api.services.discovery_service/from src.api.domains.discovery.services.discovery_service/g' src/api/domains/discovery/endpoints/discovery_router.py
sed -i 's/from src.api.services.ideas_service/from src.api.domains.discovery.services.ideas_service/g' src/api/domains/discovery/endpoints/discovery_router.py
```

**3. Test Files (Critical):**
```bash
# Update all test imports
find tests/ -name "*.py" -exec sed -i 's/from src.api.services.auth_service/from src.api.domains.auth.services.auth_service/g' {} \;
find tests/ -name "*.py" -exec sed -i 's/from src.api.services.discovery_service/from src.api.domains.discovery.services.discovery_service/g' {} \;
find tests/ -name "*.py" -exec sed -i 's/from src.api.services.ideas_service/from src.api.domains.discovery.services.ideas_service/g' {} \;
```

**4. Service Internal Dependencies:**
```bash
# Update cross-service imports
grep -r "from src.api.services" src/api/domains/ | cut -d: -f1 | sort -u | while read file; do
  sed -i 's/from src.api.services.reddit_api_client/from src.api.domains.discovery.services.reddit_api_client/g' "$file"
done
```

**Validation:**
```bash
# Check for remaining old imports
grep -r "from src.api.services" src/ tests/ || echo "✅ All imports updated!"
```

---

### **PHASE 5: CREATE SERVICE INTERFACES (45 min)**

**Domain Service __init__.py Files:**

```python
# src/api/domains/auth/services/__init__.py
from .auth_service import auth_service

__all__ = ['auth_service']

# src/api/domains/discovery/services/__init__.py  
from .discovery_service import discovery_service
from .ideas_service import ideas_service
from .reddit_api_client import reddit_api_client

__all__ = ['discovery_service', 'ideas_service', 'reddit_api_client']

# src/api/domains/credibility/services/__init__.py
from .metrics_service import metrics_service
from .database_service import database_service
from .performance_monitor import performance_monitor

__all__ = ['metrics_service', 'database_service', 'performance_monitor']
```

**Validation:**
```bash
# Test clean imports
python -c "from src.api.domains.auth.services import auth_service; print('✅ Auth imports work')"
python -c "from src.api.domains.discovery.services import discovery_service; print('✅ Discovery imports work')"
```

---

### **PHASE 6: SPLIT MONOLITHIC SERVICES (90 min - OPTIONAL)**

**Target Large Files:**
- `trend_detection_service.py` (61KB → 3 files)
- `temporal_pattern_engine.py` (35KB → 3 files)  
- `semantic_analysis_engine.py` (31KB → 3 files)

**Strategy:** Create focused modules while maintaining backward compatibility

---

### **PHASE 7: COMPREHENSIVE VALIDATION (30 min)**

**Critical Tests:**
```bash
# 1. API Startup Test
python src/api/main.py &
PID=$!
sleep 5
curl http://localhost:8000/health
kill $PID

# 2. Import Validation
python -c "
import sys
sys.path.append('.')
try:
    from src.api.domains.auth.services import auth_service
    from src.api.domains.discovery.services import discovery_service
    from src.api.domains.credibility.services import metrics_service
    print('✅ All critical imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# 3. Run Test Suite
python -m pytest tests/ -v
```

---

## 🎯 SUCCESS CRITERIA CHECKLIST

**Immediate Validation:**
- [ ] No duplicate service files exist
- [ ] All imports use domain paths
- [ ] API starts without errors
- [ ] All tests pass
- [ ] Service count: ~22 files properly distributed

**Code Quality Metrics:**
- [ ] Duplicate lines eliminated: 1500+
- [ ] Service files <30KB each (except known large ones)
- [ ] Clear domain ownership established
- [ ] No orphaned files

**Functional Validation:**
- [ ] Authentication works: `/auth/login`
- [ ] Discovery works: `/api/discover` 
- [ ] Health check works: `/health`
- [ ] Metrics work: `/metrics`

---

## 🚨 ROLLBACK PROCEDURE

**If anything fails:**
```bash
# 1. Stop operations immediately
pkill -f "python src/api/main.py"

# 2. Restore from backup
BACKUP_DIR=$(ls -1d backups/emergency-refactor-* | tail -1)
rm -rf src/
cp -r $BACKUP_DIR/src/ .

# 3. Verify restoration
python src/api/main.py &
sleep 5
curl http://localhost:8000/health
pkill -f "python src/api/main.py"

echo "✅ Rollback complete"
```

---

## 📊 EXPECTED OUTCOME

**Before Refactor:**
- Duplicate services: 4 identical pairs
- Import confusion: Mixed domain/flat patterns
- Maintenance burden: Change 2+ files per bug fix
- Architecture: Schizophrenic

**After Refactor:**
- Single source of truth for all services
- Clean domain-driven imports
- Maintenance simplified: One file per service
- Architecture: Consistent domain-driven design

**Ready for Phase 6:** Clean foundation for advanced features

---

## 🔄 CONTINUOUS VALIDATION

**After each phase:**
```bash
# Quick health check
python -c "
import sys; sys.path.append('.')
from src.api.main import app
print('✅ Main app imports successfully')
"
```

**Final validation:**
```bash
# Complete system test
python scripts/development/run_integration_tests.py
```

This refactor will **eliminate the architectural schizophrenia** and create a **clean, maintainable foundation** for future development. 