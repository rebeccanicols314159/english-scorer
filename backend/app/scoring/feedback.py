"""Personalised, diagnostics-aware feedback generator.

Architecture (from DESIGN.md):
  1. Select tone tier based on score (high ≥ 7.5 / medium 4.5–7.4 / low < 4.5)
  2. Inject diagnostic data (error counts, TTR, transition count, etc.)
  3. Return 1–3 sentences per subcategory, tone-adjusted

The `diagnostics` parameter is optional: omitting it falls back to the static
templates, preserving backward compatibility with existing callers.
"""
from __future__ import annotations


# ── Tone tier ─────────────────────────────────────────────────────────────────

def _tier(score: float) -> str:
    if score >= 7.5:
        return "high"
    if score >= 4.5:
        return "medium"
    return "low"


# ── Static fallback templates (preserved for backward-compat) ─────────────────

FEEDBACK_TEMPLATES: dict[str, dict[str, str]] = {
    "grammar": {
        "high": (
            "Excellent grammar with only minor issues. "
            "Your writing shows strong command of English grammar rules."
        ),
        "medium": (
            "Good grammar overall. Focus on tense consistency and article usage "
            "(a/an/the) to improve further."
        ),
        "low": (
            "Grammar needs work. Prioritise subject-verb agreement and consistent "
            "tense usage. Review basic grammar rules regularly."
        ),
    },
    "vocabulary": {
        "high": (
            "Impressive vocabulary range and variety. "
            "Your word choices are precise and varied — keep it up."
        ),
        "medium": (
            "Good vocabulary for everyday communication. "
            "Try incorporating more varied and advanced words to enrich your writing."
        ),
        "low": (
            "Expand your vocabulary by reading widely. "
            "Aim to reduce repetition and use synonyms to diversify your word choices."
        ),
    },
    "spelling_mechanics": {
        "high": (
            "Excellent spelling and punctuation throughout. "
            "Your mechanics are clean and professional."
        ),
        "medium": (
            "Mostly good spelling. Double-check punctuation — especially commas "
            "and apostrophes — to polish your writing."
        ),
        "low": (
            "Several spelling and punctuation errors detected. "
            "Use a spell-checker and review basic punctuation rules."
        ),
    },
    "sentence_structure": {
        "high": (
            "Great variety in sentence structure. "
            "You use a healthy mix of simple, compound, and complex sentences."
        ),
        "medium": (
            "Decent sentence structure. Try varying sentence length more — "
            "mix shorter punchy sentences with longer, more complex ones."
        ),
        "low": (
            "Work on sentence variety. "
            "Practise writing complex sentences using conjunctions like "
            "'although', 'because', and 'however', and combine short sentences."
        ),
    },
    "coherence_organization": {
        "high": (
            "Your writing flows logically with clear organisation and effective "
            "use of transition words to guide the reader."
        ),
        "medium": (
            "Good overall organisation. Use more transition words "
            "('furthermore', 'however', 'as a result') to link ideas more smoothly."
        ),
        "low": (
            "Work on organising your ideas logically. "
            "Use transition words and connectors like 'however', 'furthermore', "
            "and 'consequently' to link your sentences."
        ),
    },
    "fluency_naturalness": {
        "high": (
            "Your writing reads naturally and fluently — "
            "very close to native-level expression."
        ),
        "medium": (
            "Generally natural phrasing. Focus on idiomatic expressions and "
            "collocations to sound more natural in English."
        ),
        "low": (
            "Some phrases feel unnatural or over-simplified. "
            "Practise reading authentic English content to internalise "
            "natural phrasing and sentence rhythm."
        ),
    },
}


# ── Personalised feedback builders ────────────────────────────────────────────

def _grammar_feedback(score: float, diag: dict) -> str:
    t = _tier(score)
    error_types: list[str] = diag.get("error_types", [])

    if t == "high":
        return (
            "Excellent grammar — your writing shows strong command of "
            "English grammar rules. Keep up the great work."
        )
    if t == "medium":
        if "agreement" in error_types:
            return (
                "Good grammar overall. Watch for subject-verb agreement — "
                "for example, make sure 'he', 'she', and 'it' are followed "
                "by the correct verb form. Focus on tense consistency too."
            )
        return (
            "Good grammar overall. Focus on tense consistency and article "
            "usage (a/an/the) to improve further."
        )
    # low
    issues = " and ".join(
        {"agreement": "subject-verb agreement",
         "resumptive_pronoun": "avoiding repeated subject pronouns",
         "double_words": "removing accidental repeated words"}.get(e, e)
        for e in error_types[:2]
    ) or "subject-verb agreement and tense usage"
    return (
        f"Grammar needs work. Prioritise {issues}. "
        "Review basic grammar rules and practise writing correct sentences."
    )


def _vocabulary_feedback(score: float, diag: dict) -> str:
    t = _tier(score)
    ttr: float = diag.get("ttr", 0.6)

    if t == "high":
        return (
            "Impressive vocabulary range and variety. "
            "Your word choices are precise and varied — keep it up."
        )
    if t == "medium":
        return (
            "Good vocabulary for everyday communication. "
            "Try incorporating more varied and advanced words to enrich your writing."
        )
    # low
    if ttr < 0.4:
        return (
            "Your vocabulary needs more variety — many words are repeated frequently. "
            "Try using synonyms and consult a thesaurus to diversify your word choices."
        )
    return (
        "Expand your vocabulary by reading widely. "
        "Aim to reduce repetition and use more diverse, precise word choices."
    )


