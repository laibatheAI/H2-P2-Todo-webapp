import logging
import sys
from datetime import datetime
from typing import Any, Dict

# Create logger
logger = logging.getLogger("todo_app")
logger.setLevel(logging.INFO)

# Create handler for stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)

def log_request(method: str, url: str, user_id: str = None, status_code: int = None):
    """Log API request details"""
    user_info = f"User: {user_id}" if user_id else "Unauthenticated"
    status_info = f"Status: {status_code}" if status_code else ""
    logger.info(f"REQUEST: {method} {url} | {user_info} | {status_info}")

def log_authentication(event: str, user_email: str = None, success: bool = True):
    """Log authentication events"""
    status = "SUCCESS" if success else "FAILED"
    user_info = f"User: {user_email}" if user_email else "Unknown"
    logger.info(f"AUTH: {event} | {user_info} | {status}")

def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    logger.error(f"ERROR: {str(error)} | Context: {context}", exc_info=True)

def log_security_event(event: str, user_id: str = None, ip_address: str = None):
    """Log security-related events"""
    user_info = f"User: {user_id}" if user_id else "Unknown"
    ip_info = f"IP: {ip_address}" if ip_address else "Unknown"
    logger.warning(f"SECURITY: {event} | {user_info} | {ip_info}")