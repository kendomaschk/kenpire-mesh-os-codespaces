"""
🛠️ KenPire Utilities - Production Core
Common utilities and helper functions
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import secrets
import logging
from functools import wraps
import asyncio
import time

logger = logging.getLogger(__name__)


class JSONUtils:
    """JSON manipulation utilities"""
    
    @staticmethod
    def safe_load(file_path: str) -> Optional[Dict[str, Any]]:
        """Safely load JSON from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load JSON from {file_path}: {e}")
            return None
    
    @staticmethod
    def safe_save(data: Dict[str, Any], file_path: str) -> bool:
        """Safely save JSON to file"""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save JSON to {file_path}: {e}")
            return False
    
    @staticmethod
    def validate_schema(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """Validate JSON schema with required fields"""
        return all(field in data for field in required_fields)


class IDUtils:
    """ID generation and validation utilities"""
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate a UUID4 string"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_short_id(length: int = 8) -> str:
        """Generate a short random ID"""
        return secrets.token_urlsafe(length)[:length]
    
    @staticmethod
    def generate_hash(data: str) -> str:
        """Generate SHA256 hash of data"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def is_valid_uuid(uuid_string: str) -> bool:
        """Validate UUID format"""
        try:
            uuid.UUID(uuid_string, version=4)
            return True
        except ValueError:
            return False


class TimeUtils:
    """Time and timestamp utilities"""
    
    @staticmethod
    def utc_timestamp() -> str:
        """Get current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()
    
    @staticmethod
    def unix_timestamp() -> int:
        """Get current Unix timestamp"""
        return int(time.time())
    
    @staticmethod
    def parse_iso_timestamp(timestamp: str) -> Optional[datetime]:
        """Parse ISO timestamp string"""
        try:
            return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            return None
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 1:
            return f"{seconds*1000:.1f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"


class CacheUtils:
    """Simple in-memory caching utilities"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry['expires']:
                return entry['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        if ttl is None:
            ttl = self.default_ttl
        
        self.cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }
    
    def delete(self, key: str) -> None:
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
    
    def cleanup_expired(self) -> None:
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time >= entry['expires']
        ]
        for key in expired_keys:
            del self.cache[key]


class RetryUtils:
    """Retry mechanism utilities"""
    
    @staticmethod
    def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 1.0):
        """Decorator for retry with exponential backoff"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries - 1:
                            wait_time = backoff_factor * (2 ** attempt)
                            logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {e}")
                            await asyncio.sleep(wait_time)
                        else:
                            logger.error(f"All retries failed for {func.__name__}")
                
                raise last_exception
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries - 1:
                            wait_time = backoff_factor * (2 ** attempt)
                            logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {e}")
                            time.sleep(wait_time)
                        else:
                            logger.error(f"All retries failed for {func.__name__}")
                
                raise last_exception
            
            # Return appropriate wrapper based on function type
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator


class ValidationUtils:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Basic URL validation"""
        import re
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe filesystem usage"""
        import re
        # Remove or replace dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing whitespace and dots
        sanitized = sanitized.strip('. ')
        # Limit length
        if len(sanitized) > 255:
            sanitized = sanitized[:255]
        return sanitized or "default_filename"


class ConfigUtils:
    """Configuration management utilities"""
    
    @staticmethod
    def load_env_config() -> Dict[str, str]:
        """Load configuration from environment variables"""
        import os
        config = {}
        
        # Standard configuration keys
        env_vars = [
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY',
            'GOOGLE_API_KEY',
            'DATABASE_URL',
            'REDIS_URL',
            'SECRET_KEY',
            'ENVIRONMENT',
            'LOG_LEVEL'
        ]
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                config[var] = value
        
        return config
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            'environment': 'development',
            'log_level': 'INFO',
            'cache_ttl': 300,
            'max_retries': 3,
            'request_timeout': 30,
            'api_version': 'v1',
            'rate_limit': {
                'requests_per_minute': 100,
                'burst_limit': 10
            },
            'security': {
                'api_key_length': 32,
                'session_timeout': 3600,
                'max_login_attempts': 5
            }
        }


# Global utilities instances
json_utils = JSONUtils()
id_utils = IDUtils()
time_utils = TimeUtils()
validation_utils = ValidationUtils()
config_utils = ConfigUtils()

# Default cache instance
default_cache = CacheUtils()


# Helper function for quick logging setup
def setup_logging(level: str = "INFO", format_string: Optional[str] = None):
    """Setup logging configuration"""
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[logging.StreamHandler()]
    )