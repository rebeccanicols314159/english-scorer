"""Coherence and organisation analyzer.

Metrics (from DESIGN.md):
- Transition word frequency
- Paragraph structure (newline-separated blocks)
- Word count threshold (50+ words required for reliable assessment)
"""
from nltk.tokenize import word_tokenize, sent_tokenize
from .base import BaseAnalyzer

_TRANSITIONS = {
    "however", "therefore", "furthermore", "moreover", "additionally",
    "consequently", "nevertheless", "in addition", "on the other hand",
    "for example", "for instance", "in conclusion", "first", "second",
    "third", "finally", "meanwhile", "subsequently", "in contrast",
    "similarly", "as a result", "in summary", "thus", "hence",
    "although", "despite", "whereas", "while", "yet", "also",
    "besides", "indeed", "otherwise", "thereafter",
}


def _transition_density(text: str) -> float:
    """Transitions found per sentence."""
    sentences = sent_tokenize(text)
    if not sentences:
        return 0.0
    text_lower = text.lower()
    count = sum(1 for t in _TRANSITIONS if t in text_lower)
    return count / len(sentences)


def _paragraph_count(text: str) -> int:
    return max(len([p for p in text.split("\n") if p.strip()]), 1)


class CoherenceAnalyzer(BaseAnalyzer):
    def get_diagnostics(self, text: str) -> dict:
        tokens = word_tokenize(text)
        word_count = len(tokens)
        text_lower = text.lower()
        transition_count = sum(1 for t in _TRANSITIONS if t in text_lower)
        return {"transition_count": transition_count, "word_count": word_count}

    def analyze(self, text: str) -> float:
        word_count = len(word_tokenize(text))

        # Insufficient text for coherence assessment
        if word_count < 50:
            return round(self._clamp(1.0 + (word_count / 50.0) * 3.0), 1)

        td = _transition_density(text)
        # Ideal: ~0.5–1.0 transitions per sentence; plateau at 3+
        transition_score = min(td * 3.5, 4.0)

        para_bonus = min(_paragraph_count(text) * 0.3, 1.0)
        length_bonus = min((word_count - 50) / 450.0, 1.0)

        raw = 4.0 + transition_score + para_bonus + length_bonus
        return round(self._clamp(raw), 1)
