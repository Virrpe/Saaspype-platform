#!/bin/bash

# Luciq Docker Setup Validation Script
# Validates Docker configuration and prerequisites

set -e

echo "🔍 Luciq Docker Setup Validation"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_check() {
    echo -e "${BLUE}[CHECK]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

VALIDATION_PASSED=true

# Check Docker installation
print_check "Checking Docker installation..."
if command -v docker > /dev/null 2>&1; then
    DOCKER_VERSION=$(docker --version)
    print_pass "Docker found: $DOCKER_VERSION"
else
    print_fail "Docker not found. Please install Docker Desktop."
    VALIDATION_PASSED=false
fi

# Check Docker Compose
print_check "Checking Docker Compose..."
if command -v docker-compose > /dev/null 2>&1; then
    COMPOSE_VERSION=$(docker-compose --version)
    print_pass "Docker Compose found: $COMPOSE_VERSION"
else
    print_fail "Docker Compose not found. Please install Docker Compose."
    VALIDATION_PASSED=false
fi

# Check Docker daemon
print_check "Checking Docker daemon..."
if docker info > /dev/null 2>&1; then
    print_pass "Docker daemon is running"
else
    print_fail "Docker daemon is not running. Please start Docker Desktop."
    VALIDATION_PASSED=false
fi

# Check required files
print_check "Checking required configuration files..."

required_files=(
    "docker-compose.yml"
    "Dockerfile.backend"
    "Dockerfile.frontend"
    ".dockerignore"
    "requirements.txt"
    "start_optimized_api.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_pass "Found: $file"
    else
        print_fail "Missing: $file"
        VALIDATION_PASSED=false
    fi
done

# Check SvelteKit frontend structure
print_check "Checking SvelteKit frontend structure..."
if [ -d "src/frontend/luciq-frontend" ]; then
    if [ -f "src/frontend/luciq-frontend/package.json" ]; then
        print_pass "SvelteKit frontend structure is valid"
    else
        print_fail "SvelteKit package.json not found"
        VALIDATION_PASSED=false
    fi
else
    print_fail "SvelteKit frontend directory not found"
    VALIDATION_PASSED=false
fi

# Check backend structure
print_check "Checking backend structure..."
if [ -d "src/api" ]; then
    if [ -f "src/api/main.py" ]; then
        print_pass "Backend API structure is valid"
    else
        print_fail "Backend main.py not found"
        VALIDATION_PASSED=false
    fi
else
    print_fail "Backend API directory not found"
    VALIDATION_PASSED=false
fi

# Check system resources
print_check "Checking system resources..."

# Check available memory (Linux/Mac)
if command -v free > /dev/null 2>&1; then
    MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    if [ "$MEMORY_GB" -ge 8 ]; then
        print_pass "Available memory: ${MEMORY_GB}GB (sufficient)"
    else
        print_warn "Available memory: ${MEMORY_GB}GB (8GB+ recommended)"
    fi
fi

# Check available disk space
DISK_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$DISK_SPACE" -ge 10 ]; then
    print_pass "Available disk space: ${DISK_SPACE}GB (sufficient)"
else
    print_warn "Available disk space: ${DISK_SPACE}GB (10GB+ recommended)"
fi

# Check port availability
print_check "Checking port availability..."

check_port() {
    local port=$1
    local service=$2
    
    if command -v netstat > /dev/null 2>&1; then
        if netstat -tuln | grep ":$port " > /dev/null; then
            print_warn "Port $port is in use (needed for $service)"
        else
            print_pass "Port $port is available for $service"
        fi
    elif command -v ss > /dev/null 2>&1; then
        if ss -tuln | grep ":$port " > /dev/null; then
            print_warn "Port $port is in use (needed for $service)"
        else
            print_pass "Port $port is available for $service"
        fi
    else
        print_warn "Cannot check port $port availability (netstat/ss not found)"
    fi
}

check_port 8003 "Backend API"
check_port 3001 "Frontend UI"
check_port 6379 "Redis Cache"
check_port 5432 "PostgreSQL (production)"
check_port 80 "Nginx (production)"
check_port 9090 "Prometheus (monitoring)"
check_port 3002 "Grafana (monitoring)"

# Validate Docker Compose configuration
print_check "Validating Docker Compose configuration..."
if docker-compose config > /dev/null 2>&1; then
    print_pass "Docker Compose configuration is valid"
else
    print_fail "Docker Compose configuration has errors"
    VALIDATION_PASSED=false
fi

# Check network connectivity
print_check "Checking network connectivity..."
if ping -c 1 google.com > /dev/null 2>&1; then
    print_pass "Internet connectivity available"
else
    print_warn "Internet connectivity check failed (may affect image downloads)"
fi

# Summary
echo ""
echo "🎯 Validation Summary"
echo "===================="

if [ "$VALIDATION_PASSED" = true ]; then
    print_pass "All critical checks passed! ✅"
    echo ""
    echo "🚀 Ready to deploy Luciq with Docker!"
    echo ""
    echo "Next steps:"
    echo "  1. Start development environment:"
    echo "     ./scripts/docker/start-containers.sh --detached"
    echo ""
    echo "  2. Start production environment:"
    echo "     ./scripts/docker/start-containers.sh --production --detached"
    echo ""
    echo "  3. Start with monitoring:"
    echo "     ./scripts/docker/start-containers.sh --monitoring --detached"
    echo ""
    exit 0
else
    print_fail "Some checks failed. Please resolve the issues above before deploying."
    echo ""
    echo "Common solutions:"
    echo "  - Install Docker Desktop: https://www.docker.com/products/docker-desktop"
    echo "  - Start Docker Desktop application"
    echo "  - Ensure sufficient system resources (8GB+ RAM, 10GB+ disk)"
    echo "  - Stop services using required ports"
    echo ""
    exit 1
fi 