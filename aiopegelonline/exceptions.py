"""aiopegelonline exceptions."""
from __future__ import annotations


class PegelonlineError(Exception):
    """Base class for pegelonline errors."""


class PegelonlineDataError(PegelonlineError):
    """Raised to indicate invalid data."""

    def __init__(self, code: int, message: str = ""):
        """Initialize JSON RPC errors."""
        self.code = code
        self.message = message
        super().__init__(code, message)
