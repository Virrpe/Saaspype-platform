#!/usr/bin/env python3
"""
Metrics Service - Track API usage and performance
"""

import time
import logging
import psutil
from typing import Dict, Any
from src.shared.database.connection import db_service
import os

logger = logging.getLogger(__name__)

class MetricsService:
    """Service for application metrics and health monitoring"""
    
    def __init__(self):
        self.app_metrics = {
            "start_time": time.time(),
            "requests_total": 0,
            "requests_by_endpoint": {},
            "errors_total": 0,
            "discovery_sessions": 0,
            "ideas_saved": 0,
            "trend_analyses": 0
        }
    
    def increment_request_counter(self, endpoint: str):
        """Increment request counters for metrics"""
        self.app_metrics["requests_total"] += 1
        self.app_metrics["requests_by_endpoint"][endpoint] = \
            self.app_metrics["requests_by_endpoint"].get(endpoint, 0) + 1
    
    def increment_error_counter(self):
        """Increment error counter"""
        self.app_metrics["errors_total"] += 1
    
    def increment_discovery_sessions(self):
        """Increment discovery session counter"""
        self.app_metrics["discovery_sessions"] += 1
    
    def increment_ideas_saved(self):
        """Increment ideas saved counter"""
        self.app_metrics["ideas_saved"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current application metrics"""
        uptime = time.time() - self.app_metrics["start_time"]
        return {
            "uptime_seconds": uptime,
            "requests_total": self.app_metrics["requests_total"],
            "requests_by_endpoint": self.app_metrics["requests_by_endpoint"],
            "errors_total": self.app_metrics["errors_total"],
            "discovery_sessions": self.app_metrics["discovery_sessions"],
            "ideas_saved": self.app_metrics["ideas_saved"]
        }
    
    def get_health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        try:
            # Test database connection
            conn = db_service.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            conn.close()
            db_status = "healthy"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        # System metrics
        try:
            memory = psutil.virtual_memory()
            # Fix Windows path handling - ensure proper drive path format
            current_drive = os.path.splitdrive(os.getcwd())[0]
            if current_drive and not current_drive.endswith(os.sep):
                current_drive += os.sep
            # Fallback to C:\ if drive detection fails
            if not current_drive:
                current_drive = "C:" + os.sep
            
            disk = psutil.disk_usage(current_drive)
            
            system_metrics = {
                "memory_usage_percent": memory.percent,
                "disk_usage_percent": disk.percent,
                "cpu_count": psutil.cpu_count()
            }
        except Exception as e:
            logger.warning(f"Could not get system metrics: {e}")
            system_metrics = {
                "memory_usage_percent": 0,
                "disk_usage_percent": 0,
                "cpu_count": 1
            }
        
        uptime = time.time() - self.app_metrics["start_time"]
        
        health_data = {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "timestamp": time.time(),
            "uptime_seconds": uptime,
            "database": db_status,
            "system": system_metrics,
            "metrics": {
                "total_requests": self.app_metrics["requests_total"],
                "total_errors": self.app_metrics["errors_total"],
                "error_rate": self.app_metrics["errors_total"] / max(self.app_metrics["requests_total"], 1) * 100
            }
        }
        
        return health_data
    
    def get_startup_summary(self) -> Dict[str, Any]:
        """Get startup summary for logging"""
        return {
            "total_requests": self.app_metrics["requests_total"],
            "total_errors": self.app_metrics["errors_total"],
            "discovery_sessions": self.app_metrics["discovery_sessions"],
            "ideas_saved": self.app_metrics["ideas_saved"]
        }

# Create service instance
metrics_service = MetricsService() 