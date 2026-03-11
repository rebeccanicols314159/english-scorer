"""Spelling analyzer using pyspellchecker.

Calculates spelling error rate → score.
Proper nouns (capitalised mid-sentence) and acronyms are excluded.
"""
from nltk.tokenize import word_tokenize, sent_tokenize
from spellchecker import SpellChecker
from .base import BaseAnalyzer

_spell = SpellChecker()


def _candidate_words(text: str) -> list[str]:
    """Return lowercase alpha words that should be spell-checked.

    Skips:
    - All-caps tokens (acronyms)
    - Words capitalised at the start of a sentence (potential proper nouns)
    """
    sentences = sent_tokenize(text)
    skip_first = set()
    for sent in sentences:
        tokens = word_tokenize(sent)
        alpha = [t for t in tokens if t.isalpha()]
        if alpha:
            skip_first.add(alpha[0].lower())  # first word of each sentence

    results = []
    for token in word_tokenize(text):
        if not token.isalpha():
            continue
        if token.isupper():          # acronym
            continue
        if token[0].isupper() and token.lower() in skip_first:
            continue                  # sentence-initial word — likely proper noun
        results.append(token.lower())
    return results


class SpellingAnalyzer(BaseAnalyzer):
    def get_diagnostics(self, text: str) -> dict:
        candidates = _candidate_words(text)
        word_count = max(len(candidates), 1)
        misspelled = _spell.unknown(candidates)
        error_count = len(misspelled)
        error_rate = round((error_count / word_count) * 100, 2)
        return {"error_count": error_count, "error_rate": error_rate}

    def analyze(self, text: str) -> float:
        candidates = _candidate_words(text)
        word_count = max(len(candidates), 1)

        misspelled = _spell.unknown(candidates)
        error_rate = (len(misspelled) / word_count) * 100

        score = self._error_rate_to_score(error_rate)
        return round(score, 1)
