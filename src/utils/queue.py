"""Request queue manager for handling concurrent users."""

import asyncio
from datetime import datetime
from typing import Optional
from src.utils.config import settings
from src.utils.logger import logger


class RequestQueue:
    """Manages concurrent requests with a queue system."""
    
    def __init__(self, max_concurrent: int = None):
        """
        Initialize the request queue.
        
        Args:
            max_concurrent: Maximum number of concurrent requests
        """
        self.max_concurrent = max_concurrent or settings.max_concurrent_users
        self.active_requests = 0
        self.total_requests = 0
        self.queue = asyncio.Queue()
        self._lock = asyncio.Lock()
        
    async def acquire(self) -> bool:
        """
        Acquire a slot for processing a request.
        
        Returns:
            bool: True if slot acquired, False if queue is full
        """
        async with self._lock:
            if self.active_requests < self.max_concurrent:
                self.active_requests += 1
                self.total_requests += 1
                logger.info(f"Request acquired slot ({self.active_requests}/{self.max_concurrent})")
                return True
            else:
                logger.warning(f"Request rejected - max concurrent users reached ({self.max_concurrent})")
                return False
    
    async def release(self):
        """Release a request slot."""
        async with self._lock:
            if self.active_requests > 0:
                self.active_requests -= 1
                logger.info(f"Request released slot ({self.active_requests}/{self.max_concurrent})")
    
    def get_status(self) -> dict:
        """
        Get current queue status.
        
        Returns:
            dict: Current queue status
        """
        return {
            "active_requests": self.active_requests,
            "max_concurrent": self.max_concurrent,
            "total_processed": self.total_requests,
            "queue_available": self.active_requests < self.max_concurrent
        }


# Global request queue instance
request_queue = RequestQueue()
