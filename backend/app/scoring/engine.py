"""Dummy scoring engine using simple text heuristics.

This is a placeholder implementation. It uses basic text statistics to
produce deterministic scores in the 1–10 range. Replace with real NLP
analysis (spaCy, LanguageTool, etc.) in a future phase.
"""
import re

WEIGHTS: dict[str, float] = {
    "grammar": 0.25,
    "vocabulary": 0.20,
    "spelling_mechanics": 0.10,
    "sentence_structure": 0.20,
    "coherence_organization": 0.15,
    "fluency_naturalness": 0.10,
}

_TRANSITION_WORDS = {
    "however", "therefore", "furthermore", "moreover", "additionally",
    "consequently", "nevertheless", "in addition", "on the other hand",
    "for example", "for instance", "in conclusion", "first", "second",
    "third", "finally", "meanwhile", "subsequently", "in contrast",
    "similarly", "as a result", "in summary", "thus", "hence",
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


def count_words(text: str) -> int:
    return len(text.split())


def count_sentences(text: str) -> int:
    sentences = re.split(r"[.!?]+", text)
    return len([s for s in sentences if s.strip()])


def _type_token_ratio(text: str) -> float:
    words = text.lower().split()
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def _avg_sentence_length(text: str) -> float:
    wc = count_words(text)
    sc = count_sentences(text)
    return wc / max(sc, 1)


def _count_transition_words(text: str) -> int:
    text_lower = text.lower()
    return sum(1 for t in _TRANSITION_WORDS if t in text_lower)


def _clamp(value: float, min_val: float = 1.0, max_val: float = 10.0) -> float:
    return max(min_val, min(max_val, value))


def compute_subcategory_scores(text: str) -> dict[str, float]:
    word_count = count_words(text)
    sentence_count = count_sentences(text)
    ttr = _type_token_ratio(text)
    avg_len = _avg_sentence_length(text)
    transitions = _count_transition_words(text)

    # Grammar: blends TTR diversity with text length maturity.
    # Real implementation would use LanguageTool error counts.
    grammar = _clamp(4.0 + ttr * 4.0 + min(word_count, 300) / 300 * 2.0)

    # Vocabulary: type-token ratio is the primary proxy.
    # TTR typically ranges 0.3–0.95; map to 1–10.
    vocab = _clamp((ttr - 0.3) / 0.65 * 9.0 + 1.0)

    # Spelling & Mechanics: dummy assumes mostly correct text; docked
    # slightly for very short submissions with no punctuation variety.
    spelling = _clamp(8.5 - (2.0 if sentence_count < 2 else 0.0))

    # Sentence Structure: penalise deviation from ideal avg length (17 words).
    deviation = abs(avg_len - 17.0)
    sentence_structure = _clamp(9.5 - deviation * 0.25)

    # Coherence & Organization: requires 50+ words; rewards transitions.
    if word_count < 50:
        coherence = _clamp(2.0 + word_count / 50.0 * 3.0)
    else:
        transition_bonus = min(transitions * 0.6, 3.0)
        length_bonus = min(word_count / 500.0, 1.0)
        coherence = _clamp(5.0 + transition_bonus + length_bonus)

    # Fluency & Naturalness: combines TTR with sentence variety.
    sentence_variety_bonus = min(sentence_count / 5.0, 1.0) * 2.0
    fluency = _clamp(3.5 + ttr * 4.0 + sentence_variety_bonus)

    return {
        "grammar": round(grammar, 1),
        "vocabulary": round(vocab, 1),
        "spelling_mechanics": round(spelling, 1),
        "sentence_structure": round(sentence_structure, 1),
        "coherence_organization": round(coherence, 1),
        "fluency_naturalness": round(fluency, 1),
    }


def compute_overall_score(subcategory_scores: dict[str, float]) -> float:
    total = sum(subcategory_scores[cat] * weight for cat, weight in WEIGHTS.items())
    return round(total, 1)


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
