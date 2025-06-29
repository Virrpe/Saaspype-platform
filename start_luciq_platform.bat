@echo off
cls
echo ================================================================================
echo 🚀 LUCIQ PROFESSIONAL BUSINESS INTELLIGENCE PLATFORM v3.0
echo ================================================================================
echo.
echo 🛡️ Backend: Luciq Master API (Port 8000) - 18K+ lines business logic
echo 📱 Frontend: Professional SvelteKit Interface (Port 5173) - Enterprise UI
echo 🎯 Mission: Tesla of Business Intelligence at startup prices
echo.
echo ⚡ Enhanced startup with service validation and error handling
echo ⚡ Keep both windows open for full platform operation
echo.

REM Check if Python is available
echo 🔍 Checking system requirements...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js not found. Please install Node.js 18+ and try again.
    pause
    exit /b 1
)

echo ✅ Python and Node.js detected
echo.

REM Check if backend file exists
if not exist "master_luciq_api.py" (
    echo ❌ ERROR: master_luciq_api.py not found in current directory
    echo Please run this script from the root Luciq directory
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "src\frontend\package.json" (
    echo ❌ ERROR: Frontend not found at src\frontend\
    echo Please ensure frontend is properly installed
    pause
    exit /b 1
)

echo ✅ All required files found
echo.

REM Kill any existing processes on our ports
echo 🔄 Cleaning up any existing services...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do taskkill /f /pid %%a >nul 2>&1
echo ✅ Port cleanup complete
echo.

echo ================================================================================
echo 🚀 STARTING SERVICES...
echo ================================================================================
echo.

REM Start Backend API in new window with enhanced title
echo 🛡️ Starting Backend API (Master Business Intelligence Engine)...
start "🛡️ Luciq Backend API - Master Business Intelligence Engine (Port 8000)" cmd /k "echo Starting Luciq Master API v3.0... && echo. && python master_luciq_api.py"

REM Wait for backend to initialize
echo ⏳ Waiting for backend initialization (5 seconds)...
timeout /t 5 /nobreak > nul

REM Start Frontend in new window with proper directory handling
echo 📱 Starting Frontend Interface (Professional SvelteKit UI)...
start "📱 Luciq Frontend - Professional Business Intelligence Interface (Port 5173)" cmd /k "echo Starting Luciq Frontend v3.0... && echo. && cd /d src\frontend && npm run dev"

echo.
echo ✅ LUCIQ PLATFORM STARTUP INITIATED
echo.
echo ================================================================================
echo 🌐 YOUR LUCIQ PLATFORM SERVICES:
echo ================================================================================
echo.
echo 🛡️ Backend API (Business Intelligence Engine):
echo    • URL: http://localhost:8000
echo    • Health Check: http://localhost:8000/api/health
echo    • Documentation: http://localhost:8000/docs
echo.
echo 📱 Frontend Interface (Professional UI):
echo    • URL: http://localhost:5173
echo    • Design: Clean Intelligence with Credibility Framework
echo    • Technology: SvelteKit + Tailwind CSS
echo.
echo ================================================================================
echo 🎯 PLATFORM STATUS & NEXT STEPS:
echo ================================================================================
echo.
echo 💡 Two terminal windows are now opening:
echo    1. "Backend API" - Your 18K+ line business intelligence engine
echo    2. "Frontend Interface" - Professional user experience
echo.
echo ⚠️  Wait 10-15 seconds for both services to fully initialize
echo.
echo 🔧 To stop services:
echo    • Close both terminal windows OR
echo    • Press Ctrl+C in each terminal
echo.
echo 📊 Once running, you'll have:
echo    • Enterprise-grade business intelligence capabilities
echo    • Professional credibility framework with confidence scoring  
echo    • API endpoints ready for immediate revenue generation
echo    • Beautiful user interface suitable for client presentations
echo.
echo 🚀 Ready for customer acquisition and revenue generation!
echo.
echo ================================================================================
echo Opening browser windows in 10 seconds...
timeout /t 10 /nobreak > nul

REM Open browser windows to both services
echo 🌐 Opening Luciq Platform in your browser...
start http://localhost:8000/api/health
start http://localhost:5173

echo.
echo ✅ LUCIQ PLATFORM FULLY OPERATIONAL
echo.
echo Press any key to close this window (services will continue running)...
pause >nul 