#!/usr/bin/env python3
"""
Comprehensive Error Handling Service
Provides centralized error handling, logging, and user-friendly error responses
"""

import logging
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    DATABASE = "database"
    EXTERNAL_API = "external_api"
    SYSTEM = "system"
    BUSINESS_LOGIC = "business_logic"
    NETWORK = "network"
    UNKNOWN = "unknown"

@dataclass
class ErrorDetails:
    """Detailed error information"""
    error_id: str
    timestamp: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    user_message: str
    technical_details: str
    stack_trace: Optional[str]
    context: Dict[str, Any]
    user_id: Optional[str] = None
    endpoint: Optional[str] = None
    request_id: Optional[str] = None

class ErrorHandler:
    """Comprehensive error handling system"""
    
    def __init__(self):
        self.error_log: List[ErrorDetails] = []
        self.error_counts: Dict[str, int] = {}
        self.logs_dir = Path("data/logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # User-friendly error messages
        self.user_messages = {
            ErrorCategory.AUTHENTICATION: "Please check your login credentials and try again.",
            ErrorCategory.AUTHORIZATION: "You don't have permission to access this resource.",
            ErrorCategory.VALIDATION: "Please check your input and try again.",
            ErrorCategory.DATABASE: "We're experiencing technical difficulties. Please try again later.",
            ErrorCategory.EXTERNAL_API: "External service is temporarily unavailable. Please try again later.",
            ErrorCategory.SYSTEM: "System error occurred. Our team has been notified.",
            ErrorCategory.BUSINESS_LOGIC: "Unable to process your request. Please check your input.",
            ErrorCategory.NETWORK: "Network connection issue. Please check your connection and try again.",
            ErrorCategory.UNKNOWN: "An unexpected error occurred. Please try again later."
        }
        
        logger.info("Error Handler initialized")
    
    def handle_error(
        self,
        error: Exception,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Dict[str, Any] = None,
        user_id: Optional[str] = None,
        endpoint: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_message: Optional[str] = None
    ) -> ErrorDetails:
        """Handle and log an error"""
        
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(error)}"
        
        # Get stack trace
        stack_trace = traceback.format_exc() if error else None
        
        # Determine user-friendly message
        user_message = custom_message or self.user_messages.get(category, self.user_messages[ErrorCategory.UNKNOWN])
        
        # Create error details
        error_details = ErrorDetails(
            error_id=error_id,
            timestamp=datetime.now().isoformat(),
            category=category,
            severity=severity,
            message=str(error),
            user_message=user_message,
            technical_details=f"{type(error).__name__}: {str(error)}",
            stack_trace=stack_trace,
            context=context or {},
            user_id=user_id,
            endpoint=endpoint,
            request_id=request_id
        )
        
        # Log the error
        self._log_error(error_details)
        
        # Update error counts
        category_key = category.value
        self.error_counts[category_key] = self.error_counts.get(category_key, 0) + 1
        
        # Store in memory (keep last 1000 errors)
        self.error_log.append(error_details)
        if len(self.error_log) > 1000:
            self.error_log = self.error_log[-1000:]
        
        return error_details
    
    def _log_error(self, error_details: ErrorDetails):
        """Log error to file and console"""
        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(error_details.severity, logging.ERROR)
        
        log_message = (
            f"[{error_details.error_id}] {error_details.category.value.upper()}: "
            f"{error_details.message}"
        )
        
        if error_details.context:
            log_message += f" | Context: {error_details.context}"
        
        logger.log(log_level, log_message)
        
        # Write to error log file for critical errors
        if error_details.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            self._write_error_to_file(error_details)
    
    def _write_error_to_file(self, error_details: ErrorDetails):
        """Write error details to file"""
        try:
            error_file = self.logs_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Read existing errors
            errors = []
            if error_file.exists():
                with open(error_file, 'r') as f:
                    errors = json.load(f)
            
            # Add new error
            errors.append(asdict(error_details))
            
            # Write back to file
            with open(error_file, 'w') as f:
                json.dump(errors, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to write error to file: {e}")
    
    def get_error_summary(self, hours: int = 24) -> Dict:
        """Get error summary for the last N hours"""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        recent_errors = [
            error for error in self.error_log
            if datetime.fromisoformat(error.timestamp).timestamp() >= cutoff_time
        ]
        
        # Count by category
        category_counts = {}
        severity_counts = {}
        
        for error in recent_errors:
            category = error.category.value
            severity = error.severity.value
            
            category_counts[category] = category_counts.get(category, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "period_hours": hours,
            "total_errors": len(recent_errors),
            "category_breakdown": category_counts,
            "severity_breakdown": severity_counts,
            "error_rate": len(recent_errors) / max(hours, 1),  # errors per hour
            "most_common_category": max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None,
            "critical_errors": len([e for e in recent_errors if e.severity == ErrorSeverity.CRITICAL]),
            "recent_errors": [asdict(e) for e in recent_errors[-10:]]  # Last 10 errors
        }
    
    def get_error_trends(self, days: int = 7) -> Dict:
        """Get error trends over the last N days"""
        trends = {}
        
        for i in range(days):
            date = datetime.now().date() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            day_errors = [
                error for error in self.error_log
                if datetime.fromisoformat(error.timestamp).date() == date
            ]
            
            trends[date_str] = {
                "total": len(day_errors),
                "critical": len([e for e in day_errors if e.severity == ErrorSeverity.CRITICAL]),
                "high": len([e for e in day_errors if e.severity == ErrorSeverity.HIGH]),
                "medium": len([e for e in day_errors if e.severity == ErrorSeverity.MEDIUM]),
                "low": len([e for e in day_errors if e.severity == ErrorSeverity.LOW])
            }
        
        return trends
    
    def get_user_friendly_response(self, error_details: ErrorDetails) -> Dict:
        """Get user-friendly error response"""
        return {
            "error": True,
            "error_id": error_details.error_id,
            "message": error_details.user_message,
            "timestamp": error_details.timestamp,
            "support_info": {
                "error_id": error_details.error_id,
                "category": error_details.category.value,
                "contact": "support@luciq.com"
            }
        }
    
    def create_http_exception_response(self, error_details: ErrorDetails, status_code: int = 500) -> Dict:
        """Create HTTP exception response"""
        response = self.get_user_friendly_response(error_details)
        response["status_code"] = status_code
        
        # Add technical details for development
        if logger.level <= logging.DEBUG:
            response["technical_details"] = {
                "message": error_details.message,
                "category": error_details.category.value,
                "severity": error_details.severity.value,
                "context": error_details.context
            }
        
        return response
    
    def check_error_patterns(self) -> List[Dict]:
        """Check for error patterns that might indicate issues"""
        patterns = []
        
        # Check for high error rates
        recent_errors = self.get_error_summary(hours=1)
        if recent_errors["total_errors"] > 10:  # More than 10 errors in last hour
            patterns.append({
                "type": "high_error_rate",
                "severity": "warning",
                "message": f"High error rate detected: {recent_errors['total_errors']} errors in last hour",
                "details": recent_errors
            })
        
        # Check for critical errors
        critical_count = recent_errors.get("critical_errors", 0)
        if critical_count > 0:
            patterns.append({
                "type": "critical_errors",
                "severity": "critical",
                "message": f"{critical_count} critical errors detected in last hour",
                "details": {"critical_count": critical_count}
            })
        
        # Check for repeated errors
        error_messages = [error.message for error in self.error_log[-50:]]  # Last 50 errors
        message_counts = {}
        for msg in error_messages:
            message_counts[msg] = message_counts.get(msg, 0) + 1
        
        repeated_errors = {msg: count for msg, count in message_counts.items() if count >= 3}
        if repeated_errors:
            patterns.append({
                "type": "repeated_errors",
                "severity": "warning",
                "message": "Repeated error patterns detected",
                "details": repeated_errors
            })
        
        return patterns

# Global error handler instance
error_handler = ErrorHandler() 