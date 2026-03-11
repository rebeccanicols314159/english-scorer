"""Tests for the dummy scoring engine."""
import pytest
from unittest.mock import patch
import app.scoring.engine as engine_module
from app.scoring.engine import (
    count_words,
    count_sentences,
    get_confidence_level,
    get_proficiency_level,
    compute_subcategory_scores,
    compute_all_diagnostics,
    compute_overall_score,
    WEIGHTS,
)


class TestCountWords:
    def test_simple_sentence(self):
        assert count_words("Hello world this is a test") == 6

    def test_empty_string(self):
        assert count_words("") == 0

    def test_extra_whitespace(self):
        assert count_words("  hello   world  ") == 2


class TestCountSentences:
    def test_single_sentence(self):
        assert count_sentences("This is one sentence.") == 1

    def test_multiple_sentences(self):
        assert count_sentences("First sentence. Second sentence. Third one!") == 3

    def test_question_and_exclamation(self):
        assert count_sentences("Really? Yes! Absolutely.") == 3

    def test_empty_string_returns_zero(self):
        assert count_sentences("") == 0


class TestGetConfidenceLevel:
    def test_very_short_text_is_low(self):
        assert get_confidence_level(15) == "low"

    def test_at_threshold_30_is_medium(self):
        assert get_confidence_level(30) == "medium"

    def test_medium_range(self):
        assert get_confidence_level(75) == "medium"

    def test_at_threshold_100_is_high(self):
        assert get_confidence_level(100) == "high"

    def test_high_range(self):
        assert get_confidence_level(250) == "high"

    def test_at_threshold_500_is_very_high(self):
        assert get_confidence_level(500) == "very_high"

    def test_long_text_is_very_high(self):
        assert get_confidence_level(1500) == "very_high"


class TestGetProficiencyLevel:
    def test_score_1_is_beginner(self):
        assert get_proficiency_level(1.0) == "Beginner"

    def test_score_2_is_beginner(self):
        assert get_proficiency_level(2.0) == "Beginner"

    def test_score_2_1_is_elementary(self):
        assert get_proficiency_level(2.1) == "Elementary"

    def test_score_3_5_is_elementary(self):
        assert get_proficiency_level(3.5) == "Elementary"

    def test_score_3_6_is_pre_intermediate(self):
        assert get_proficiency_level(3.6) == "Pre-Intermediate"

    def test_score_5_is_pre_intermediate(self):
        assert get_proficiency_level(5.0) == "Pre-Intermediate"

    def test_score_5_1_is_intermediate(self):
        assert get_proficiency_level(5.1) == "Intermediate"

    def test_score_6_5_is_intermediate(self):
        assert get_proficiency_level(6.5) == "Intermediate"

    def test_score_6_6_is_upper_intermediate(self):
        assert get_proficiency_level(6.6) == "Upper-Intermediate"

    def test_score_7_5_is_upper_intermediate(self):
        assert get_proficiency_level(7.5) == "Upper-Intermediate"

    def test_score_7_6_is_advanced(self):
        assert get_proficiency_level(7.6) == "Advanced"

    def test_score_8_5_is_advanced(self):
        assert get_proficiency_level(8.5) == "Advanced"

    def test_score_8_6_is_proficient(self):
        assert get_proficiency_level(8.6) == "Proficient"

    def test_score_10_is_proficient(self):
        assert get_proficiency_level(10.0) == "Proficient"


class TestWeights:
    def test_weights_sum_to_one(self):
        total = sum(WEIGHTS.values())
        assert abs(total - 1.0) < 0.0001

    def test_grammar_weight_is_25_percent(self):
        assert WEIGHTS["grammar"] == pytest.approx(0.25)

    def test_vocabulary_weight_is_20_percent(self):
        assert WEIGHTS["vocabulary"] == pytest.approx(0.20)

    def test_spelling_weight_is_10_percent(self):
        assert WEIGHTS["spelling_mechanics"] == pytest.approx(0.10)

    def test_sentence_structure_weight_is_20_percent(self):
        assert WEIGHTS["sentence_structure"] == pytest.approx(0.20)

    def test_coherence_weight_is_15_percent(self):
        assert WEIGHTS["coherence_organization"] == pytest.approx(0.15)

    def test_fluency_weight_is_10_percent(self):
        assert WEIGHTS["fluency_naturalness"] == pytest.approx(0.10)


SAMPLE_TEXT_SHORT = "I go to store yesterday. She don't like cats."
SAMPLE_TEXT_MEDIUM = (
    "The quick brown fox jumps over the lazy dog. "
    "This sentence demonstrates a variety of words. "
    "English learners often struggle with grammar rules. "
    "However, practice makes perfect in language learning. "
    "Reading and writing regularly can improve your skills significantly."
)
SAMPLE_TEXT_LONG = " ".join([
    "The study of English as a second language presents numerous challenges for learners worldwide.",
    "Grammar rules, vocabulary acquisition, and pronunciation all require dedicated practice.",
    "Moreover, understanding idiomatic expressions adds another layer of complexity.",
    "Nevertheless, many learners achieve high proficiency through consistent effort.",
    "Technology has transformed language learning in remarkable ways.",
    "Online platforms offer immediate feedback that was previously unavailable.",
    "Furthermore, exposure to authentic materials helps develop natural fluency.",
    "Consequently, modern learners have unprecedented access to resources.",
    "In conclusion, while English acquisition demands significant effort, the rewards are substantial.",
    "The ability to communicate globally opens countless professional and personal opportunities.",
] * 6)


