"""Sentence structure analyzer using NLTK + textstat.

Metrics (from DESIGN.md):
- Average sentence length
- Sentence length variety (coefficient of variation)
- Proportion of complex sentences (containing subordinating conjunctions)
"""
import statistics
from nltk.tokenize import sent_tokenize, word_tokenize
from .base import BaseAnalyzer

# Subordinating conjunctions signal complex sentence structure
_SUBORDINATORS = {
    "although", "because", "since", "while", "whereas", "unless", "until",
    "if", "when", "whenever", "after", "before", "as", "though", "even",
    "whether", "which", "who", "whom", "whose", "that",
}


def _sentence_lengths(text: str) -> list[int]:
    return [len(word_tokenize(s)) for s in sent_tokenize(text) if s.strip()]


def _complex_sentence_ratio(text: str) -> float:
    sentences = sent_tokenize(text)
    if not sentences:
        return 0.0
    complex_count = sum(
        1 for s in sentences
        if any(w.lower() in _SUBORDINATORS for w in word_tokenize(s))
    )
    return complex_count / len(sentences)


class SentenceStructureAnalyzer(BaseAnalyzer):
    def get_diagnostics(self, text: str) -> dict:
        lengths = _sentence_lengths(text)
        avg = round(sum(lengths) / max(len(lengths), 1), 1)
        complex_ratio = round(_complex_sentence_ratio(text), 3)
        return {
            "avg_sentence_length": avg,
            "sentence_count": len(lengths),
            "complex_ratio": complex_ratio,
        }

    def analyze(self, text: str) -> float:
        lengths = _sentence_lengths(text)
        if not lengths:
            return 1.0

        avg = sum(lengths) / len(lengths)
        # Penalise very short (<5) or very long (>40) average sentence lengths
        length_penalty = abs(avg - 17) * 0.15

        # Variety: coefficient of variation (std/mean); higher = more varied
        cv = (statistics.stdev(lengths) / avg) if len(lengths) > 1 else 0.0
        variety_bonus = min(cv * 3.0, 2.5)

        # Complexity bonus
        complexity_bonus = _complex_sentence_ratio(text) * 2.0

        raw = 6.5 - length_penalty + variety_bonus + complexity_bonus
        return round(self._clamp(raw), 1)
