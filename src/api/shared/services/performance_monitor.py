#!/usr/bin/env python3
"""
Performance Monitoring Service
Tracks system metrics, API performance, and user experience indicators
"""

import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    timestamp: str
    metric_type: str
    value: float
    unit: str
    context: Dict = None

@dataclass
class SystemHealth:
    """System health snapshot"""
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_io: Dict
    active_connections: int
    response_time_avg: float
    error_rate: float
    uptime: float

class PerformanceMonitor:
    """Comprehensive performance monitoring system"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.start_time = time.time()
        self.request_times: List[float] = []
        self.error_count = 0
        self.total_requests = 0
        self.logs_dir = Path("data/logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance thresholds
        self.thresholds = {
            'cpu_warning': 70.0,
            'cpu_critical': 85.0,
            'memory_warning': 75.0,
            'memory_critical': 90.0,
            'response_time_warning': 2.0,
            'response_time_critical': 5.0,
            'error_rate_warning': 5.0,
            'error_rate_critical': 10.0
        }
        
        logger.info("Performance Monitor initialized")
    
    def record_request(self, duration: float, success: bool = True):
        """Record API request performance"""
        self.total_requests += 1
        self.request_times.append(duration)
        
        if not success:
            self.error_count += 1
        
        # Keep only last 1000 requests for rolling average
        if len(self.request_times) > 1000:
            self.request_times = self.request_times[-1000:]
        
        # Record metric
        metric = PerformanceMetric(
            timestamp=datetime.now().isoformat(),
            metric_type="api_response_time",
            value=duration,
            unit="seconds",
            context={"success": success}
        )
        self.metrics.append(metric)
    
    def get_system_health(self) -> SystemHealth:
        """Get current system health snapshot"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # Active connections (approximate)
            connections = len(psutil.net_connections())
            
            # Calculate averages
            avg_response_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
            error_rate = (self.error_count / self.total_requests * 100) if self.total_requests > 0 else 0
            uptime = time.time() - self.start_time
            
            health = SystemHealth(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_usage=disk.percent,
                network_io=network_io,
                active_connections=connections,
                response_time_avg=avg_response_time,
                error_rate=error_rate,
                uptime=uptime
            )
            
            # Record system metrics
            self._record_system_metrics(health)
            
            return health
            
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return SystemHealth(0, 0, 0, {}, 0, 0, 0, 0)
    
    def _record_system_metrics(self, health: SystemHealth):
        """Record system metrics"""
        timestamp = datetime.now().isoformat()
        
        metrics = [
            PerformanceMetric(timestamp, "cpu_usage", health.cpu_percent, "percent"),
            PerformanceMetric(timestamp, "memory_usage", health.memory_percent, "percent"),
            PerformanceMetric(timestamp, "disk_usage", health.disk_usage, "percent"),
            PerformanceMetric(timestamp, "error_rate", health.error_rate, "percent"),
            PerformanceMetric(timestamp, "avg_response_time", health.response_time_avg, "seconds")
        ]
        
        self.metrics.extend(metrics)
    
    def check_alerts(self, health: SystemHealth) -> List[Dict]:
        """Check for performance alerts"""
        alerts = []
        
        # CPU alerts
        if health.cpu_percent >= self.thresholds['cpu_critical']:
            alerts.append({
                'level': 'CRITICAL',
                'metric': 'CPU Usage',
                'value': health.cpu_percent,
                'threshold': self.thresholds['cpu_critical'],
                'message': f"CPU usage critically high: {health.cpu_percent:.1f}%"
            })
        elif health.cpu_percent >= self.thresholds['cpu_warning']:
            alerts.append({
                'level': 'WARNING',
                'metric': 'CPU Usage',
                'value': health.cpu_percent,
                'threshold': self.thresholds['cpu_warning'],
                'message': f"CPU usage high: {health.cpu_percent:.1f}%"
            })
        
        # Memory alerts
        if health.memory_percent >= self.thresholds['memory_critical']:
            alerts.append({
                'level': 'CRITICAL',
                'metric': 'Memory Usage',
                'value': health.memory_percent,
                'threshold': self.thresholds['memory_critical'],
                'message': f"Memory usage critically high: {health.memory_percent:.1f}%"
            })
        elif health.memory_percent >= self.thresholds['memory_warning']:
            alerts.append({
                'level': 'WARNING',
                'metric': 'Memory Usage',
                'value': health.memory_percent,
                'threshold': self.thresholds['memory_warning'],
                'message': f"Memory usage high: {health.memory_percent:.1f}%"
            })
        
        # Response time alerts
        if health.response_time_avg >= self.thresholds['response_time_critical']:
            alerts.append({
                'level': 'CRITICAL',
                'metric': 'Response Time',
                'value': health.response_time_avg,
                'threshold': self.thresholds['response_time_critical'],
                'message': f"Response time critically slow: {health.response_time_avg:.2f}s"
            })
        elif health.response_time_avg >= self.thresholds['response_time_warning']:
            alerts.append({
                'level': 'WARNING',
                'metric': 'Response Time',
                'value': health.response_time_avg,
                'threshold': self.thresholds['response_time_warning'],
                'message': f"Response time slow: {health.response_time_avg:.2f}s"
            })
        
        # Error rate alerts
        if health.error_rate >= self.thresholds['error_rate_critical']:
            alerts.append({
                'level': 'CRITICAL',
                'metric': 'Error Rate',
                'value': health.error_rate,
                'threshold': self.thresholds['error_rate_critical'],
                'message': f"Error rate critically high: {health.error_rate:.1f}%"
            })
        elif health.error_rate >= self.thresholds['error_rate_warning']:
            alerts.append({
                'level': 'WARNING',
                'metric': 'Error Rate',
                'value': health.error_rate,
                'threshold': self.thresholds['error_rate_warning'],
                'message': f"Error rate high: {health.error_rate:.1f}%"
            })
        
        return alerts
    
    def get_performance_summary(self, hours: int = 24) -> Dict:
        """Get performance summary for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_metrics = [
            m for m in self.metrics 
            if datetime.fromisoformat(m.timestamp) >= cutoff_time
        ]
        
        # Group metrics by type
        metric_groups = {}
        for metric in recent_metrics:
            if metric.metric_type not in metric_groups:
                metric_groups[metric.metric_type] = []
            metric_groups[metric.metric_type].append(metric.value)
        
        # Calculate statistics
        summary = {}
        for metric_type, values in metric_groups.items():
            if values:
                summary[metric_type] = {
                    'count': len(values),
                    'avg': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'latest': values[-1] if values else 0
                }
        
        return {
            'period_hours': hours,
            'total_requests': self.total_requests,
            'total_errors': self.error_count,
            'uptime_hours': (time.time() - self.start_time) / 3600,
            'metrics': summary
        }
    
    def export_metrics(self, filename: Optional[str] = None) -> str:
        """Export metrics to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_metrics_{timestamp}.json"
        
        filepath = self.logs_dir / filename
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'system_info': {
                'uptime': time.time() - self.start_time,
                'total_requests': self.total_requests,
                'total_errors': self.error_count
            },
            'current_health': asdict(self.get_system_health()),
            'performance_summary': self.get_performance_summary(),
            'recent_metrics': [asdict(m) for m in self.metrics[-100:]]  # Last 100 metrics
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Performance metrics exported to {filepath}")
        return str(filepath)
    
    def get_user_experience_score(self) -> float:
        """Calculate user experience score (0-100)"""
        health = self.get_system_health()
        
        # Weight factors for UX score
        weights = {
            'response_time': 0.4,
            'error_rate': 0.3,
            'system_performance': 0.3
        }
        
        # Response time score (inverse relationship)
        if health.response_time_avg <= 0.5:
            response_score = 100
        elif health.response_time_avg <= 1.0:
            response_score = 90
        elif health.response_time_avg <= 2.0:
            response_score = 70
        elif health.response_time_avg <= 5.0:
            response_score = 40
        else:
            response_score = 10
        
        # Error rate score (inverse relationship)
        error_score = max(0, 100 - (health.error_rate * 10))
        
        # System performance score (average of CPU and memory)
        cpu_score = max(0, 100 - health.cpu_percent)
        memory_score = max(0, 100 - health.memory_percent)
        system_score = (cpu_score + memory_score) / 2
        
        # Calculate weighted UX score
        ux_score = (
            response_score * weights['response_time'] +
            error_score * weights['error_rate'] +
            system_score * weights['system_performance']
        )
        
        return round(ux_score, 1)

# Global performance monitor instance
performance_monitor = PerformanceMonitor() 