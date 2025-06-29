# Luciq Frontend Startup Guide (Standardized)

## 🎯 **Correct Frontend Server Startup**

### **Current Directory Structure** (Post-Refactor)
```
luciq/
├── src/frontend/          ← CORRECT (current structure)
│   ├── index.html
│   ├── pages/
│   ├── components/
│   └── static/
└── apps/frontend/         ← ARCHIVED (pre-refactor structure)
```

### **PowerShell Commands (Windows)**
```powershell
# Method 1: Single command (PowerShell compatible)
cd src/frontend; python -m http.server 3000

# Method 2: Separate commands
cd src/frontend
python -m http.server 3000
```

### **Cross-Platform Commands**
```bash
# Unix/Linux/MacOS
cd src/frontend && python -m http.server 3000

# Windows PowerShell
cd src/frontend; python -m http.server 3000
```

## 🌐 **Access URLs**

- **Main Application**: http://localhost:3000/
- **Dashboard**: http://localhost:3000/pages/core/dashboard.html
- **Discovery Interface**: http://localhost:3000/pages/features/discover.html
- **Trends Analysis**: http://localhost:3000/pages/features/trends.html
- **My Ideas**: http://localhost:3000/pages/features/my-ideas.html
- **Quality Dashboard**: http://localhost:3000/pages/testing/quality-dashboard.html

## 🚨 **Common Mistakes to Avoid**

❌ **Wrong Directory**: `cd apps/frontend` (pre-refactor structure)
❌ **Wrong Port**: `python -m http.server 5000` (use 3000)
❌ **Wrong Syntax**: `&&` in PowerShell (use `;` instead)

✅ **Correct**: `cd src/frontend; python -m http.server 3000`

## 🎨 **Current Theme: PS2 Signal Console**

The frontend has been unified with PS2 Signal Console design:
- **Background**: Dark (#0a0a0f) with ambient pulse animations
- **Colors**: Cyan (#00ffff) and Magenta (#ff00ff)
- **Logo**: Waveform animations with breathing effects
- **Cards**: Glass effect with signal console styling
- **Navigation**: Unified across all pages

## 🔧 **Troubleshooting**

**Port Already in Use**:
```powershell
# Kill existing process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

**Path Not Found**:
```powershell
# Verify you're in the project root
pwd
# Should show: .../luciq

# List directories to confirm structure
ls
# Should show: src/, docs/, config/, etc.
```

## 📋 **Agent Instructions**

**For AI Agents/Specialists**:
1. **ALWAYS** use `src/frontend/` directory
2. **ALWAYS** use port 3000
3. **ALWAYS** use PowerShell-compatible syntax (`;` not `&&`)
4. **NEVER** reference `apps/frontend/` (archived structure)
5. **NEVER** use port 5000 or other ports

**Standard Command Template**:
```
cd src/frontend; python -m http.server 3000
```

---

**Last Updated**: 2025-01-15 (Post-Refactor Standardization)
**Status**: ✅ CURRENT AND STANDARDIZED 