# Luciq Discovery Engine 2.0 - Docker Deployment Guide

## 🐳 Complete Dockerized Deployment

This guide provides comprehensive instructions for deploying the entire Luciq Discovery Engine 2.0 using Docker containers.

## 📋 Prerequisites

- **Docker**: Version 20.10+ 
- **Docker Compose**: Version 2.0+
- **System Requirements**: 4GB RAM, 10GB disk space
- **Ports**: 3000, 8000, 6379 (and optionally 9090, 3001 for monitoring)

### Quick Installation Check
```bash
# Check Docker installation
docker --version
docker-compose --version

# Verify Docker is running
docker info
```

## 🚀 Quick Start

### Option 1: One-Command Startup (Linux/macOS)
```bash
chmod +x docker-start.sh
./docker-start.sh
```

### Option 2: One-Command Startup (Windows)
```cmd
docker-start.bat
```

### Option 3: Manual Docker Compose
```bash
# Build and start core services
docker-compose up -d

# Or with monitoring enabled
docker-compose --profile monitoring up -d
```

## 🏗️ Architecture Overview

The Docker deployment includes:

### Core Services
- **luciq-api**: FastAPI backend (Port 8000)
- **luciq-frontend**: Nginx static server (Port 3000)
- **redis**: Caching and background tasks (Port 6379)
- **luciq-worker**: Background trend detection worker

### Optional Monitoring (--monitoring flag)
- **prometheus**: Metrics collection (Port 9090)
- **grafana**: Visualization dashboard (Port 3001)

## 📁 File Structure

```
luciq/
├── Dockerfile                 # Multi-stage application build
├── docker-compose.yml         # Service orchestration
├── nginx.conf                 # Frontend proxy configuration
├── requirements.txt           # Python dependencies
├── docker-start.sh           # Linux/macOS startup script
├── docker-start.bat          # Windows startup script
├── .dockerignore             # Build optimization
└── monitoring/               # Optional monitoring configs
    ├── prometheus.yml
    └── grafana/
        ├── dashboards/
        └── datasources/
```

## 🔧 Configuration

### Environment Variables

The system uses these key environment variables:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_PATH=/app/data/luciq_discovery.db
LOG_LEVEL=INFO
SECRET_KEY=luciq-discovery-secret-key-2025-docker

# CORS and Security
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Redis Configuration
REDIS_URL=redis://redis:6379/0
```

### Volume Mounts

Data persistence is handled through Docker volumes:

```yaml
volumes:
  - ./data:/app/data                    # Database and persistent data
  - ./logs:/app/logs                    # Application logs
  - ./working-memory:/app/working-memory # Session and cache data
```

## 🎯 Service URLs

After successful deployment:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application |
| **Trends Page** | http://localhost:3000/pages/trends.html | Discovery Engine 2.0 |
| **API** | http://localhost:8000 | REST API endpoints |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | System health status |
| **Metrics** | http://localhost:8000/metrics | Performance metrics |

### Monitoring URLs (if enabled)
| Service | URL | Credentials |
|---------|-----|-------------|
| **Prometheus** | http://localhost:9090 | None |
| **Grafana** | http://localhost:3001 | admin/luciq2025 |

## 🛠️ Management Commands

### Starting Services
```bash
# Start core services
docker-compose up -d

# Start with monitoring
docker-compose --profile monitoring up -d

# Start specific service
docker-compose up -d luciq-api
```

### Monitoring Services
```bash
# View all service status
docker-compose ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f luciq-api

# View recent logs
docker-compose logs --tail=50
```

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

### Maintenance
```bash
# Rebuild services
docker-compose build --no-cache

# Update and restart
docker-compose pull
docker-compose up -d

