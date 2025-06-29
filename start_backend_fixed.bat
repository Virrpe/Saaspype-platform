@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo 🚀 LUCIQ BACKEND STARTUP - CORS FIXED VERSION
echo ========================================================
echo.

REM Kill any existing Python processes
echo [1/4] 🧹 Cleaning up existing processes...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Find Python executable
echo [2/4] 🔍 Locating Python installation...

REM Try conda first
if exist "%USERPROFILE%\anaconda3\python.exe" (
    set PYTHON_PATH=%USERPROFILE%\anaconda3\python.exe
    echo ✅ Found Python: Anaconda installation
    goto :found_python
)

REM Try conda in default location
if exist "%USERPROFILE%\miniconda3\python.exe" (
    set PYTHON_PATH=%USERPROFILE%\miniconda3\python.exe
    echo ✅ Found Python: Miniconda installation
    goto :found_python
)

REM Try system Python
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_PATH=python
    echo ✅ Found Python: System installation
    goto :found_python
)

REM Try Python 3
where python3 >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_PATH=python3
    echo ✅ Found Python: Python3 installation
    goto :found_python
)

REM Try common installation paths
if exist "C:\Python39\python.exe" (
    set PYTHON_PATH=C:\Python39\python.exe
    echo ✅ Found Python: C:\Python39
    goto :found_python
)

if exist "C:\Python310\python.exe" (
    set PYTHON_PATH=C:\Python310\python.exe
    echo ✅ Found Python: C:\Python310
    goto :found_python
)

if exist "C:\Python311\python.exe" (
    set PYTHON_PATH=C:\Python311\python.exe
    echo ✅ Found Python: C:\Python311
    goto :found_python
)

echo ❌ ERROR: Python not found!
echo Please ensure Python is installed and try running:
echo    conda activate base
echo    python master_luciq_api.py
pause
exit /b 1

:found_python
echo Using Python: %PYTHON_PATH%

REM Validate Python works
echo [3/4] ✅ Testing Python installation...
"%PYTHON_PATH%" --version
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python installation is broken
    pause
    exit /b 1
)

REM Check if master API file exists
if not exist "master_luciq_api.py" (
    echo ❌ ERROR: master_luciq_api.py not found
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo ✅ Backend API file found

REM Start the backend with updated CORS configuration
echo [4/4] 🚀 Starting Luciq Master API with CORS fix...
echo.
echo CORS Origins will include: localhost:5173
echo Backend will start on: http://localhost:8000
echo.
echo ====== BACKEND CONSOLE OUTPUT ======

"%PYTHON_PATH%" master_luciq_api.py

echo.
echo ====== BACKEND STOPPED ======
pause 