# Luciq V2 Production Deployment Guide

## 🚀 Quick Start

### Windows
```bash
# Run the production deployment script
start_production.bat
```

### Linux/macOS
```bash
# Make scripts executable (first time only)
chmod +x start_production.sh stop_production.sh

# Run the production deployment
./start_production.sh
```

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 2GB available
- **Storage**: 1GB free space
- **Network**: Internet connection for Reddit API access

### Required Python Packages
The deployment script will automatically install these if missing:
- `fastapi` - Web framework for API
- `uvicorn` - ASGI server
- `requests` - HTTP client library
- `praw` - Reddit API wrapper
- `python-multipart` - Form data parsing

### Optional Dependencies
- `redis` - For enhanced caching (future enhancement)
- `nginx` - For production web server (alternative to Python HTTP server)

## 🏗️ Architecture Overview

### Services
1. **Discovery API Server** (Port 8001)
   - FastAPI application with LLM intelligence
   - Reddit scraping and analysis
   - Trend detection and monitoring
   - User authentication and data management

2. **Real-time Monitor Service** (Background)
   - Continuous trend analysis (15-minute intervals)
   - Signal detection and alert generation
   - Predictive analytics and forecasting

3. **Frontend Server** (Port 3000)
   - Static file server for web interface
   - Responsive design with Tailwind CSS
   - Real-time dashboard with Chart.js
   - Trend widgets and visualization components

### Data Flow
```
User Browser → Frontend (Port 3000) → Discovery API (Port 8001) → SQLite Database
                                    ↓
                              Real-time Monitor → Trend Analysis → Alerts
```

## 📁 Directory Structure

```
luciq/
├── start_production.bat          # Windows deployment script
├── start_production.sh           # Unix deployment script
├── stop_production.sh            # Unix stop script
├── luciq_discovery.db         # SQLite database
├── logs/                         # Runtime logs
│   ├── api.log                   # API server logs
│   ├── monitor.log               # Monitor service logs
│   ├── frontend.log              # Frontend server logs
│   ├── api.pid                   # API process ID
│   ├── monitor.pid               # Monitor process ID
│   └── frontend.pid              # Frontend process ID
├── apps/
│   ├── src/api/                  # Backend API code
│   │   ├── main.py               # FastAPI application
│   │   ├── trend_detector.py     # Trend analysis engine
│   │   └── llm_discovery_analysis.py # LLM intelligence
│   └── frontend/                 # Frontend application
│       ├── pages/                # HTML pages
│       ├── components/           # Reusable components
│       └── assets/               # Static assets
├── tools/discovery/              # Background services
│   └── realtime_monitor.py       # Real-time monitoring daemon
└── working-memory/               # System state and context
```

## 🔧 Configuration

### Environment Variables
The deployment script sets these automatically:
- `LUCIQ_ENV=production`
- `LUCIQ_API_PORT=8001`
- `LUCIQ_FRONTEND_PORT=3000`
- `LUCIQ_LOG_LEVEL=INFO`
- `LUCIQ_DB_PATH=luciq_discovery.db`

### Custom Configuration
To customize settings, edit the deployment script variables:

**Windows (start_production.bat):**
```batch
set LUCIQ_API_PORT=8001
set LUCIQ_FRONTEND_PORT=3000
set LUCIQ_LOG_LEVEL=INFO
```

**Unix (start_production.sh):**
```bash
export LUCIQ_API_PORT=8001
export LUCIQ_FRONTEND_PORT=3000
export LUCIQ_LOG_LEVEL=INFO
```

### Database Configuration
- **Type**: SQLite
- **Location**: `luciq_discovery.db` (root directory)
- **Auto-initialization**: Creates tables and sample data on first run
- **Backup**: Automatically preserved during updates

## 🌐 Access Points

Once deployed, access the application at:

| Service | URL | Description |
|---------|-----|-------------|
| **Landing Page** | http://localhost:3000/pages/index.html | Main entry point |
| **Discovery Tool** | http://localhost:3000/pages/discover.html | Reddit analysis interface |
| **Live Trends** | http://localhost:3000/pages/trends.html | Real-time trend dashboard |
| **My Ideas** | http://localhost:3000/pages/my-ideas.html | Saved ideas management |
| **API Health** | http://localhost:8001/ | API status check |
| **API Docs** | http://localhost:8001/docs | Interactive API documentation |

## 📊 Monitoring and Logs

### Log Files
All logs are stored in the `logs/` directory:

