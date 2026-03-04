"""Vocabulary analyzer using NLTK.

Metrics (from DESIGN.md):
- Type-token ratio (lexical diversity)
- Average content-word length (proxy for sophistication)
- Proportion of words with 3+ syllables (polysyllabic ratio)
"""
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .base import BaseAnalyzer

_STOP_WORDS = set(stopwords.words("english"))
_VOWELS = re.compile(r"[aeiou]", re.IGNORECASE)


def _syllable_count(word: str) -> int:
    """Simple vowel-cluster syllable counter — no external corpus needed."""
    word = word.lower().rstrip("e")
    syllables = len(_VOWELS.findall(word))
    return max(syllables, 1)


def _content_words(tokens: list[str]) -> list[str]:
    return [w for w in tokens if w.isalpha() and w.lower() not in _STOP_WORDS]


class VocabularyAnalyzer(BaseAnalyzer):
    def get_diagnostics(self, text: str) -> dict:
        tokens = word_tokenize(text)
        alpha = [w for w in tokens if w.isalpha()]
        word_count = max(len(alpha), 1)
        ttr = round(len({w.lower() for w in alpha}) / word_count, 3)
        content = _content_words([w.lower() for w in alpha])
        avg_len = round(sum(len(w) for w in content) / max(len(content), 1), 2)
        return {"ttr": ttr, "avg_word_length": avg_len}

    def analyze(self, text: str) -> float:
        tokens = word_tokenize(text)
        alpha_tokens = [w for w in tokens if w.isalpha()]
        word_count = max(len(alpha_tokens), 1)

        # Type-token ratio
        ttr = len({w.lower() for w in alpha_tokens}) / word_count

        # Average content-word length
        content = _content_words([w.lower() for w in alpha_tokens])
        avg_len = sum(len(w) for w in content) / max(len(content), 1)

        # Polysyllabic ratio (words with 3+ syllables)
        poly = sum(1 for w in content if _syllable_count(w) >= 3)
        poly_ratio = poly / max(len(content), 1)

        # Combine: TTR (0-1) → ~0-6 pts, avg_len (typically 4-8) → ~0-2 pts,
        # poly_ratio (0-1) → ~0-2 pts
        raw = ttr * 6.0 + min((avg_len - 3) / 5.0, 1.0) * 2.0 + poly_ratio * 2.0
        score = self._clamp(raw + 1.0)
        return round(score, 1)
