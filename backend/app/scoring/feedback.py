"""Template-based feedback generator for each scoring subcategory.

Feedback is selected by score tier:
  high   >= 7.5
  medium  4.5 – 7.4
  low    <  4.5
"""

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
            "Work on fundamental grammar rules, particularly subject-verb agreement "
            "and tense usage. Consider reviewing basic English grammar guides."
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
            "Expand your vocabulary by reading widely and using a thesaurus. "
            "Aim to reduce repetition of the same words."
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
            "Sentences tend to be too simple or repetitive. "
            "Practice writing compound and complex sentences using conjunctions "
            "like 'although', 'because', and 'however'."
        ),
    },
    "coherence_organization": {
        "high": (
            "Your writing flows logically with clear organisation and effective "
            "use of transition words to guide the reader."
        ),
        "medium": (
            "Good overall organisation. Use more transition words "
            "('furthermore', 'however', 'as a result') to connect ideas more smoothly."
        ),
        "low": (
            "Work on organising your ideas into clear paragraphs with a logical "
            "flow. Begin with a clear topic and use transitions between ideas."
        ),
    },
    "fluency_naturalness": {
        "high": (
            "Your writing reads naturally and fluently — very close to native-level expression."
        ),
        "medium": (
            "Generally natural phrasing. Focus on idiomatic expressions and "
            "collocations to sound more natural in English."
        ),
        "low": (
            "Some phrases feel unnatural or translated. "
            "Practise reading authentic English content to internalise natural phrasing."
        ),
    },
}


def _get_tier(score: float) -> str:
    if score >= 7.5:
        return "high"
    if score >= 4.5:
        return "medium"
    return "low"


def generate_feedback(subcategory_scores: dict[str, float]) -> dict[str, str]:
    return {
        category: FEEDBACK_TEMPLATES[category][_get_tier(score)]
        for category, score in subcategory_scores.items()
    }
