@echo off
echo ========================================
echo    Luciq V2 Production Deployment
echo    Real-time SaaS Discovery Engine
echo ========================================
echo.

:: Set production environment variables
set LUCIQ_ENV=production
set LUCIQ_API_PORT=8001
set LUCIQ_FRONTEND_PORT=3000
set LUCIQ_LOG_LEVEL=INFO
set LUCIQ_DB_PATH=luciq_discovery.db

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

:: Function to check if port is available
echo [INFO] Checking system requirements...

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

:: Check required Python packages
echo [INFO] Verifying Python dependencies...
python -c "import fastapi, uvicorn, sqlite3, requests, praw" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Missing required Python packages
    echo Installing dependencies...
    pip install fastapi uvicorn sqlite3 requests praw python-multipart
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Check if ports are available
echo [INFO] Checking port availability...
netstat -an | find ":%LUCIQ_API_PORT%" >nul
if not errorlevel 1 (
    echo [WARNING] Port %LUCIQ_API_PORT% is already in use
    echo Attempting to kill existing processes...
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":%LUCIQ_API_PORT%"') do taskkill /PID %%a /F >nul 2>&1
)

netstat -an | find ":%LUCIQ_FRONTEND_PORT%" >nul
if not errorlevel 1 (
    echo [WARNING] Port %LUCIQ_FRONTEND_PORT% is already in use
    echo Attempting to kill existing processes...
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":%LUCIQ_FRONTEND_PORT%"') do taskkill /PID %%a /F >nul 2>&1
)

:: Initialize database if needed
echo [INFO] Initializing database...
if not exist "%LUCIQ_DB_PATH%" (
    echo [INFO] Creating new database...
    python -c "
import sqlite3
import json
from datetime import datetime

# Create database and tables
conn = sqlite3.connect('%LUCIQ_DB_PATH%')
cursor = conn.cursor()

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Saved ideas table
cursor.execute('''
CREATE TABLE IF NOT EXISTS saved_ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    idea_title TEXT NOT NULL,
    idea_description TEXT,
    pain_point_source TEXT,
    market_potential TEXT,
    concept_data TEXT,
    system_generated BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Discovery sessions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS discovery_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subreddit TEXT,
    posts_analyzed INTEGER,
    pain_points_found INTEGER,
    session_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Insert sample system ideas
system_ideas = [
    ('AI-Powered Invoice Processing', 'Automated invoice extraction and processing using OCR and machine learning', 'Reddit r/entrepreneur', 'high', 1),
    ('Social Media Scheduler for SMBs', 'Simple social media scheduling tool designed specifically for small businesses', 'Reddit r/smallbusiness', 'high', 1),
    ('Customer Support Chatbot Builder', 'No-code platform for building intelligent customer support chatbots', 'Reddit r/SaaS', 'medium', 1),
    ('Project Time Tracking Tool', 'Intuitive time tracking and project management for freelancers and agencies', 'Reddit r/freelance', 'high', 1),
    ('Email Marketing Automation', 'Simplified email marketing automation for e-commerce businesses', 'Reddit r/ecommerce', 'medium', 1),
    ('Inventory Management System', 'Cloud-based inventory management for small retail businesses', 'Reddit r/retailbusiness', 'high', 1),
    ('Lead Generation Dashboard', 'Comprehensive lead tracking and nurturing platform for B2B sales teams', 'Reddit r/sales', 'high', 1),
    ('Content Calendar Planner', 'Editorial calendar and content planning tool for marketing teams', 'Reddit r/marketing', 'medium', 1),
    ('Employee Onboarding Platform', 'Streamlined digital onboarding process for HR departments', 'Reddit r/humanresources', 'medium', 1),
    ('Expense Tracking App', 'Smart expense tracking and reporting for small business owners', 'Reddit r/accounting', 'high', 1)
]

for title, desc, source, potential, system_gen in system_ideas:
    cursor.execute('''
    INSERT INTO saved_ideas (idea_title, idea_description, pain_point_source, market_potential, system_generated)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, desc, source, potential, system_gen))

conn.commit()
conn.close()
print('[INFO] Database initialized successfully')
"
    if errorlevel 1 (
        echo [ERROR] Failed to initialize database
        pause
        exit /b 1
    )
) else (
    echo [INFO] Database already exists
)

