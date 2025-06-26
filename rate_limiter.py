"""
Rate limiting module for voting contract
"""

import time
from collections import defaultdict, deque
from threading import Lock
from logger import setup_logger

class RateLimiter:
    def __init__(self):
        self.logger = setup_logger("rate_limiter")
        self.requests = defaultdict(deque)
        self.lock = Lock()
        
        # Rate limit configurations
        self.limits = {
            'vote': {'count': 1, 'window': 3600},  # 1 vote per hour
            'proposal': {'count': 3, 'window': 86400},  # 3 proposals per day
            'api_call': {'count': 100, 'window': 3600},  # 100 API calls per hour
            'login': {'count': 5, 'window': 900}  # 5 login attempts per 15 minutes
        }
    
    def is_allowed(self, identifier, action_type):
        """Check if action is allowed for identifier"""
        try:
            with self.lock:
                current_time = time.time()
                key = f"{identifier}:{action_type}"
                
                if action_type not in self.limits:
                    self.logger.warning(f"Unknown action type: {action_type}")
                    return True
                
                limit_config = self.limits[action_type]
                window_size = limit_config['window']
                max_requests = limit_config['count']
                
                # Clean old requests outside the window
                request_times = self.requests[key]
                while request_times and request_times[0] < current_time - window_size:
                    request_times.popleft()
                
                # Check if limit exceeded
                if len(request_times) >= max_requests:
                    self.logger.warning(f"Rate limit exceeded for {identifier} - {action_type}")
                    return False
                
                # Record this request
                request_times.append(current_time)
                
                self.logger.info(f"Rate limit check passed: {identifier} - {action_type} ({len(request_times)}/{max_requests})")
                return True
                
        except Exception as e:
            self.logger.error(f"Rate limit check failed: {e}")
            return True  # Allow on error to avoid blocking legitimate users
    
    def get_remaining_requests(self, identifier, action_type):
        """Get remaining requests for identifier"""
        try:
            with self.lock:
                current_time = time.time()
                key = f"{identifier}:{action_type}"
                
                if action_type not in self.limits:
                    return -1
                
                limit_config = self.limits[action_type]
                window_size = limit_config['window']
                max_requests = limit_config['count']
                
                # Clean old requests
                request_times = self.requests[key]
                while request_times and request_times[0] < current_time - window_size:
                    request_times.popleft()
                
                remaining = max_requests - len(request_times)
                return max(0, remaining)
                
        except Exception as e:
            self.logger.error(f"Failed to get remaining requests: {e}")
            return -1
    
    def get_reset_time(self, identifier, action_type):
        """Get time when rate limit resets"""
        try:
            with self.lock:
                current_time = time.time()
                key = f"{identifier}:{action_type}"
                
                if action_type not in self.limits:
                    return current_time
                
                window_size = self.limits[action_type]['window']
                request_times = self.requests[key]
                
                if not request_times:
                    return current_time
                
                # Reset time is when the oldest request expires
                reset_time = request_times[0] + window_size
                return reset_time
                
        except Exception as e:
            self.logger.error(f"Failed to get reset time: {e}")
            return time.time()
    
    def clear_user_limits(self, identifier):
        """Clear all rate limits for a user (admin function)"""
        try:
            with self.lock:
                keys_to_remove = [key for key in self.requests.keys() if key.startswith(f"{identifier}:")]
                
                for key in keys_to_remove:
                    del self.requests[key]
                
                self.logger.info(f"Cleared rate limits for {identifier}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to clear limits: {e}")
            return False
    
    def get_stats(self):
        """Get rate limiter statistics"""
        try:
            with self.lock:
                stats = {
                    'total_tracked_users': len(set(key.split(':')[0] for key in self.requests.keys())),
                    'total_requests_tracked': sum(len(deque_obj) for deque_obj in self.requests.values()),
                    'limits_configured': len(self.limits),
                    'active_limits': len(self.requests)
                }
                
                return stats
                
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {}

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit_decorator(action_type):
    """Decorator for rate limiting functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Extract identifier from function arguments
            identifier = kwargs.get('user_id') or kwargs.get('address') or 'anonymous'
            
            if not rate_limiter.is_allowed(identifier, action_type):
                raise Exception(f"Rate limit exceeded for {action_type}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    # Test rate limiter
    limiter = RateLimiter()
    
    # Test voting rate limit
    user = "test_user_123"
    print(f"Vote allowed: {limiter.is_allowed(user, 'vote')}")
    print(f"Vote allowed again: {limiter.is_allowed(user, 'vote')}")  # Should be False
    print(f"Remaining votes: {limiter.get_remaining_requests(user, 'vote')}")