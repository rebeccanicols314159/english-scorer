"""Tests for the enhanced, diagnostics-aware feedback generator."""
import re
import pytest
from app.scoring.feedback import generate_feedback

CATEGORIES = [
    "grammar", "vocabulary", "spelling_mechanics",
    "sentence_structure", "coherence_organization", "fluency_naturalness",
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def sentence_count(text: str) -> int:
    return len([s for s in re.split(r"[.!?]+", text) if s.strip()])


def scores_at(value: float) -> dict[str, float]:
    return {k: value for k in CATEGORIES}


# ── Format invariants ─────────────────────────────────────────────────────────

class TestFeedbackFormat:
    def test_returns_all_six_categories(self):
        fb = generate_feedback(scores_at(6.0))
        assert set(fb.keys()) == set(CATEGORIES)

    def test_each_value_is_a_non_empty_string(self):
        fb = generate_feedback(scores_at(6.0))
        for cat, text in fb.items():
            assert isinstance(text, str) and len(text) > 0, cat

    def test_feedback_is_1_to_3_sentences(self):
        for score in (2.0, 5.0, 9.0):
            fb = generate_feedback(scores_at(score))
            for cat, text in fb.items():
                sc = sentence_count(text)
                assert 1 <= sc <= 3, f"{cat} at {score}: '{text}'"

    def test_feedback_with_no_diagnostics_still_works(self):
        fb = generate_feedback(scores_at(5.0))
        assert len(fb) == 6


# ── Tone by score tier ────────────────────────────────────────────────────────

class TestFeedbackTone:
    def test_high_score_grammar_contains_positive_language(self):
        fb = generate_feedback({"grammar": 9.0, **{k: 5.0 for k in CATEGORIES if k != "grammar"}})
        assert any(w in fb["grammar"].lower() for w in ("excellent", "great", "strong", "impressive", "accurate"))

    def test_medium_score_grammar_contains_encouraging_language(self):
        fb = generate_feedback({"grammar": 6.0, **{k: 5.0 for k in CATEGORIES if k != "grammar"}})
        assert any(w in fb["grammar"].lower() for w in ("good", "progress", "improving", "developing"))

    def test_low_score_grammar_contains_actionable_language(self):
        fb = generate_feedback({"grammar": 3.0, **{k: 5.0 for k in CATEGORIES if k != "grammar"}})
        assert any(w in fb["grammar"].lower() for w in ("focus", "work", "practise", "practice", "review", "start"))

    def test_high_score_spelling_contains_positive_language(self):
        fb = generate_feedback({"spelling_mechanics": 9.0, **{k: 5.0 for k in CATEGORIES if k != "spelling_mechanics"}})
        assert any(w in fb["spelling_mechanics"].lower() for w in ("excellent", "great", "impeccable", "accurate", "strong"))

    def test_low_score_vocabulary_contains_actionable_language(self):
        fb = generate_feedback({"vocabulary": 2.0, **{k: 5.0 for k in CATEGORIES if k != "vocabulary"}})
        assert any(w in fb["vocabulary"].lower() for w in ("expand", "varied", "variety", "diverse", "repetition", "synonyms"))


# ── Personalisation with diagnostics ─────────────────────────────────────────

class TestFeedbackPersonalisation:
    def test_spelling_feedback_mentions_error_count_when_errors_found(self):
        diag = {"spelling_mechanics": {"error_count": 5, "error_rate": 8.0}}
        fb = generate_feedback({"spelling_mechanics": 4.0, **{k: 5.0 for k in CATEGORIES if k != "spelling_mechanics"}},
                               diagnostics=diag)
        assert "5" in fb["spelling_mechanics"]

    def test_grammar_feedback_mentions_agreement_when_detected(self):
        diag = {"grammar": {"error_count": 3, "error_types": ["agreement"]}}
        fb = generate_feedback({"grammar": 5.0, **{k: 5.0 for k in CATEGORIES if k != "grammar"}},
                               diagnostics=diag)
        assert any(w in fb["grammar"].lower() for w in ("agreement", "subject", "verb"))

    def test_coherence_feedback_mentions_transitions_when_few(self):
        diag = {"coherence_organization": {"transition_count": 0, "word_count": 120}}
        fb = generate_feedback({"coherence_organization": 3.0, **{k: 5.0 for k in CATEGORIES if k != "coherence_organization"}},
                               diagnostics=diag)
        assert any(w in fb["coherence_organization"].lower()
                   for w in ("transition", "connector", "however", "furthermore", "link"))

    def test_vocabulary_feedback_mentions_variety_when_low_ttr(self):
        diag = {"vocabulary": {"ttr": 0.28, "avg_word_length": 4.1}}
        fb = generate_feedback({"vocabulary": 3.0, **{k: 5.0 for k in CATEGORIES if k != "vocabulary"}},
                               diagnostics=diag)
        assert any(w in fb["vocabulary"].lower()
                   for w in ("repetit", "varied", "variety", "diverse", "synonyms"))

    def test_sentence_feedback_mentions_length_when_sentences_too_short(self):
        diag = {"sentence_structure": {"avg_sentence_length": 5.0, "sentence_count": 6, "complex_ratio": 0.1}}
        fb = generate_feedback({"sentence_structure": 4.0, **{k: 5.0 for k in CATEGORIES if k != "sentence_structure"}},
                               diagnostics=diag)
        assert any(w in fb["sentence_structure"].lower()
                   for w in ("short", "variety", "complex", "longer", "combine"))

    def test_diagnostics_none_falls_back_to_template(self):
        # No diagnostics → static template, should still be valid
        fb = generate_feedback(scores_at(5.0), diagnostics=None)
        assert all(len(v) > 0 for v in fb.values())


# ── Engine integration: feedback uses real diagnostics ────────────────────────

class TestFeedbackEngineIntegration:
    def test_engine_produces_personalized_feedback(self):
        """Score + generate_feedback from real engine output passes format checks."""
        from app.scoring.engine import compute_subcategory_scores, compute_all_diagnostics
        from tests.scoring.fixtures import BEGINNER_TEXT

        scores = compute_subcategory_scores(BEGINNER_TEXT)
        diag = compute_all_diagnostics(BEGINNER_TEXT)
        fb = generate_feedback(scores, diagnostics=diag)

        for cat, text in fb.items():
            assert isinstance(text, str) and len(text) > 0
            sc = sentence_count(text)
            assert 1 <= sc <= 3, f"{cat}: '{text}'"
