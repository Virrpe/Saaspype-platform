@echo off
cls
echo ================================================================================
echo 📱 LUCIQ FRONTEND DEVELOPMENT SERVER
echo ================================================================================
echo.
echo 🎨 Starting Professional SvelteKit + Tailwind CSS Interface
echo 🛡️ Clear Intelligence Design with Credibility Framework
echo 🎯 Enterprise-grade UI for Business Intelligence Platform
echo.

REM Check if Node.js is available
echo 🔍 Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js not found. Please install Node.js 18+ and try again.
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "src\frontend\package.json" (
    echo ❌ ERROR: Frontend not found at src\frontend\
    echo Please ensure you're running from the root Luciq directory
    pause
    exit /b 1
)

echo ✅ Node.js detected and frontend found
echo.

REM Clean up any existing frontend process
echo 🔄 Cleaning up existing frontend process...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do taskkill /f /pid %%a >nul 2>&1
echo ✅ Port 5173 cleanup complete
echo.

echo ================================================================================
echo 🚀 STARTING FRONTEND DEVELOPMENT SERVER...
echo ================================================================================
echo.

REM Navigate to frontend directory and start dev server
cd /d src\frontend
echo 📁 Changed to frontend directory: %CD%
echo.
echo 🛠️ Installing/updating dependencies...
call npm install
echo.
echo 🎨 Starting SvelteKit development server...
echo.
echo ⚡ Frontend will be available at: http://localhost:5173
echo 🔧 Development mode with hot reload enabled
echo 💡 Press Ctrl+C to stop the server
echo.
echo ================================================================================

REM Start the development server
call npm run dev 