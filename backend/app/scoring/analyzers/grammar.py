"""Grammar analyzer using NLTK POS tagging and pattern matching.

Detects:
- Double words ("the the", "is is")
- Subject-verb agreement errors (he/she/it + VBP, I/we/they + VBZ)
- Sentences starting with a lowercase letter (after filtering known exceptions)

Designed for easy substitution with spaCy + LanguageTool once available.
"""
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from .base import BaseAnalyzer

# Pronouns that require 3rd-person singular verb (VBZ: walks, goes)
_SINGULAR_SUBJECTS = {"he", "she", "it"}
# Pronouns that require base-form verb (VBP: walk, go) — NOT VBZ
_PLURAL_SUBJECTS = {"i", "we", "they", "you"}

_DOUBLE_WORD_RE = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)

# "My friend he…", "The teacher she…" — resumptive pronoun after a noun phrase
_RESUMPTIVE_RE = re.compile(
    r"\b(?:the|my|your|his|her|our|their)\s+\w+\s+(he|she|they|it)\b",
    re.IGNORECASE,
)


def _count_double_words(text: str) -> int:
    return len(_DOUBLE_WORD_RE.findall(text))


def _count_resumptive_pronouns(text: str) -> int:
    return len(_RESUMPTIVE_RE.findall(text))


def _count_agreement_errors(text: str) -> int:
    errors = 0
    for sent in sent_tokenize(text):
        tokens = word_tokenize(sent)
        tagged = pos_tag(tokens)
        for i, (word, tag) in enumerate(tagged[:-1]):
            next_tag = tagged[i + 1][1]
            w = word.lower()
            if w in _SINGULAR_SUBJECTS and next_tag == "VBP":
                errors += 1
            if w in _PLURAL_SUBJECTS and next_tag == "VBZ":
                errors += 1
    return errors


def _count_lowercase_sentence_starts(text: str) -> int:
    errors = 0
    for sent in sent_tokenize(text):
        stripped = sent.strip()
        if stripped and stripped[0].islower():
            errors += 1
    return errors


class GrammarAnalyzer(BaseAnalyzer):
    def get_diagnostics(self, text: str) -> dict:
        words = word_tokenize(text)
        word_count = max(len(words), 1)
        double = _count_double_words(text)
        agreement = _count_agreement_errors(text)
        resumptive = _count_resumptive_pronouns(text)
        lowercase = _count_lowercase_sentence_starts(text)

        error_types: list[str] = []
        if agreement > 0:
            error_types.append("agreement")
        if double > 0:
            error_types.append("double_words")
        if resumptive > 0:
            error_types.append("resumptive_pronoun")
        if lowercase > 0:
            error_types.append("capitalisation")

        total_errors = double * 2 + agreement + resumptive * 2 + lowercase
        return {
            "error_count": total_errors,
            "error_types": error_types,
        }

    def analyze(self, text: str) -> float:
        words = word_tokenize(text)
        word_count = max(len(words), 1)

        errors = (
            _count_double_words(text) * 2
            + _count_agreement_errors(text)
            + _count_lowercase_sentence_starts(text)
            + _count_resumptive_pronouns(text) * 2
        )

        error_rate = (errors / word_count) * 100
        score = self._error_rate_to_score(error_rate)
        return round(score, 1)
