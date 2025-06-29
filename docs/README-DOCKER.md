# Luciq Docker Deployment Guide

🚀 **Enterprise-Grade Containerized Deployment for Luciq Intelligence Platform**

## 🎯 Overview

This Docker deployment provides a complete containerized solution for the Luciq enterprise intelligence platform, including:

- **Backend API**: FastAPI with 6 AI engines (port 8003)
- **Frontend UI**: SvelteKit with glassmorphism design (port 3001)
- **Redis Cache**: For real-time features and session management
- **PostgreSQL**: Production database (optional)
- **Nginx**: Reverse proxy for production (optional)
- **Monitoring**: Prometheus + Grafana (optional)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Luciq Container Stack                 │
├─────────────────────────────────────────────────────────────┤
│  Frontend (SvelteKit)     │  Backend (FastAPI)             │
│  Port: 3001               │  Port: 8003                    │
│  - Glassmorphism UI       │  - 6 AI Engines               │
│  - Real-time Dashboard    │  - Enterprise Intelligence    │
│  - Observable Plot Charts │  - WebSocket Support          │
├─────────────────────────────────────────────────────────────┤
│  Redis Cache              │  PostgreSQL (Production)      │
│  Port: 6379               │  Port: 5432                    │
│  - Session Management     │  - Persistent Data Storage    │
│  - Real-time Features     │  - Enterprise Scale           │
├─────────────────────────────────────────────────────────────┤
│  Nginx (Production)       │  Monitoring Stack             │
│  Port: 80/443             │  Prometheus: 9090, Grafana: 3002│
│  - Reverse Proxy          │  - Performance Metrics        │
│  - Load Balancing         │  - System Health Monitoring   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **8GB RAM** minimum (16GB recommended)
- **10GB free disk space**

### 1. Basic Development Environment

```bash
# Clone and navigate to project
cd luciq

# Start development environment
./scripts/docker/start-containers.sh --detached

# Or on Windows
scripts\docker\start-containers.bat --detached
```

**Access Points:**
- 🌐 **Frontend**: http://localhost:3001
- 🔧 **Backend API**: http://localhost:8003
- 📚 **API Docs**: http://localhost:8003/docs

### 2. Production Environment

```bash
# Start with production profile
./scripts/docker/start-containers.sh --production --detached

# Or on Windows
scripts\docker\start-containers.bat --production --detached
```

**Additional Services:**
- 🌍 **Production (Nginx)**: http://localhost
- 🗄️ **PostgreSQL**: localhost:5432

### 3. Full Monitoring Stack

```bash
# Start with monitoring
./scripts/docker/start-containers.sh --monitoring --detached

# Or on Windows
scripts\docker\start-containers.bat --monitoring --detached
```

**Monitoring Access:**
- 📊 **Prometheus**: http://localhost:9090
- 📈 **Grafana**: http://localhost:3002
  - Username: `admin`
  - Password: `luciq2025enterprise`

## 📋 Deployment Profiles

### Development Profile (Default)
- ✅ Backend API (FastAPI)
- ✅ Frontend UI (SvelteKit)
- ✅ Redis Cache
- ❌ PostgreSQL
- ❌ Nginx
- ❌ Monitoring

### Production Profile
- ✅ Backend API (FastAPI)
- ✅ Frontend UI (SvelteKit)
- ✅ Redis Cache
- ✅ PostgreSQL Database
- ✅ Nginx Reverse Proxy
- ❌ Monitoring

### Monitoring Profile
- ✅ Backend API (FastAPI)
- ✅ Frontend UI (SvelteKit)
- ✅ Redis Cache
- ✅ Prometheus Metrics
- ✅ Grafana Dashboard
- ❌ PostgreSQL
- ❌ Nginx

## 🛠️ Manual Docker Commands

### Build and Start

```bash
# Build all containers
docker-compose build

# Start development environment
docker-compose up -d

# Start production environment
docker-compose --profile production up -d

# Start with monitoring
docker-compose --profile monitoring up -d
```

### Management Commands

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f luciq-backend
docker-compose logs -f luciq-frontend

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild and restart
docker-compose up -d --build
```

### Health Checks

```bash
# Check all container status
docker-compose ps

