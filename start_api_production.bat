@echo off
echo Starting Luciq Master API v3.0 - Production Mode
echo ================================================

REM Load environment variables from .env file
for /f "delims=" %%x in (.env) do (set "%%x")

REM Start API without auto-reload for stability
echo Starting API on port %API_PORT%...
python -m uvicorn master_luciq_api:app --host %API_HOST% --port %API_PORT%

pause 