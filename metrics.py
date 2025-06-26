"""
Performance metrics for voting contract
"""

import time
import psutil
from datetime import datetime
from logger import setup_logger

class PerformanceMetrics:
    def __init__(self):
        self.logger = setup_logger("metrics")
        self.start_time = time.time()
        self.transaction_count = 0
        self.error_count = 0
    
    def record_transaction(self, tx_type, duration):
        """Record transaction performance"""
        try:
            self.transaction_count += 1
            
            metric = {
                'type': tx_type,
                'duration': duration,
                'timestamp': datetime.now().isoformat(),
                'total_transactions': self.transaction_count
            }
            
            self.logger.info(f"Transaction recorded: {tx_type} - {duration:.3f}s")
            return metric
        except Exception as e:
            self.logger.error(f"Metric recording failed: {e}")
            return None
    
    def get_system_metrics(self):
        """Get system performance metrics"""
        try:
            metrics = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'uptime': time.time() - self.start_time,
                'transaction_count': self.transaction_count,
                'error_count': self.error_count
            }
            
            self.logger.info("System metrics collected")
            return metrics
        except Exception as e:
            self.logger.error(f"System metrics failed: {e}")
            return None
    
    def calculate_throughput(self, time_window=3600):
        """Calculate transaction throughput"""
        try:
            throughput = self.transaction_count / (time.time() - self.start_time) * time_window
            
            self.logger.info(f"Throughput: {throughput:.2f} tx/hour")
            return throughput
        except Exception as e:
            self.logger.error(f"Throughput calculation failed: {e}")
            return 0
    
    def record_error(self, error_type, details=None):
        """Record error occurrence"""
        try:
            self.error_count += 1
            
            error_metric = {
                'type': error_type,
                'details': details,
                'timestamp': datetime.now().isoformat(),
                'total_errors': self.error_count
            }
            
            self.logger.warning(f"Error recorded: {error_type}")
            return error_metric
        except Exception as e:
            self.logger.error(f"Error recording failed: {e}")
            return None
    
    def generate_report(self):
        """Generate performance report"""
        try:
            report = {
                'uptime': time.time() - self.start_time,
                'transactions': self.transaction_count,
                'errors': self.error_count,
                'error_rate': (self.error_count / max(self.transaction_count, 1)) * 100,
                'throughput': self.calculate_throughput(),
                'system': self.get_system_metrics()
            }
            
            self.logger.info("Performance report generated")
            return report
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return None

if __name__ == "__main__":
    metrics = PerformanceMetrics()
    report = metrics.generate_report()
    print(f"Performance Report: {report}")