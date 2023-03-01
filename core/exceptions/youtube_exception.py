from typing import Any, Dict, Optional


class YouTubeException(Exception):
    """Base class for exceptions in this module."""

    def __init__(
        self, description: str = "", can_retry: bool = False, payload: Optional[Dict[Any, Any]] = None, *args, **kwargs
    ):
        if not payload:
            payload = {}
        self.description = description
        self.can_retry = can_retry
        self.payload = payload
        super().__init__(*args, **kwargs)
