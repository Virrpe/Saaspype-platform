#!/bin/bash

# Luciq Docker Deployment Script v2.1
# Optimized for Linux/Mac with comprehensive error handling

set -e  # Exit on any error

echo "========================================"
echo "   Luciq V2.1 Docker Deployment"
echo "   Revolutionary Discovery Engine"
echo "========================================"
echo

# Function for colored output
print_info() { echo -e "\e[34m[INFO]\e[0m $1"; }
print_success() { echo -e "\e[32m[SUCCESS]\e[0m $1"; }
print_error() { echo -e "\e[31m[ERROR]\e[0m $1"; }
print_warning() { echo -e "\e[33m[WARNING]\e[0m $1"; }

# Check Docker availability
print_info "Checking Docker availability..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    print_info "Please install Docker and try again"
    exit 1
fi

if ! docker info &> /dev/null; then
    print_error "Docker is not running"
    print_info "Please start Docker and try again"
    exit 1
fi

print_success "Docker is available and running"

# Check Docker Compose availability
print_info "Checking Docker Compose availability..."
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed"
    print_info "Please install Docker Compose and try again"
    exit 1
fi

print_success "Docker Compose is available"
echo

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p data logs working-memory monitoring/prometheus monitoring/grafana/dashboards monitoring/grafana/datasources
chmod 755 data logs working-memory

# Stop existing containers
print_info "Stopping any existing containers..."
docker-compose down --remove-orphans || true

# Build the application
print_info "Building Luciq Docker images..."
if ! docker-compose build --no-cache luciq-api; then
    print_error "Docker build failed"
    print_info "Check the build logs above for errors"
    exit 1
fi

print_success "Docker build completed successfully"
echo

# Start core services
print_info "Starting Luciq services..."
print_info "- API Server (Port 8000)"
print_info "- Frontend (Port 3000)"
print_info "- Redis Cache (Port 6379)"

if ! docker-compose up -d luciq-api luciq-frontend redis; then
    print_error "Failed to start containers"
    print_info "Check Docker logs for details"
    exit 1
fi

print_success "Services started successfully"
echo

# Wait for services to initialize
print_info "Waiting for services to initialize..."
sleep 15

# Check service health
print_info "Checking service health..."
docker-compose ps

echo
echo "========================================"
echo "   Luciq V2.1 DOCKER DEPLOYMENT"
echo "========================================"
echo
echo "✅ API Server:      http://localhost:8000"
echo "✅ API Docs:       http://localhost:8000/docs"  
echo "✅ Health Check:   http://localhost:8000/health"
echo "✅ Frontend:       http://localhost:3000"
echo "✅ Production UI:  http://localhost:3000/pages/production-validation-testing.html"
echo
echo "📊 Optional Services:"
echo "   Monitoring:     docker-compose --profile monitoring up -d"
echo "   PostgreSQL:     docker-compose --profile production up -d postgres"
echo
echo "🔍 Management Commands:"
echo "   View Logs:      docker-compose logs -f luciq-api"
echo "   Stop Services:  docker-compose down"
echo "   Restart:        docker-compose restart"
echo

print_success "Luciq Docker deployment complete!"
echo

# Test API health
print_info "Testing API health..."
if curl -f http://localhost:8000/health &> /dev/null; then
    print_success "API is responding correctly"
else
    print_warning "API health check failed - services may still be starting"
fi

# Offer to show logs
echo
print_info "Would you like to view live logs? (y/N)"
read -t 10 -r response || response="n"
if [[ $response =~ ^[Yy]$ ]]; then
    echo
    print_info "Showing live API logs (Press CTRL+C to exit)..."
    docker-compose logs -f luciq-api
else
    print_info "Services are running in background"
    print_info "Use 'docker-compose logs -f luciq-api' to view logs"
fi 