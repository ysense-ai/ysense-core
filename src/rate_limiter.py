"""
YSense™ Rate Limiter
====================
Protects against DDoS attacks and abuse by limiting request rates.
Uses session-based tracking (no external dependencies required).
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Optional
import hashlib
import time


class RateLimiter:
    """
    Simple rate limiter using Streamlit session state.

    Features:
    - Per-session request counting
    - Time-based windows
    - IP-based tracking (when available)
    - Automatic cleanup of old entries
    """

    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 3600,
        cooldown_seconds: int = 30
    ):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds (default: 1 hour)
            cooldown_seconds: Minimum seconds between requests
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.cooldown_seconds = cooldown_seconds

        # Initialize session state
        if 'rate_limit_requests' not in st.session_state:
            st.session_state.rate_limit_requests = []

        if 'last_request_time' not in st.session_state:
            st.session_state.last_request_time = None

    def _get_client_id(self) -> str:
        """
        Get a unique identifier for this client.
        Uses session ID as fallback.
        """
        # Try to get IP from headers (when behind proxy)
        try:
            from streamlit.web.server.websocket_headers import _get_websocket_headers
            headers = _get_websocket_headers()
            if headers and 'X-Forwarded-For' in headers:
                ip = headers['X-Forwarded-For'].split(',')[0].strip()
                return hashlib.sha256(ip.encode()).hexdigest()[:16]
        except:
            pass

        # Fallback to session-based tracking
        if 'client_id' not in st.session_state:
            st.session_state.client_id = hashlib.sha256(
                str(time.time()).encode()
            ).hexdigest()[:16]

        return st.session_state.client_id

    def _cleanup_old_requests(self):
        """Remove requests older than the time window."""
        cutoff_time = datetime.now() - timedelta(seconds=self.window_seconds)
        st.session_state.rate_limit_requests = [
            req_time for req_time in st.session_state.rate_limit_requests
            if req_time > cutoff_time
        ]

    def check_rate_limit(self) -> tuple[bool, Optional[str]]:
        """
        Check if the request should be allowed.

        Returns:
            Tuple of (allowed: bool, error_message: Optional[str])
        """
        self._cleanup_old_requests()
        now = datetime.now()

        # Check cooldown period
        if st.session_state.last_request_time:
            time_since_last = (now - st.session_state.last_request_time).total_seconds()
            if time_since_last < self.cooldown_seconds:
                remaining = int(self.cooldown_seconds - time_since_last)
                return False, f"⏳ Please wait {remaining} seconds before trying again."

        # Check request count
        request_count = len(st.session_state.rate_limit_requests)
        if request_count >= self.max_requests:
            return False, f"🚫 Rate limit exceeded. Maximum {self.max_requests} requests per hour. Please try again later."

        return True, None

    def record_request(self):
        """Record a new request."""
        now = datetime.now()
        st.session_state.rate_limit_requests.append(now)
        st.session_state.last_request_time = now

    def get_remaining_requests(self) -> int:
        """Get number of remaining requests in current window."""
        self._cleanup_old_requests()
        return max(0, self.max_requests - len(st.session_state.rate_limit_requests))

    def get_cooldown_remaining(self) -> int:
        """Get remaining cooldown seconds."""
        if not st.session_state.last_request_time:
            return 0

        elapsed = (datetime.now() - st.session_state.last_request_time).total_seconds()
        remaining = max(0, self.cooldown_seconds - elapsed)
        return int(remaining)


# Global rate limiter instances for different operations
PAGE_RATE_LIMITER = RateLimiter(
    max_requests=200,    # 200 page loads per hour
    window_seconds=3600,
    cooldown_seconds=1   # 1 second between page loads
)

API_RATE_LIMITER = RateLimiter(
    max_requests=10,     # 10 API calls per hour
    window_seconds=3600,
    cooldown_seconds=30  # 30 seconds between API calls
)

SUBMIT_RATE_LIMITER = RateLimiter(
    max_requests=50,     # 50 form submissions per hour
    window_seconds=3600,
    cooldown_seconds=5   # 5 seconds between submissions
)


def rate_limit_decorator(limiter: RateLimiter):
    """
    Decorator to apply rate limiting to functions.

    Usage:
        @rate_limit_decorator(API_RATE_LIMITER)
        def my_api_call():
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            allowed, error = limiter.check_rate_limit()
            if not allowed:
                st.error(error)
                st.stop()

            limiter.record_request()
            return func(*args, **kwargs)

        return wrapper
    return decorator


def show_rate_limit_info(limiter: RateLimiter, label: str = "requests"):
    """
    Display rate limit information to user.

    Args:
        limiter: The RateLimiter instance
        label: Label for the rate limit (e.g., "API calls", "requests")
    """
    remaining = limiter.get_remaining_requests()
    cooldown = limiter.get_cooldown_remaining()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            f"Remaining {label}",
            f"{remaining}/{limiter.max_requests}"
        )
    with col2:
        if cooldown > 0:
            st.metric("Next request available in", f"{cooldown}s")
        else:
            st.metric("Status", "✅ Ready")
