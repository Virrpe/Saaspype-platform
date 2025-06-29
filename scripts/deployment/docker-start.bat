@echo off
setlocal enabledelayedexpansion

REM Luciq Docker Deployment Script v2.1
REM Optimized for Windows environment with error handling

echo ========================================
echo    Luciq V2.1 Docker Deployment
echo    Revolutionary Discovery Engine
echo ========================================

echo.
echo [INFO] Checking Docker availability...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not running
    echo [INFO] Please install Docker Desktop and ensure it's running
    pause
    exit /b 1
)

echo [INFO] Checking Docker Compose availability...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not available
    echo [INFO] Please ensure Docker Compose is installed
    pause
    exit /b 1
)

echo [INFO] Docker environment verified successfully
echo.

echo [INFO] Stopping any existing containers...
docker-compose down --remove-orphans

echo.
echo [INFO] Building Luciq Docker images...
docker-compose build --no-cache luciq-api

if %errorlevel% neq 0 (
    echo [ERROR] Docker build failed
    echo [INFO] Check the build logs above for errors
    pause
    exit /b 1
)

echo.
echo [INFO] Starting Luciq services...
echo [INFO] - API Server (Port 8000)
echo [INFO] - Frontend (Port 3000) 
echo [INFO] - Redis Cache (Port 6379)

docker-compose up -d luciq-api luciq-frontend redis

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start containers
    echo [INFO] Check Docker logs for details
    pause
    exit /b 1
)

echo.
echo [INFO] Waiting for services to initialize...
timeout /t 15 /nobreak >nul

echo.
echo [INFO] Checking service health...
docker-compose ps

echo.
echo ========================================
echo    Luciq V2.1 DOCKER DEPLOYMENT
echo ========================================
echo.
echo ✅ API Server:      http://localhost:8000
echo ✅ API Docs:       http://localhost:8000/docs
echo ✅ Health Check:   http://localhost:8000/health
echo ✅ Frontend:       http://localhost:3000
echo ✅ Production UI:  http://localhost:3000/pages/production-validation-testing.html
echo.
echo 📊 Optional Services:
echo    Monitoring:     docker-compose --profile monitoring up -d
echo    PostgreSQL:     docker-compose --profile production up -d postgres
echo.
echo 🔍 Management Commands:
echo    View Logs:      docker-compose logs -f luciq-api
echo    Stop Services:  docker-compose down
echo    Restart:        docker-compose restart
echo.
echo [SUCCESS] Luciq Docker deployment complete!
echo.

REM Open browser windows
echo [INFO] Opening browser windows...
start "" "http://localhost:8000/health"
timeout /t 2 /nobreak >nul
start "" "http://localhost:3000"

echo [INFO] Services are running in background
echo [INFO] Press any key to view live logs (CTRL+C to exit logs)
pause >nul

echo.
echo [INFO] Showing live API logs (Press CTRL+C to exit)...
docker-compose logs -f luciq-api

REM Configuration
set PROJECT_NAME=luciq
set HEALTH_CHECK_TIMEOUT=120
set MONITORING_ENABLED=false

REM Parse command line arguments
:parse_args
if "%1"=="--monitoring" (
    set MONITORING_ENABLED=true
    shift
    goto parse_args
)
if "%1"=="--help" (
    echo Usage: %0 [--monitoring] [--help]
    echo   --monitoring  Enable Prometheus and Grafana monitoring
    echo   --help        Show this help message
    exit /b 0
)
if not "%1"=="" (
    echo Unknown option %1
    exit /b 1
)

REM Function to check if Docker is running
echo [INFO] Checking Docker installation...

docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker and try again.
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker daemon is not running. Please start Docker and try again.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose and try again.
    pause
    exit /b 1
)

echo [SUCCESS] Docker and Docker Compose are ready

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "working-memory" mkdir "working-memory"
if not exist "monitoring\prometheus" mkdir "monitoring\prometheus"
if not exist "monitoring\grafana\dashboards" mkdir "monitoring\grafana\dashboards"
if not exist "monitoring\grafana\datasources" mkdir "monitoring\grafana\datasources"

