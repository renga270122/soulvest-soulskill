"""
Analytics & Monitoring for SoulSkill Resume Builder
Track usage, errors, and performance metrics
"""
import os
from datetime import datetime
from typing import Dict, Optional, List
import json

class AnalyticsTracker:
    """Track user interactions and app usage"""
    
    def __init__(self):
        self.enabled = os.getenv('ANALYTICS_ENABLED', 'true').lower() == 'true'
        self.google_analytics_id = os.getenv('GOOGLE_ANALYTICS_ID', '')
        self.events = []
    
    def track_event(self, event_name: str, properties: Optional[Dict] = None, user_email: Optional[str] = None):
        """Track a custom event"""
        if not self.enabled:
            return
        
        event = {
            'event': event_name,
            'timestamp': datetime.now().isoformat(),
            'properties': properties or {},
            'user_email': user_email
        }
        
        self.events.append(event)
        
        # Log to database if available
        try:
            from database import get_db_manager
            db = get_db_manager()
            db.log_analytics(event_name, properties, user_email)
        except:
            pass
        
        # Send to Google Analytics if configured
        if self.google_analytics_id:
            self._send_to_google_analytics(event)
    
    def track_page_view(self, page_name: str, user_email: Optional[str] = None):
        """Track page view"""
        self.track_event('page_view', {'page': page_name}, user_email)
    
    def track_resume_created(self, template: str, user_email: Optional[str] = None):
        """Track resume creation"""
        self.track_event('resume_created', {'template': template}, user_email)
    
    def track_resume_downloaded(self, format: str, user_email: Optional[str] = None):
        """Track resume download"""
        self.track_event('resume_downloaded', {'format': format}, user_email)
    
    def track_ai_usage(self, feature: str, user_email: Optional[str] = None):
        """Track AI feature usage"""
        self.track_event('ai_feature_used', {'feature': feature}, user_email)
    
    def track_error(self, error_type: str, error_message: str, user_email: Optional[str] = None):
        """Track application error"""
        self.track_event('error', {
            'error_type': error_type,
            'message': error_message
        }, user_email)
    
    def _send_to_google_analytics(self, event: Dict):
        """Send event to Google Analytics 4"""
        # Placeholder for GA4 implementation
        # In production, use gtag.js or measurement protocol API
        pass
    
    def get_analytics_summary(self) -> Dict:
        """Get analytics summary"""
        if not self.events:
            return {}
        
        summary = {
            'total_events': len(self.events),
            'unique_users': len(set(e.get('user_email') for e in self.events if e.get('user_email'))),
            'event_counts': {}
        }
        
        for event in self.events:
            event_name = event['event']
            summary['event_counts'][event_name] = summary['event_counts'].get(event_name, 0) + 1
        
        return summary
    
    def inject_google_analytics(self) -> str:
        """Generate Google Analytics tracking code"""
        if not self.google_analytics_id:
            return ""
        
        return f"""
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={self.google_analytics_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{self.google_analytics_id}');
        </script>
        """


class PerformanceMonitor:
    """Monitor app performance and health"""
    
    def __init__(self):
        self.metrics = []
    
    def record_metric(self, metric_name: str, value: float, unit: str = 'ms'):
        """Record a performance metric"""
        self.metrics.append({
            'metric': metric_name,
            'value': value,
            'unit': unit,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_average(self, metric_name: str) -> float:
        """Get average value for a metric"""
        values = [m['value'] for m in self.metrics if m['metric'] == metric_name]
        return sum(values) / len(values) if values else 0
    
    def get_health_status(self) -> Dict:
        """Get overall app health status"""
        return {
            'status': 'healthy',  # or 'degraded', 'unhealthy'
            'metrics_collected': len(self.metrics),
            'uptime': 'active'
        }


class ErrorLogger:
    """Log and track application errors"""
    
    def __init__(self):
        self.errors = []
        self.error_file = 'soulskill_errors.log'
    
    def log_error(self, error: Exception, context: Optional[Dict] = None):
        """Log an error with context"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': type(error).__name__,
            'message': str(error),
            'context': context or {}
        }
        
        self.errors.append(error_entry)
        
        # Write to file
        with open(self.error_file, 'a') as f:
            f.write(json.dumps(error_entry) + '\n')
        
        # Track in analytics
        try:
            tracker = get_analytics_tracker()
            tracker.track_error(error_entry['type'], error_entry['message'])
        except:
            pass
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict]:
        """Get recent errors"""
        return self.errors[-limit:]


# Global instances
analytics_tracker = None
performance_monitor = None
error_logger = None

def get_analytics_tracker() -> AnalyticsTracker:
    """Get or create analytics tracker singleton"""
    global analytics_tracker
    if analytics_tracker is None:
        analytics_tracker = AnalyticsTracker()
    return analytics_tracker

def get_performance_monitor() -> PerformanceMonitor:
    """Get or create performance monitor singleton"""
    global performance_monitor
    if performance_monitor is None:
        performance_monitor = PerformanceMonitor()
    return performance_monitor

def get_error_logger() -> ErrorLogger:
    """Get or create error logger singleton"""
    global error_logger
    if error_logger is None:
        error_logger = ErrorLogger()
    return error_logger
