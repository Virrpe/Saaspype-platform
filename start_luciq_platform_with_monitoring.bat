@echo off
setlocal enabledelayedexpansion

REM ====================================================================
REM Luciq Master Platform Startup Script v3.1 - Enhanced with Monitoring
REM Professional Business Intelligence Platform
REM Backend: Luciq Master API (Port 8000)
REM Frontend: SvelteKit + Tailwind CSS (Port 5173)
REM Monitor: Real-time error tracking and logging
REM ====================================================================

echo.
echo ==============================================================
echo    🚀 LUCIQ MASTER PLATFORM STARTUP v3.1 (WITH MONITORING)
echo ==============================================================
echo    Professional Business Intelligence Platform
echo    Backend: Luciq Master API (Port 8000)
echo    Frontend: SvelteKit + Tailwind CSS (Port 5173) 
echo    Monitor: Real-time development tracking
echo ==============================================================
echo.

REM Step 1: System Requirements Check
echo [1/7] 🔍 Checking system requirements...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ and try again
    pause
    exit /b 1
)

echo ✅ Python and Node.js are available

REM Step 2: File Structure Validation
echo [2/7] 📁 Validating file structure...

if not exist "master_luciq_api.py" (
    echo ❌ ERROR: Backend API file not found
    echo Expected: master_luciq_api.py
    pause
    exit /b 1
)

if not exist "src\frontend\package.json" (
    echo ❌ ERROR: Frontend package.json not found  
    echo Expected: src\frontend\package.json
    pause
    exit /b 1
)

if not exist "frontend-monitor.js" (
    echo ❌ ERROR: Frontend monitor script not found
    echo Expected: frontend-monitor.js
    pause
    exit /b 1
)

echo ✅ All required files found

REM Step 3: Port Cleanup
echo [3/7] 🧹 Cleaning up existing processes...

for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Killing process on port 8000: %%a
    taskkill /f /pid %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING"') do (
    echo Killing process on port 5173: %%a  
    taskkill /f /pid %%a >nul 2>&1
)

echo ✅ Ports 8000 and 5173 are ready

REM Step 4: Backend Dependency Check
echo [4/7] 📦 Checking backend dependencies...

python -c "import fastapi, uvicorn" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Installing backend dependencies...
    pip install fastapi uvicorn python-multipart
    if !errorlevel! neq 0 (
        echo ❌ ERROR: Failed to install backend dependencies
        pause
        exit /b 1
    )
)

echo ✅ Backend dependencies ready

REM Step 5: Frontend Dependency Check
echo [5/7] 🎨 Checking frontend dependencies...

cd src\frontend
if not exist "node_modules" (
    echo ⚠️  Installing frontend dependencies...
    npm install
    if !errorlevel! neq 0 (
        echo ❌ ERROR: Failed to install frontend dependencies
        cd ..\..
        pause
        exit /b 1
    )
)

echo ✅ Frontend dependencies ready
cd ..\..

REM Step 6: Start Backend Server
echo [6/7] 🛡️  Starting Luciq Master API...

echo Starting backend server on port 8000...
start "Luciq Master API" cmd /k "python master_luciq_api.py"

echo Waiting for backend initialization...
timeout /t 5 /nobreak >nul

REM Verify backend is running
curl -f http://localhost:8000/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Backend might still be starting... continuing anyway
) else (
    echo ✅ Backend API is responding
)

REM Step 7: Start Frontend with Monitoring
echo [7/7] 📱 Starting Frontend with Real-time Monitor...

echo Starting frontend monitor and development server...
start "Luciq Frontend Monitor" cmd /k "node frontend-monitor.js"

timeout /t 3 /nobreak >nul

REM Step 8: Open in Browser
echo 🌐 Opening application in browser...

timeout /t 8 /nobreak >nul
start "" "http://localhost:8000/api/health"
timeout /t 2 /nobreak >nul  
start "" "http://localhost:5173"

REM Final Status
echo.
echo ==============================================================
echo ✅ LUCIQ PLATFORM STARTUP COMPLETE
echo ==============================================================
echo 🛡️  Backend API: http://localhost:8000 (Luciq Master API v3.0)
echo 📱 Frontend UI: http://localhost:5173 (SvelteKit + Tailwind)
echo 📊 Monitor: Real-time tracking active (frontend-monitor.log)
echo.
echo 📋 Available Services:
echo    • Health Check: http://localhost:8000/api/health
echo    • Chat Service: http://localhost:8000/api/chat/message
echo    • Intelligence: http://localhost:8000/api/intelligence/*
echo    • Authentication: http://localhost:8000/api/auth/*
echo    • System Stats: http://localhost:8000/api/system/stats
echo.
echo 📝 Monitoring Features:
echo    • Real-time error detection and categorization
echo    • Dependency validation and suggestions
echo    • Performance tracking and uptime monitoring
echo    • Detailed logging to frontend-monitor.log
echo    • Automatic issue resolution suggestions
echo.
echo 🎯 Ready for Development and Testing!
echo.
echo Press Ctrl+C in any terminal to stop services
echo Monitor logs are saved to frontend-monitor.log
echo ==============================================================

pause 