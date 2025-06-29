@echo off
echo 🤖 LUCIQ + CLAUDE SETUP
echo ================================
echo.

set /p CLAUDE_KEY="Enter your Claude API key: "

if "%CLAUDE_KEY%"=="" (
    echo ❌ No API key provided
    pause
    exit
)

echo ✅ Setting Claude API key...
set ANTHROPIC_API_KEY=%CLAUDE_KEY%

echo 🚀 Starting Luciq with Claude integration...
echo.
echo 💡 In another terminal, run: python live_cost_dashboard.py
echo    This will show real-time costs as you use Claude!
echo.

python master_luciq_api.py

pause 