# Clean up unused resources
docker system prune -f
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using the ports
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Kill processes using the ports
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:3000 | xargs kill -9
```

#### 2. Permission Issues
```bash
# Fix directory permissions
sudo chown -R $USER:$USER data logs working-memory
chmod 755 data logs working-memory
```

#### 3. Database Issues
```bash
# Reset database
rm -f data/luciq_discovery.db
docker-compose restart luciq-api
```

#### 4. Memory Issues
```bash
# Check container resource usage
docker stats

# Increase Docker memory limit (Docker Desktop)
# Settings > Resources > Advanced > Memory: 4GB+
```

### Health Checks

The system includes comprehensive health checks:

```bash
# API health check
curl http://localhost:8000/health

# Frontend health check
curl http://localhost:3000

# Redis health check
docker-compose exec redis redis-cli ping
```

### Log Analysis

```bash
# API errors
docker-compose logs luciq-api | grep ERROR

# Worker status
docker-compose logs luciq-worker

# Nginx access logs
docker-compose logs luciq-frontend
```

## 🔒 Security Considerations

### Production Deployment

For production use, consider these security enhancements:

1. **Environment Variables**
```bash
# Use secure secrets
SECRET_KEY=your-secure-secret-key-here
DATABASE_PATH=/secure/path/to/database

# Restrict CORS origins
CORS_ORIGINS=https://yourdomain.com
```

2. **SSL/TLS Configuration**
```yaml
# Add SSL termination
services:
  nginx-ssl:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl
      - ./nginx-ssl.conf:/etc/nginx/nginx.conf
```

3. **Network Security**
```yaml
# Use custom networks
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

## 📊 Monitoring and Metrics

### Prometheus Metrics

Available at http://localhost:9090 (when monitoring enabled):

- API request rates and latencies
- Error rates and status codes
- System resource usage
- Custom business metrics

### Grafana Dashboards

Available at http://localhost:3001 (admin/luciq2025):

- Real-time system overview
- API performance metrics
- Discovery engine analytics
- Alert management

### Custom Metrics

Add custom metrics to your application:

```python
from prometheus_client import Counter, Histogram

# Request counter
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests')

# Response time histogram
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'API request duration')
```

## 🚀 Performance Optimization

### Resource Limits

Configure resource limits in docker-compose.yml:

```yaml
services:
  luciq-api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

### Caching Strategy

Redis is configured for:
- Session storage
- API response caching
- Background task queuing
- Real-time data caching

### Database Optimization

SQLite optimizations:
- WAL mode enabled
- Connection pooling
- Query optimization
- Regular VACUUM operations

## 🔄 Backup and Recovery

### Automated Backups

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec luciq-api sqlite3 /app/data/luciq_discovery.db ".backup /app/data/backup_$DATE.db"
```

### Data Recovery

```bash
# Restore from backup
cp data/backup_20250101_120000.db data/luciq_discovery.db
docker-compose restart luciq-api
```

## 📈 Scaling Considerations

### Horizontal Scaling

```yaml
# Scale workers
docker-compose up -d --scale luciq-worker=3

# Load balancer configuration
services:
  nginx-lb:
    image: nginx:alpine
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
```

### Database Scaling

For larger deployments, consider:
- PostgreSQL instead of SQLite
- Read replicas
- Connection pooling
- Database sharding

## 🎉 Success Verification

After deployment, verify everything is working:

1. ✅ **API Health**: http://localhost:8000/health returns 200
2. ✅ **Frontend**: http://localhost:3000 loads successfully
3. ✅ **Trends Page**: http://localhost:3000/pages/trends.html shows Discovery Engine 2.0
4. ✅ **API Docs**: http://localhost:8000/docs shows interactive documentation
5. ✅ **Background Tasks**: Worker logs show trend detection activity
6. ✅ **Redis**: `docker-compose exec redis redis-cli ping` returns PONG

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs -f`
3. Verify system requirements and port availability
4. Ensure Docker and Docker Compose are up to date

---

**🎯 Ready to discover the next big SaaS opportunity with Docker! 🚀** 