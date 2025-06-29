#!/bin/bash

# Luciq Container Startup Script
# Comprehensive Docker deployment for enterprise intelligence platform

set -e

echo "🚀 Luciq Enterprise Container Deployment"
echo "============================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    print_error "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

print_status "Docker environment verified ✅"

# Parse command line arguments
PROFILE="development"
DETACHED=false
BUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --production)
            PROFILE="production"
            shift
            ;;
        --monitoring)
            PROFILE="monitoring"
            shift
            ;;
        --detached|-d)
            DETACHED=true
            shift
            ;;
        --build)
            BUILD=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --production     Start with production profile (includes PostgreSQL, Nginx)"
            echo "  --monitoring     Start with monitoring profile (includes Prometheus, Grafana)"
            echo "  --detached, -d   Run containers in detached mode"
            echo "  --build          Force rebuild of containers"
            echo "  --help, -h       Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Start development environment"
            echo "  $0 --production --detached   # Start production environment in background"
            echo "  $0 --monitoring --build      # Start with monitoring and rebuild containers"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

print_status "Starting Luciq with profile: $PROFILE"

# Prepare environment
print_status "Preparing environment..."

# Create necessary directories
mkdir -p logs data/logs data/backups working-memory/current config/nginx/ssl

# Set proper permissions
chmod -R 755 logs data working-memory

# Build containers if requested
if [ "$BUILD" = true ]; then
    print_status "Building containers..."
    if [ "$PROFILE" = "production" ]; then
        docker-compose --profile production build
    elif [ "$PROFILE" = "monitoring" ]; then
        docker-compose --profile monitoring build
    else
        docker-compose build
    fi
    print_success "Containers built successfully"
fi

# Start containers based on profile
print_status "Starting containers..."

COMPOSE_CMD="docker-compose"

if [ "$PROFILE" = "production" ]; then
    COMPOSE_CMD="$COMPOSE_CMD --profile production"
elif [ "$PROFILE" = "monitoring" ]; then
    COMPOSE_CMD="$COMPOSE_CMD --profile monitoring"
fi

if [ "$DETACHED" = true ]; then
    COMPOSE_CMD="$COMPOSE_CMD up -d"
else
    COMPOSE_CMD="$COMPOSE_CMD up"
fi

print_status "Executing: $COMPOSE_CMD"
eval $COMPOSE_CMD

if [ "$DETACHED" = true ]; then
    print_success "Luciq containers started in detached mode"
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check service health
    print_status "Checking service health..."
    
    # Check backend
    if curl -f http://localhost:8003/health > /dev/null 2>&1; then
        print_success "Backend API is healthy"
    else
        print_warning "Backend API health check failed"
    fi
    
    # Check frontend
    if curl -f http://localhost:3001/ > /dev/null 2>&1; then
        print_success "Frontend is healthy"
    else
        print_warning "Frontend health check failed"
    fi
    
    # Display access information
    echo ""
    echo "🎯 Luciq Enterprise Platform Access:"
    echo "============================================"
    echo "🌐 Frontend (Glassmorphism UI): http://localhost:3001"
    echo "🔧 Backend API:                 http://localhost:8003"
    echo "📚 API Documentation:           http://localhost:8003/docs"
    echo "❤️  Health Check:               http://localhost:8003/health"
    
    if [ "$PROFILE" = "production" ]; then
        echo "🌍 Production (Nginx):          http://localhost"
        echo "🗄️  PostgreSQL:                 localhost:5432"
    fi
    
    if [ "$PROFILE" = "monitoring" ]; then
        echo "📊 Prometheus:                  http://localhost:9090"
        echo "📈 Grafana:                     http://localhost:3002"
        echo "   └─ Username: admin"
        echo "   └─ Password: luciq2025enterprise"
    fi
    
    echo "🔄 Redis Cache:                 localhost:6379"
    echo ""
    echo "🛠️  Container Management:"
    echo "   └─ View logs: docker-compose logs -f"
    echo "   └─ Stop all: docker-compose down"
    echo "   └─ Restart: docker-compose restart"
    echo ""
    print_success "Luciq Enterprise Platform is ready! 🚀"
fi 