# Check backend health
curl http://localhost:8003/health

# Check frontend health
curl http://localhost:3001/

# Check Redis
docker-compose exec redis redis-cli ping
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8003
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO

# Database Configuration
DATABASE_PATH=/app/luciq_discovery.db
POSTGRES_DB=luciq
POSTGRES_USER=luciq
POSTGRES_PASSWORD=your-postgres-password

# Frontend Configuration
NODE_ENV=production
VITE_API_URL=http://localhost:8003
VITE_WS_URL=ws://localhost:8003

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Security
CORS_ORIGINS=http://localhost:3001,http://localhost

# Performance
LUCIQ_FAST_MODE=true
DOCKER_DEPLOYMENT=true
```

### Volume Mounts

The following directories are mounted for persistence:

```yaml
volumes:
  - ./data:/app/data                    # Application data
  - ./logs:/app/logs                    # Application logs
  - ./working-memory:/app/working-memory # AI agent memory
  - luciq-db:/app/db                 # Database files
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using the ports
netstat -tulpn | grep :8003
netstat -tulpn | grep :3001

# Stop conflicting services
sudo systemctl stop apache2  # If Apache is running
sudo systemctl stop nginx    # If Nginx is running
```

#### 2. Memory Issues
```bash
# Check Docker memory usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Recommended: 8GB minimum, 16GB optimal
```

#### 3. Build Failures
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check disk space
df -h
```

#### 4. Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### Debug Mode

```bash
# Start with debug logging
LOG_LEVEL=DEBUG docker-compose up

# Access container shell
docker-compose exec luciq-backend bash
docker-compose exec luciq-frontend sh

# Check container resources
docker-compose exec luciq-backend top
```

## 📊 Performance Optimization

### Resource Allocation

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 8GB
- Disk: 10GB

**Recommended for Production:**
- CPU: 4+ cores
- RAM: 16GB+
- Disk: 50GB+ SSD

### Docker Compose Overrides

Create `docker-compose.override.yml` for custom configurations:

```yaml
version: '3.8'

services:
  luciq-backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  luciq-frontend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 🔐 Security Considerations

### Production Security

1. **Change Default Passwords**
   ```bash
   # Update in .env file
   SECRET_KEY=your-strong-secret-key
   POSTGRES_PASSWORD=your-strong-postgres-password
   GF_SECURITY_ADMIN_PASSWORD=your-grafana-password
   ```

2. **Enable HTTPS**
   ```bash
   # Add SSL certificates to config/nginx/ssl/
   # Update nginx.conf for HTTPS
   ```

3. **Network Security**
   ```bash
   # Use custom networks
   # Restrict external access to internal services
   ```

4. **Regular Updates**
   ```bash
   # Update base images regularly
   docker-compose pull
   docker-compose up -d
   ```

## 📈 Monitoring and Logging

### Grafana Dashboards

Pre-configured dashboards available:
- **System Overview**: Container metrics, resource usage
- **API Performance**: Response times, error rates
- **Business Intelligence**: AI engine performance
- **User Activity**: Frontend usage patterns

### Log Management

```bash
# View aggregated logs
docker-compose logs -f --tail=100

# Export logs
docker-compose logs > luciq-logs.txt

# Log rotation (add to crontab)
0 0 * * * docker-compose logs --tail=1000 > /var/log/luciq-$(date +%Y%m%d).log
```

## 🚀 Deployment to Cloud

### AWS ECS
```bash
# Install ECS CLI
# Configure cluster
# Deploy with docker-compose.yml
```

### Google Cloud Run
```bash
# Build and push images
# Deploy services
# Configure load balancer
```

### Azure Container Instances
```bash
# Create resource group
# Deploy container group
# Configure networking
```

## 📞 Support

For deployment issues:
1. Check the troubleshooting section above
2. Review container logs: `docker-compose logs -f`
3. Verify system requirements
4. Check Docker Desktop settings

---

**🎯 Luciq Enterprise Intelligence Platform - Containerized for Scale** 🚀 