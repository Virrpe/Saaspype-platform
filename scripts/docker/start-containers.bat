@echo off
REM Luciq Container Startup Script - Windows Version
REM Comprehensive Docker deployment for enterprise intelligence platform

setlocal enabledelayedexpansion

echo 🚀 Luciq Enterprise Container Deployment
echo ============================================

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose and try again.
    pause
    exit /b 1
)

echo [INFO] Docker environment verified ✅

REM Parse command line arguments
set PROFILE=development
set DETACHED=false
set BUILD=false

:parse_args
if "%~1"=="" goto start_deployment
if "%~1"=="--production" (
    set PROFILE=production
    shift
    goto parse_args
)
if "%~1"=="--monitoring" (
    set PROFILE=monitoring
    shift
    goto parse_args
)
if "%~1"=="--detached" (
    set DETACHED=true
    shift
    goto parse_args
)
if "%~1"=="-d" (
    set DETACHED=true
    shift
    goto parse_args
)
if "%~1"=="--build" (
    set BUILD=true
    shift
    goto parse_args
)
if "%~1"=="--help" goto show_help
if "%~1"=="-h" goto show_help

echo [ERROR] Unknown option: %~1
echo Use --help for usage information
pause
exit /b 1

:show_help
echo Usage: %0 [OPTIONS]
echo.
echo Options:
echo   --production     Start with production profile (includes PostgreSQL, Nginx)
echo   --monitoring     Start with monitoring profile (includes Prometheus, Grafana)
echo   --detached, -d   Run containers in detached mode
echo   --build          Force rebuild of containers
echo   --help, -h       Show this help message
echo.
echo Examples:
echo   %0                           # Start development environment
echo   %0 --production --detached   # Start production environment in background
echo   %0 --monitoring --build      # Start with monitoring and rebuild containers
exit /b 0

:start_deployment
echo [INFO] Starting Luciq with profile: %PROFILE%

REM Prepare environment
echo [INFO] Preparing environment...

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "data\logs" mkdir data\logs
if not exist "data\backups" mkdir data\backups
if not exist "working-memory\current" mkdir working-memory\current
if not exist "config\nginx\ssl" mkdir config\nginx\ssl

REM Build containers if requested
if "%BUILD%"=="true" (
    echo [INFO] Building containers...
    if "%PROFILE%"=="production" (
        docker-compose --profile production build
    ) else if "%PROFILE%"=="monitoring" (
        docker-compose --profile monitoring build
    ) else (
        docker-compose build
    )
    if errorlevel 1 (
        echo [ERROR] Container build failed
        pause
        exit /b 1
    )
    echo [SUCCESS] Containers built successfully
)

REM Start containers based on profile
echo [INFO] Starting containers...

set COMPOSE_CMD=docker-compose

if "%PROFILE%"=="production" (
    set COMPOSE_CMD=!COMPOSE_CMD! --profile production
) else if "%PROFILE%"=="monitoring" (
    set COMPOSE_CMD=!COMPOSE_CMD! --profile monitoring
)

if "%DETACHED%"=="true" (
    set COMPOSE_CMD=!COMPOSE_CMD! up -d
) else (
    set COMPOSE_CMD=!COMPOSE_CMD! up
)

echo [INFO] Executing: !COMPOSE_CMD!
!COMPOSE_CMD!

if errorlevel 1 (
    echo [ERROR] Failed to start containers
    pause
    exit /b 1
)

if "%DETACHED%"=="true" (
    echo [SUCCESS] Luciq containers started in detached mode
    
    REM Wait for services to be ready
    echo [INFO] Waiting for services to be ready...
    timeout /t 10 /nobreak >nul
    
    REM Check service health
    echo [INFO] Checking service health...
    
    REM Check backend
    curl -f http://localhost:8003/health >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Backend API health check failed
    ) else (
        echo [SUCCESS] Backend API is healthy
    )
    
    REM Check frontend
    curl -f http://localhost:3001/ >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Frontend health check failed
    ) else (
        echo [SUCCESS] Frontend is healthy
    )
    
    REM Display access information
    echo.
    echo 🎯 Luciq Enterprise Platform Access:
    echo ============================================
    echo 🌐 Frontend (Glassmorphism UI): http://localhost:3001
    echo 🔧 Backend API:                 http://localhost:8003
    echo 📚 API Documentation:           http://localhost:8003/docs
    echo ❤️  Health Check:               http://localhost:8003/health
    
    if "%PROFILE%"=="production" (
        echo 🌍 Production (Nginx):          http://localhost
        echo 🗄️  PostgreSQL:                 localhost:5432
    )
    
    if "%PROFILE%"=="monitoring" (
        echo 📊 Prometheus:                  http://localhost:9090
        echo 📈 Grafana:                     http://localhost:3002
        echo    └─ Username: admin
        echo    └─ Password: luciq2025enterprise
    )
    
    echo 🔄 Redis Cache:                 localhost:6379
    echo.
    echo 🛠️  Container Management:
    echo    └─ View logs: docker-compose logs -f
    echo    └─ Stop all: docker-compose down
    echo    └─ Restart: docker-compose restart
    echo.
    echo [SUCCESS] Luciq Enterprise Platform is ready! 🚀
    
    REM Open browser to frontend
    start http://localhost:3001
)

pause 