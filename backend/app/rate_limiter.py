"""Simple in-memory sliding-window rate limiter."""
from collections import defaultdict
from time import time


class RateLimiter:
    def __init__(self, limit: int, window: int):
        """
        limit: max requests allowed per window
        window: window size in seconds
        """
        self.limit = limit
        self.window = window
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        """Return True if the request is within the rate limit, False otherwise."""
        now = time()
        timestamps = self._requests[key]
        # Drop timestamps outside the current window
        self._requests[key] = [t for t in timestamps if now - t < self.window]
        if len(self._requests[key]) >= self.limit:
            return False
        self._requests[key].append(now)
        return True

    def reset(self) -> None:
        """Clear all stored request data (used in tests)."""
        self._requests.clear()