def _spelling_feedback(score: float, diag: dict) -> str:
    t = _tier(score)
    error_count: int = diag.get("error_count", 0)

    if t == "high":
        return (
            "Excellent spelling and punctuation throughout. "
            "Your mechanics are clean and accurate."
        )
    if t == "medium":
        if error_count > 0:
            return (
                f"{error_count} spelling error{'s' if error_count != 1 else ''} detected. "
                "Use a spell-checker before submitting and review any recurring mistakes."
            )
        return (
            "Mostly good spelling. Double-check punctuation — especially commas "
            "and apostrophes — to polish your writing."
        )
    # low
    if error_count > 0:
        return (
            f"{error_count} spelling errors detected. "
            "Use a spell-checker and focus on the most commonly misspelled words. "
            "Regular reading will help you internalise correct spellings."
        )
    return (
        "Several spelling and punctuation errors detected. "
        "Use a spell-checker and review basic punctuation rules."
    )


def _sentence_feedback(score: float, diag: dict) -> str:
    t = _tier(score)
    avg_len: float = diag.get("avg_sentence_length", 15.0)
    complex_ratio: float = diag.get("complex_ratio", 0.3)

    if t == "high":
        return (
            "Great variety in sentence structure. "
            "You use a healthy mix of simple, compound, and complex sentences."
        )
    if t == "medium":
        return (
            "Decent sentence structure. Try varying sentence length more — "
            "mix shorter punchy sentences with longer, more complex ones."
        )
    # low
    if avg_len < 8:
        return (
            f"Your sentences average only {avg_len:.0f} words — try writing longer, "
            "more detailed sentences. Combine short sentences using conjunctions "
            "like 'although', 'because', and 'which'."
        )
    if complex_ratio < 0.2:
        return (
            "Most sentences are simple in structure. Add variety by using complex "
            "sentences with subordinate clauses and connectors to show relationships "
            "between ideas."
        )
    return (
        "Work on sentence variety. Practise writing complex sentences and combine "
        "short sentences to improve the flow of your writing."
    )


def _coherence_feedback(score: float, diag: dict) -> str:
    t = _tier(score)
    transition_count: int = diag.get("transition_count", 0)
    word_count: int = diag.get("word_count", 100)

    if t == "high":
        return (
            "Your writing flows logically with clear organisation and effective "
            "use of transition words to guide the reader."
        )
    if t == "medium":
        return (
            "Good overall organisation. Use more transition words "
            "('furthermore', 'however', 'as a result') to link ideas more smoothly."
        )
    # low
    if word_count < 50:
        return (
            "Submit longer text for a reliable coherence assessment. "
            "When writing more, organise ideas into clear paragraphs and use "
            "transitions like 'however', 'furthermore', and 'consequently'."
        )
    if transition_count == 0:
        return (
            "No transition words were detected. Use connectors like 'however', "
            "'furthermore', 'consequently', and 'in addition' to link your ideas "
            "and improve the logical flow of your writing."
        )
    return (
        f"Only {transition_count} transition word{'s' if transition_count != 1 else ''} found. "
        "Use more connectors like 'however', 'furthermore', and 'as a result' "
        "to improve the logical flow between your ideas."
    )


def _fluency_feedback(score: float, diag: dict) -> str:
    t = _tier(score)
    fre: float = diag.get("fre", 55.0)

    if t == "high":
        return (
            "Your writing reads naturally and fluently — "
            "very close to native-level expression."
        )
    if t == "medium":
        if fre > 70:
            return (
                "Your writing is clear and easy to follow. To sound more fluent, "
                "try using more complex sentence patterns and a wider range of vocabulary."
            )
        return (
            "Generally natural phrasing. Focus on idiomatic expressions and "
            "collocations to sound more natural in English."
        )
    # low
    if fre > 80:
        return (
            "Your writing is very simple in style. Work on using more varied "
            "sentence structures and a broader vocabulary to sound more fluent."
        )
    return (
        "Some phrases feel unnatural or over-simplified. "
        "Practise reading authentic English content to internalise "
        "natural phrasing and improve the rhythm of your writing."
    )


# ── Category dispatch ─────────────────────────────────────────────────────────

_BUILDERS = {
    "grammar":                _grammar_feedback,
    "vocabulary":             _vocabulary_feedback,
    "spelling_mechanics":     _spelling_feedback,
    "sentence_structure":     _sentence_feedback,
    "coherence_organization": _coherence_feedback,
    "fluency_naturalness":    _fluency_feedback,
}


# ── Public API ────────────────────────────────────────────────────────────────

def generate_feedback(
    subcategory_scores: dict[str, float],
    diagnostics: dict[str, dict] | None = None,
) -> dict[str, str]:
    """Generate personalised feedback for each subcategory.

    Args:
        subcategory_scores: Mapping of category name → score (1–10).
        diagnostics: Optional mapping of category name → diagnostic dict.
                     When omitted, falls back to static templates.
    """
    result: dict[str, str] = {}
    diag = diagnostics or {}

    for category, score in subcategory_scores.items():
        builder = _BUILDERS.get(category)
        if builder:
            result[category] = builder(score, diag.get(category, {}))
        else:
            t = _tier(score)
            result[category] = FEEDBACK_TEMPLATES.get(category, {}).get(t, "")

    return result