echo.
echo [INFO] Starting Luciq V2 Production Services...
echo.

:: Start API Server
echo [INFO] Starting Discovery API Server on port %LUCIQ_API_PORT%...
cd apps\src\api
start "Luciq API Server" cmd /k "echo Luciq Discovery API Server && echo Port: %LUCIQ_API_PORT% && echo Logs: ../../../logs/api.log && python -m uvicorn main:app --host 0.0.0.0 --port %LUCIQ_API_PORT% --log-level %LUCIQ_LOG_LEVEL% > ../../../logs/api.log 2>&1"

:: Wait for API to start
echo [INFO] Waiting for API server to initialize...
timeout /t 5 /nobreak >nul

:: Test API health
python -c "
import requests
import time
for i in range(10):
    try:
        response = requests.get('http://localhost:%LUCIQ_API_PORT%/')
        if response.status_code == 200:
            print('[SUCCESS] API server is responding')
            break
    except:
        pass
    time.sleep(1)
else:
    print('[ERROR] API server failed to start')
    exit(1)
"
if errorlevel 1 (
    echo [ERROR] API server health check failed
    pause
    exit /b 1
)

cd ..\..\..

:: Start Real-time Monitoring Service
echo [INFO] Starting Real-time Trend Monitoring Service...
cd tools\discovery
start "Luciq Monitor" cmd /k "echo Luciq Real-time Monitor && echo Interval: 15 minutes && echo Logs: ../../logs/monitor.log && python realtime_monitor.py > ../../logs/monitor.log 2>&1"
cd ..\..

:: Start Frontend Server
echo [INFO] Starting Frontend Server on port %LUCIQ_FRONTEND_PORT%...
cd apps\frontend
start "Luciq Frontend" cmd /k "echo Luciq Frontend Server && echo Port: %LUCIQ_FRONTEND_PORT% && echo URL: http://localhost:%LUCIQ_FRONTEND_PORT% && python -m http.server %LUCIQ_FRONTEND_PORT% > ../../logs/frontend.log 2>&1"
cd ..\..

:: Wait for frontend to start
echo [INFO] Waiting for frontend server to initialize...
timeout /t 3 /nobreak >nul

:: Test frontend health
python -c "
import requests
import time
for i in range(5):
    try:
        response = requests.get('http://localhost:%LUCIQ_FRONTEND_PORT%/')
        if response.status_code == 200:
            print('[SUCCESS] Frontend server is responding')
            break
    except:
        pass
    time.sleep(1)
else:
    print('[ERROR] Frontend server failed to start')
    exit(1)
"
if errorlevel 1 (
    echo [ERROR] Frontend server health check failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo     Luciq V2 Successfully Deployed!
echo ========================================
echo.
echo 🚀 System Status: OPERATIONAL
echo.
echo 📊 Services Running:
echo   • Discovery API:     http://localhost:%LUCIQ_API_PORT%
echo   • Frontend App:      http://localhost:%LUCIQ_FRONTEND_PORT%
echo   • Trend Monitor:     Background Service (15min intervals)
echo.
echo 📁 Access Points:
echo   • Landing Page:      http://localhost:%LUCIQ_FRONTEND_PORT%/pages/index.html
echo   • Discovery Tool:    http://localhost:%LUCIQ_FRONTEND_PORT%/pages/discover.html
echo   • Live Trends:       http://localhost:%LUCIQ_FRONTEND_PORT%/pages/trends.html
echo   • API Health:        http://localhost:%LUCIQ_API_PORT%/
echo.
echo 📋 Log Files:
echo   • API Logs:          logs\api.log
echo   • Monitor Logs:      logs\monitor.log
echo   • Frontend Logs:     logs\frontend.log
echo.
echo 🔧 Management:
echo   • Stop Services:     Close the terminal windows
echo   • View Logs:         Check logs\ directory
echo   • Restart:           Run this script again
echo.
echo Press any key to open the application in your browser...
pause >nul

:: Open application in default browser
start http://localhost:%LUCIQ_FRONTEND_PORT%/pages/index.html

echo.
echo Luciq V2 is now running in production mode!
echo Keep this window open to monitor the deployment.
echo.
pause 