class TestComputeSubcategoryScores:
    def test_returns_all_six_categories(self):
        scores = compute_subcategory_scores(SAMPLE_TEXT_MEDIUM)
        assert set(scores.keys()) == {
            "grammar", "vocabulary", "spelling_mechanics",
            "sentence_structure", "coherence_organization", "fluency_naturalness"
        }

    def test_all_scores_are_between_1_and_10(self):
        scores = compute_subcategory_scores(SAMPLE_TEXT_MEDIUM)
        for category, score in scores.items():
            assert 1.0 <= score <= 10.0, f"{category} score {score} out of range"

    def test_scores_for_short_text_also_in_range(self):
        scores = compute_subcategory_scores(SAMPLE_TEXT_SHORT)
        for category, score in scores.items():
            assert 1.0 <= score <= 10.0, f"{category} score {score} out of range"

    def test_scores_for_long_text_in_range(self):
        scores = compute_subcategory_scores(SAMPLE_TEXT_LONG)
        for category, score in scores.items():
            assert 1.0 <= score <= 10.0, f"{category} score {score} out of range"

    def test_scores_are_deterministic(self):
        scores1 = compute_subcategory_scores(SAMPLE_TEXT_MEDIUM)
        scores2 = compute_subcategory_scores(SAMPLE_TEXT_MEDIUM)
        assert scores1 == scores2

    def test_short_text_has_lower_coherence(self):
        # Coherence requires 50+ words; short text should score lower
        short_scores = compute_subcategory_scores("I like cats. Dogs are good.")
        medium_scores = compute_subcategory_scores(SAMPLE_TEXT_LONG)
        assert short_scores["coherence_organization"] < medium_scores["coherence_organization"]

    def test_scores_are_rounded_to_one_decimal(self):
        scores = compute_subcategory_scores(SAMPLE_TEXT_MEDIUM)
        for score in scores.values():
            assert score == round(score, 1)


class TestComputeOverallScore:
    def test_overall_score_is_weighted_average(self):
        subcategory_scores = {
            "grammar": 8.0,
            "vocabulary": 6.0,
            "spelling_mechanics": 10.0,
            "sentence_structure": 7.0,
            "coherence_organization": 5.0,
            "fluency_naturalness": 4.0,
        }
        expected = (
            8.0 * 0.25 + 6.0 * 0.20 + 10.0 * 0.10 +
            7.0 * 0.20 + 5.0 * 0.15 + 4.0 * 0.10
        )
        result = compute_overall_score(subcategory_scores)
        assert result == pytest.approx(expected, abs=0.05)

    def test_overall_score_is_between_1_and_10(self):
        subcategory_scores = {k: 5.0 for k in WEIGHTS}
        score = compute_overall_score(subcategory_scores)
        assert 1.0 <= score <= 10.0

    def test_all_tens_gives_overall_ten(self):
        subcategory_scores = {k: 10.0 for k in WEIGHTS}
        score = compute_overall_score(subcategory_scores)
        assert score == pytest.approx(10.0, abs=0.05)

    def test_all_ones_gives_overall_one(self):
        subcategory_scores = {k: 1.0 for k in WEIGHTS}
        score = compute_overall_score(subcategory_scores)
        assert score == pytest.approx(1.0, abs=0.05)


class TestAnalyzerFailureRecovery:
    def test_failed_analyzer_returns_fallback_score(self):
        with patch.object(engine_module._grammar, "analyze", side_effect=RuntimeError("NLP failure")):
            scores = compute_subcategory_scores(SAMPLE_TEXT_MEDIUM)
        assert scores["grammar"] == 5.0

    def test_other_scores_unaffected_by_failed_analyzer(self):
        with patch.object(engine_module._grammar, "analyze", side_effect=RuntimeError("NLP failure")):
            scores = compute_subcategory_scores(SAMPLE_TEXT_MEDIUM)
        for cat in ["vocabulary", "spelling_mechanics", "sentence_structure", "coherence_organization", "fluency_naturalness"]:
            assert 1.0 <= scores[cat] <= 10.0, f"{cat} score {scores[cat]} out of range"

    def test_failed_diagnostics_returns_empty_dict(self):
        with patch.object(engine_module._grammar, "get_diagnostics", side_effect=RuntimeError("NLP failure")):
            diag = compute_all_diagnostics(SAMPLE_TEXT_MEDIUM)
        assert diag["grammar"] == {}

    def test_other_diagnostics_unaffected_by_failed_analyzer(self):
        with patch.object(engine_module._grammar, "get_diagnostics", side_effect=RuntimeError("NLP failure")):
            diag = compute_all_diagnostics(SAMPLE_TEXT_MEDIUM)
        for cat in ["vocabulary", "spelling_mechanics", "sentence_structure", "coherence_organization", "fluency_naturalness"]:
            assert isinstance(diag[cat], dict)
