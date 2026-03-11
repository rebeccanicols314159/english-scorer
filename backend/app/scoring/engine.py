"""Scoring engine — orchestrates the six NLP analyzers.

Public API is unchanged from the dummy engine so all existing tests pass.
Utility functions (count_words, count_sentences, get_confidence_level,
get_proficiency_level) are preserved verbatim.
"""
import re
from app.scoring.analyzers.grammar import GrammarAnalyzer
from app.scoring.analyzers.vocabulary import VocabularyAnalyzer
from app.scoring.analyzers.spelling import SpellingAnalyzer
from app.scoring.analyzers.sentence import SentenceStructureAnalyzer
from app.scoring.analyzers.coherence import CoherenceAnalyzer
from app.scoring.analyzers.fluency import FluencyAnalyzer

WEIGHTS: dict[str, float] = {
    "grammar": 0.25,
    "vocabulary": 0.20,
    "spelling_mechanics": 0.10,
    "sentence_structure": 0.20,
    "coherence_organization": 0.15,
    "fluency_naturalness": 0.10,
}

_PROFICIENCY_LEVELS = [
    (2.0, "Beginner"),
    (3.5, "Elementary"),
    (5.0, "Pre-Intermediate"),
    (6.5, "Intermediate"),
    (7.5, "Upper-Intermediate"),
    (8.5, "Advanced"),
    (10.0, "Proficient"),
]

# Instantiate analyzers once at module level (no re-loading on each request)
_grammar = GrammarAnalyzer()
_vocabulary = VocabularyAnalyzer()
_spelling = SpellingAnalyzer()
_sentence = SentenceStructureAnalyzer()
_coherence = CoherenceAnalyzer()
_fluency = FluencyAnalyzer()


# ── Utility functions (unchanged public API) ──────────────────────────────────

def count_words(text: str) -> int:
    return len(text.split())


def count_sentences(text: str) -> int:
    sentences = re.split(r"[.!?]+", text)
    return len([s for s in sentences if s.strip()])


def get_confidence_level(word_count: int) -> str:
    if word_count < 30:
        return "low"
    if word_count < 100:
        return "medium"
    if word_count < 500:
        return "high"
    return "very_high"


def get_proficiency_level(score: float) -> str:
    for threshold, label in _PROFICIENCY_LEVELS:
        if score <= threshold:
            return label
    return "Proficient"


# ── Core scoring functions ─────────────────────────────────────────────────────

_FALLBACK_SCORE = 5.0

_ANALYZERS = [
    ("grammar",                _grammar),
    ("vocabulary",             _vocabulary),
    ("spelling_mechanics",     _spelling),
    ("sentence_structure",     _sentence),
    ("coherence_organization", _coherence),
    ("fluency_naturalness",    _fluency),
]


def compute_subcategory_scores(text: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    for name, analyzer in _ANALYZERS:
        try:
            scores[name] = analyzer.analyze(text)
        except Exception:
            scores[name] = _FALLBACK_SCORE
    return scores


def compute_all_diagnostics(text: str) -> dict[str, dict]:
    diagnostics: dict[str, dict] = {}
    for name, analyzer in _ANALYZERS:
        try:
            diagnostics[name] = analyzer.get_diagnostics(text)
        except Exception:
            diagnostics[name] = {}
    return diagnostics


def compute_overall_score(subcategory_scores: dict[str, float]) -> float:
    total = sum(subcategory_scores[cat] * weight for cat, weight in WEIGHTS.items())
    return round(total, 1)
