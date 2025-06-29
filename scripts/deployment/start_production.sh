#!/bin/bash

echo "========================================"
echo "   Luciq V2 Production Deployment"
echo "   Real-time SaaS Discovery Engine"
echo "========================================"
echo

# Set production environment variables
export LUCIQ_ENV=production
export LUCIQ_API_PORT=8001
export LUCIQ_FRONTEND_PORT=3000
export LUCIQ_LOG_LEVEL=INFO
export LUCIQ_DB_PATH=luciq_discovery.db

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "[WARNING] Port $port is already in use"
        echo "Attempting to kill existing processes..."
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# Function to wait for service
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=10
    local attempt=1
    
    echo "[INFO] Waiting for $service_name to start..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo "[SUCCESS] $service_name is responding"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done
    
    echo "[ERROR] $service_name failed to start after $max_attempts attempts"
    return 1
}

echo "[INFO] Checking system requirements..."

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check required Python packages
echo "[INFO] Verifying Python dependencies..."
python3 -c "import fastapi, uvicorn, sqlite3, requests, praw" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] Missing required Python packages"
    echo "Installing dependencies..."
    pip3 install fastapi uvicorn requests praw python-multipart
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
fi

# Check port availability
echo "[INFO] Checking port availability..."
check_port $LUCIQ_API_PORT
check_port $LUCIQ_FRONTEND_PORT

# Initialize database if needed
echo "[INFO] Initializing database..."
if [ ! -f "$LUCIQ_DB_PATH" ]; then
    echo "[INFO] Creating new database..."
    python3 << 'EOF'
import sqlite3
import json
from datetime import datetime

# Create database and tables
conn = sqlite3.connect('luciq_discovery.db')
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
EOF
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to initialize database"
        exit 1
    fi
else
    echo "[INFO] Database already exists"
fi

echo
echo "[INFO] Starting Luciq V2 Production Services..."
echo

# Start API Server
echo "[INFO] Starting Discovery API Server on port $LUCIQ_API_PORT..."
cd apps/src/api
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port $LUCIQ_API_PORT --log-level $LUCIQ_LOG_LEVEL > ../../../logs/api.log 2>&1 &
API_PID=$!
echo $API_PID > ../../../logs/api.pid
cd ../../..

# Wait for API to start
sleep 5
if ! wait_for_service "http://localhost:$LUCIQ_API_PORT/" "API server"; then
    echo "[ERROR] API server health check failed"
    exit 1
fi

# Start Real-time Monitoring Service
echo "[INFO] Starting Real-time Trend Monitoring Service..."
cd tools/discovery
nohup python3 realtime_monitor.py > ../../logs/monitor.log 2>&1 &
MONITOR_PID=$!
echo $MONITOR_PID > ../../logs/monitor.pid
cd ../..

# Start Frontend Server
echo "[INFO] Starting Frontend Server on port $LUCIQ_FRONTEND_PORT..."
cd src/frontend
nohup python3 -m http.server $LUCIQ_FRONTEND_PORT > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../../logs/frontend.pid
cd ../..

# Wait for frontend to start
sleep 3
if ! wait_for_service "http://localhost:$LUCIQ_FRONTEND_PORT/" "Frontend server"; then
    echo "[ERROR] Frontend server health check failed"
    exit 1
fi

echo
echo "========================================"
echo "    Luciq V2 Successfully Deployed!"
echo "========================================"
echo
echo "🚀 System Status: OPERATIONAL"
echo
echo "📊 Services Running:"
echo "  • Discovery API:     http://localhost:$LUCIQ_API_PORT"
echo "  • Frontend App:      http://localhost:$LUCIQ_FRONTEND_PORT"
echo "  • Trend Monitor:     Background Service (15min intervals)"
echo
echo "📁 Access Points:"
echo "  • Landing Page:      http://localhost:$LUCIQ_FRONTEND_PORT/pages/index.html"
echo "  • Discovery Tool:    http://localhost:$LUCIQ_FRONTEND_PORT/pages/discover.html"
echo "  • Live Trends:       http://localhost:$LUCIQ_FRONTEND_PORT/pages/trends.html"
echo "  • API Health:        http://localhost:$LUCIQ_API_PORT/"
echo
echo "📋 Log Files:"
echo "  • API Logs:          logs/api.log"
echo "  • Monitor Logs:      logs/monitor.log"
echo "  • Frontend Logs:     logs/frontend.log"
echo
echo "📋 Process IDs:"
echo "  • API PID:           $API_PID (saved to logs/api.pid)"
echo "  • Monitor PID:       $MONITOR_PID (saved to logs/monitor.pid)"
echo "  • Frontend PID:      $FRONTEND_PID (saved to logs/frontend.pid)"
echo
echo "🔧 Management:"
echo "  • Stop Services:     ./stop_production.sh"
echo "  • View Logs:         tail -f logs/*.log"
echo "  • Restart:           ./stop_production.sh && ./start_production.sh"
echo
echo "Opening application in your browser..."

# Try to open in browser (works on macOS and some Linux distros)
if command -v open &> /dev/null; then
    open "http://localhost:$LUCIQ_FRONTEND_PORT/pages/index.html"
elif command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:$LUCIQ_FRONTEND_PORT/pages/index.html"
else
    echo "Please open http://localhost:$LUCIQ_FRONTEND_PORT/pages/index.html in your browser"
fi

echo
echo "Luciq V2 is now running in production mode!"
echo "Use './stop_production.sh' to stop all services."
echo 