```bash
# View real-time API logs
tail -f logs/api.log

# View monitor service logs
tail -f logs/monitor.log

# View all logs simultaneously
tail -f logs/*.log
```

### Process Management

**Check running services:**
```bash
# Unix
ps aux | grep -E "(uvicorn|python.*http.server|realtime_monitor)"

# Windows
tasklist | findstr python
```

**Stop services:**
```bash
# Unix
./stop_production.sh

# Windows
# Close the terminal windows or use Task Manager
```

### Health Checks
The deployment script includes automatic health checks:
- API server response validation
- Frontend server accessibility
- Port availability verification
- Database connectivity testing

## 🔒 Security Considerations

### Production Hardening
1. **Change Default Ports** (if needed for security)
2. **Enable HTTPS** (add SSL certificates)
3. **Configure Firewall** (restrict access to necessary ports)
4. **Regular Updates** (keep Python packages updated)

### API Security
- JWT token-based authentication
- Input validation and sanitization
- Rate limiting (configurable)
- CORS protection

### Database Security
- SQLite file permissions
- Regular backups
- Data encryption (optional)

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```
[WARNING] Port 8001 is already in use
```
**Solution**: The script automatically kills existing processes. If issues persist:
```bash
# Unix
lsof -ti:8001 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

#### Python Dependencies Missing
```
[ERROR] Missing required Python packages
```
**Solution**: Install manually:
```bash
pip install fastapi uvicorn requests praw python-multipart
```

#### Database Initialization Failed
```
[ERROR] Failed to initialize database
```
**Solution**: Check permissions and disk space:
```bash
# Check disk space
df -h .

# Check permissions
ls -la luciq_discovery.db

# Manual database reset
rm luciq_discovery.db
# Re-run deployment script
```

#### API Server Won't Start
```
[ERROR] API server health check failed
```
**Solution**: Check logs and dependencies:
```bash
# Check API logs
cat logs/api.log

# Test manual start
cd apps/src/api
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

#### Frontend Not Loading
```
[ERROR] Frontend server health check failed
```
**Solution**: Verify file permissions and Python HTTP server:
```bash
# Check frontend logs
cat logs/frontend.log

# Test manual start
cd src/frontend
python -m http.server 3000
```

### Performance Issues

#### High Memory Usage
- Monitor with `htop` or Task Manager
- Restart services if memory usage exceeds 1GB
- Consider adding swap space on Linux

#### Slow API Responses
- Check Reddit API rate limits
- Monitor network connectivity
- Review API logs for bottlenecks

#### Database Locks
- Ensure only one instance is running
- Check for long-running queries
- Restart services if database is locked

## 🔄 Maintenance

### Regular Tasks
1. **Log Rotation** (weekly)
   ```bash
   # Archive old logs
   mkdir -p logs/archive
   mv logs/*.log logs/archive/
   ```

2. **Database Backup** (daily)
   ```bash
   cp luciq_discovery.db backups/luciq_$(date +%Y%m%d).db
   ```

3. **System Updates** (monthly)
   ```bash
   pip install --upgrade fastapi uvicorn requests praw
   ```

### Scaling Considerations
- **Horizontal Scaling**: Deploy multiple API instances with load balancer
- **Database Scaling**: Migrate to PostgreSQL for high-volume usage
- **Caching**: Implement Redis for improved performance
- **CDN**: Use content delivery network for static assets

## 📈 Performance Metrics

### Expected Performance
- **API Response Time**: < 2 seconds for discovery requests
- **Trend Analysis**: < 0.01 seconds per cycle
- **Memory Usage**: 200-500MB per service
- **Database Size**: ~1MB per 1000 saved ideas

### Monitoring Endpoints
- `GET /health` - API health status
- `GET /metrics` - Performance metrics (future enhancement)
- `GET /api/trends` - Trend analysis status

## 🆘 Support

### Getting Help
1. **Check Logs**: Review `logs/*.log` files for error details
2. **Verify Configuration**: Ensure all environment variables are set
3. **Test Components**: Use manual startup commands to isolate issues
4. **Documentation**: Refer to API docs at http://localhost:8001/docs

### Reporting Issues
When reporting issues, include:
- Operating system and Python version
- Complete error messages from logs
- Steps to reproduce the problem
- System resource usage (CPU, memory, disk)

---

## 🎉 Success!

If you see this message after running the deployment script:

```
🚀 System Status: OPERATIONAL
```

Your Luciq V2 system is successfully deployed and ready for use!

Visit http://localhost:3000/pages/index.html to start discovering SaaS opportunities. 