# Luciq Quality Dashboard - Docker Setup Guide

🐳 **Complete guide to running Luciq Quality Dashboard with Docker**

## 🚀 Quick Start

### **Windows Users**
```cmd
# Simple startup (recommended)
start-quality-dashboard.bat

# OR manual startup
docker-compose up -d luciq-api luciq-frontend redis
```

### **Linux/Mac Users**  
```bash
# Simple startup (recommended)
./start-quality-dashboard.sh

# OR manual startup
docker-compose up -d luciq-api luciq-frontend redis
```

## 📋 Prerequisites

1. **Docker Desktop** installed and running
2. **Docker Compose** (included with Docker Desktop)
3. **8GB+ RAM** recommended for optimal performance
4. **Ports available**: 8000 (API), 3000 (Frontend), 6379 (Redis)

## 🔧 Setup Steps

### 1. **Verify Docker Installation**
```bash
docker --version
docker-compose --version
docker info
```

### 2. **Build and Start Services**
```bash
# Stop any existing containers
docker-compose down

# Build the application
docker-compose build luciq-api

# Start core services
docker-compose up -d luciq-api luciq-frontend redis

# Check status
docker-compose ps
```

### 3. **Verify Services Are Running**
```bash
# Check API health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# View logs
docker-compose logs -f luciq-api
```

## 🎯 Access Points

Once running, access these URLs:

- **🏠 Main Dashboard**: http://localhost:3000/pages/dashboard.html
- **📊 Quality Dashboard**: http://localhost:3000/pages/quality-dashboard.html  
- **🔧 API Documentation**: http://localhost:8000/docs
- **❤️ Health Check**: http://localhost:8000/health
- **📈 API Metrics**: http://localhost:8000/metrics

### Quality API Endpoints
- **Metrics**: http://localhost:8000/api/quality/metrics
- **Trends**: http://localhost:8000/api/quality/trends
- **Alerts**: http://localhost:8000/api/quality/alerts

## 🐛 Troubleshooting

### **Issue: Import Error "No module named 'shared'"**
✅ **Fixed in Docker setup** - The Dockerfile properly sets `PYTHONPATH=/app/src:/app`

### **Issue: Services won't start**
```bash
# Check Docker daemon
docker info

# Check ports are free
netstat -an | findstr ":8000\|:3000\|:6379"

# Restart Docker Desktop
# Then retry: docker-compose up -d
```

### **Issue: API returns 500 errors**
```bash
# Check API logs
docker-compose logs luciq-api

# Restart API service
docker-compose restart luciq-api

# Check database permissions
docker-compose exec luciq-api ls -la /app/data/
```

### **Issue: Frontend shows connection errors**
```bash
# Check if API is responding
curl http://localhost:8000/health

# Check frontend logs
docker-compose logs luciq-frontend

# Verify CORS settings in docker-compose.yml
```

## 📊 Quality Dashboard Features

The Docker setup includes all Quality Dashboard features:

### **Real-time Metrics**
- Quality validation rate (60% threshold)
- Signals processed count
- Active platforms monitoring
- API response time tracking

### **6-Dimensional Quality Scoring**
- Authenticity (20% weight)
- Freshness (15% weight)
- Relevance (25% weight)
- Source Credibility (15% weight)
- Content Quality (15% weight)
- Engagement Validity (10% weight)

### **Data Source Health**
- 8 data sources monitoring
- Real-time health indicators
- Platform status tracking

### **Interactive Charts**
- 24-hour quality trends
- Multiple time periods (6h, 24h, 72h)
- Dual-axis visualization
- Auto-refresh every 30 seconds

## 🔄 Docker Commands Reference

### **Basic Operations**
```bash
# Start all services
docker-compose up -d

# Stop all services  
docker-compose down

# Restart a service
docker-compose restart luciq-api

# View logs
docker-compose logs -f luciq-api

# Check status
docker-compose ps
```

### **Maintenance**
```bash
# Rebuild without cache
docker-compose build --no-cache luciq-api

# Remove all containers and volumes
docker-compose down -v

# Clean up Docker system
docker system prune -f
```

### **Debugging**
```bash
# Execute commands in container
docker-compose exec luciq-api bash

# Check environment variables
docker-compose exec luciq-api env

# Check Python path
docker-compose exec luciq-api python -c "import sys; print(sys.path)"
```

## 📁 Docker Configuration

### **Key Files**
- `Dockerfile` - Application container definition
- `docker-compose.yml` - Multi-service orchestration
- `start-quality-dashboard.bat/.sh` - Simple startup scripts

### **Environment Variables**
```yaml
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_PATH=/app/data/luciq_discovery.db
SECRET_KEY=luciq-docker-secret-key-2025
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost
PYTHONPATH=/app/src:/app
```

### **Volume Mounts**
```yaml
- ./data:/app/data              # Database persistence
- ./logs:/app/logs              # Log files
- ./working-memory:/app/working-memory  # Session data
```

## 🎉 Success Verification

After startup, you should see:

1. **✅ API Health Check**: `http://localhost:8000/health` returns `200 OK`
2. **✅ Quality Metrics**: `http://localhost:8000/api/quality/metrics` returns JSON
3. **✅ Frontend Loading**: `http://localhost:3000` shows Luciq interface
4. **✅ Quality Dashboard**: `http://localhost:3000/pages/quality-dashboard.html` displays metrics

## 🚀 Next Steps

1. **Access Quality Dashboard**: Navigate to the quality dashboard URL
2. **Create User Account**: Use the authentication system
3. **Start Discovery**: Begin discovering trends and pain points  
4. **Monitor Quality**: Watch real-time quality metrics and trends
5. **Explore API**: Use the interactive API documentation

## 💡 Tips

- **Performance**: The system performs best with 8GB+ RAM
- **Development**: Use `docker-compose logs -f` to monitor in real-time
- **Persistence**: Data persists in Docker volumes between restarts
- **Scaling**: Additional services can be added to docker-compose.yml
- **Monitoring**: Consider enabling Prometheus/Grafana for advanced monitoring

---

🎯 **Quality Dashboard is now running in Docker!** Access it at: http://localhost:3000/pages/quality-dashboard.html 