echo [SUCCESS] Directories created successfully

REM Create monitoring configuration if enabled
if "%MONITORING_ENABLED%"=="true" (
    echo [INFO] Creating monitoring configuration...
    
    REM Create Prometheus config
    (
        echo global:
        echo   scrape_interval: 15s
        echo   evaluation_interval: 15s
        echo.
        echo scrape_configs:
        echo   - job_name: 'luciq-api'
        echo     static_configs:
        echo       - targets: ['luciq-api:8000']
        echo     metrics_path: '/metrics'
        echo     scrape_interval: 30s
        echo.
        echo   - job_name: 'prometheus'
        echo     static_configs:
        echo       - targets: ['localhost:9090']
    ) > monitoring\prometheus.yml
    
    REM Create Grafana datasource config
    (
        echo apiVersion: 1
        echo.
        echo datasources:
        echo   - name: Prometheus
        echo     type: prometheus
        echo     access: proxy
        echo     url: http://prometheus:9090
        echo     isDefault: true
    ) > monitoring\grafana\datasources\prometheus.yml
    
    echo [SUCCESS] Monitoring configuration created
)

REM Wait for services to be healthy
echo [INFO] Waiting for services to become healthy...

set /a elapsed=0
set /a interval=5

:health_check_loop
if %elapsed% geq %HEALTH_CHECK_TIMEOUT% (
    echo [ERROR] Services failed to become healthy within %HEALTH_CHECK_TIMEOUT% seconds
    echo [INFO] Checking service logs...
    docker-compose -p %PROJECT_NAME% logs --tail=20
    pause
    exit /b 1
)

REM Check API health
curl -f http://localhost:8000/health >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] API service is healthy
    goto health_check_done
)

echo [INFO] Waiting for services... (%elapsed%s/%HEALTH_CHECK_TIMEOUT%s)
timeout /t %interval% /nobreak >nul
set /a elapsed=%elapsed%+%interval%
goto health_check_loop

:health_check_done

REM Check frontend
curl -f http://localhost:3000 >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Frontend service is healthy
) else (
    echo [WARNING] Frontend service may not be fully ready
)

REM Display service status
echo [INFO] Service Status:
echo.
docker-compose -p %PROJECT_NAME% ps
echo.

echo [INFO] Service URLs:
echo 🌐 Frontend:        http://localhost:3000
echo 🎯 Trends Page:     http://localhost:3000/pages/trends.html
echo 🚀 API:             http://localhost:8000
echo 📚 API Docs:        http://localhost:8000/docs
echo ❤️  Health Check:   http://localhost:8000/health
echo 📊 Metrics:         http://localhost:8000/metrics

if "%MONITORING_ENABLED%"=="true" (
    echo 📈 Prometheus:      http://localhost:9090
    echo 📊 Grafana:         http://localhost:3001 (admin/luciq2025)
)

echo.
echo [SUCCESS] Luciq Discovery Engine 2.0 is running!
echo.

echo [INFO] Deployment complete!
echo.
echo To view logs: docker-compose -p %PROJECT_NAME% logs -f
echo To stop services: docker-compose -p %PROJECT_NAME% down
echo.

REM Open the application
set /p open_app="Would you like to open the application in your browser? (y/N): "
if /i "%open_app%"=="y" (
    start http://localhost:3000/pages/trends.html
)

REM Ask about viewing logs
set /p view_logs="Would you like to view logs now? (y/N): "
if /i "%view_logs%"=="y" (
    docker-compose -p %PROJECT_NAME% logs --tail=10 --follow
)

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
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo Luciq Quality Dashboard is starting!
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
echo Press any key to view logs...
pause > nul

echo.
echo Showing live logs (Ctrl+C to exit):
docker-compose logs -f luciq-api

pause 