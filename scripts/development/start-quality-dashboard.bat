@echo off
echo ========================================
echo Luciq Quality Dashboard - Docker Start
echo ========================================
echo.

echo Building and starting Luciq with Quality Dashboard...
echo.

REM Stop any existing containers
echo Stopping any existing containers...
docker-compose down

echo.
echo Building Docker image...
docker-compose build luciq-api

echo.
echo Starting services...
docker-compose up -d luciq-api luciq-frontend redis

echo.
echo Waiting for services to start...
timeout /t 15 /nobreak > nul

echo.
echo Checking service health...
curl -f http://localhost:8000/health > nul 2>&1
if %errorlevel% == 0 (
    echo ✅ API service is healthy
) else (
    echo ⚠️  API service may still be starting...
)

curl -f http://localhost:3000 > nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Frontend service is healthy
) else (
    echo ⚠️  Frontend service may still be starting...
)

echo.
echo ========================================
echo 🎉 Luciq Quality Dashboard is running!
echo ========================================
echo.
echo 🚀 API Server: http://localhost:8000
echo 📊 Quality Dashboard: http://localhost:3000/pages/quality-dashboard.html
echo 🏠 Main Dashboard: http://localhost:3000/pages/dashboard.html
echo 🔧 API Documentation: http://localhost:8000/docs
echo ❤️  Health Check: http://localhost:8000/health
echo 📈 Metrics: http://localhost:8000/metrics
echo.
echo 🔍 Quality API Endpoints:
echo    • http://localhost:8000/api/quality/metrics
echo    • http://localhost:8000/api/quality/trends
echo    • http://localhost:8000/api/quality/alerts
echo.
echo 📋 Container Status:
docker-compose ps
echo.
echo Press any key to view logs, or Ctrl+C to exit...
pause > nul

echo.
echo Showing live logs (Ctrl+C to exit):
docker-compose logs -f luciq-api 