@echo off
echo ========================================
echo    Luciq Discovery Engine 2.0
echo    Starting API and Frontend Servers
echo ========================================

:: Kill any existing processes on our ports
echo [INFO] Cleaning up existing processes...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000"') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| find ":3000"') do taskkill /PID %%a /F >nul 2>&1

:: Start API Server
echo [INFO] Starting API Server on port 8000...
start "Luciq API" cmd /k "echo Luciq API Server - Port 8000 && python start_api_v2.py"

:: Wait a moment
timeout /t 5 /nobreak >nul

:: Start Frontend Server  
echo [INFO] Starting Frontend Server on port 3000...
start "Luciq Frontend" cmd /k "echo Luciq Frontend - Port 3000 && cd src/frontend && python -m http.server 3000"

:: Wait a moment
timeout /t 3 /nobreak >nul

echo.
echo [SUCCESS] Luciq Discovery Engine 2.0 is starting up!
echo.
echo API Server:      http://localhost:8000
echo Frontend:        http://localhost:3000/pages/trends.html
echo API Docs:        http://localhost:8000/docs
echo Health Check:    http://localhost:8000/health
echo.
echo Press any key to open the application...
pause >nul

:: Open the application
start http://localhost:3000/pages/trends.html

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
pause 