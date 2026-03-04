"""Shared utilities for all scoring analyzers."""
from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, text: str) -> float:
        """Analyze text and return a score from 1.0 to 10.0."""
        ...

    @abstractmethod
    def get_diagnostics(self, text: str) -> dict:
        """Return a dict of diagnostic data used to personalise feedback."""
        ...

    def _clamp(self, value: float, lo: float = 1.0, hi: float = 10.0) -> float:
        return max(lo, min(hi, value))

    def _error_rate_to_score(self, error_rate: float) -> float:
        """Map errors-per-100-words to a 1–10 score (lower errors = higher score)."""
        # 0 errors → 10, 15+ errors/100 words → 1
        return self._clamp(10.0 - error_rate * 0.6)
