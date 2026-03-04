"""Tests for the feedback generator."""
import pytest
from app.scoring.feedback import generate_feedback, FEEDBACK_TEMPLATES


CATEGORIES = [
    "grammar", "vocabulary", "spelling_mechanics",
    "sentence_structure", "coherence_organization", "fluency_naturalness",
]


class TestFeedbackTemplates:
    def test_templates_exist_for_all_categories(self):
        for category in CATEGORIES:
            assert category in FEEDBACK_TEMPLATES

    def test_each_category_has_high_medium_low_tiers(self):
        for category in CATEGORIES:
            assert "high" in FEEDBACK_TEMPLATES[category]
            assert "medium" in FEEDBACK_TEMPLATES[category]
            assert "low" in FEEDBACK_TEMPLATES[category]

    def test_all_templates_are_non_empty_strings(self):
        for category, tiers in FEEDBACK_TEMPLATES.items():
            for tier, text in tiers.items():
                assert isinstance(text, str)
                assert len(text) > 0, f"Empty template for {category}/{tier}"


class TestGenerateFeedback:
    def test_returns_feedback_for_all_categories(self):
        subcategory_scores = {k: 5.0 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        for category in CATEGORIES:
            assert category in feedback

    def test_high_score_gives_high_tier_feedback(self):
        subcategory_scores = {k: 9.0 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        expected = FEEDBACK_TEMPLATES["grammar"]["high"]
        assert feedback["grammar"] == expected

    def test_medium_score_gives_medium_tier_feedback(self):
        subcategory_scores = {k: 6.0 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        expected = FEEDBACK_TEMPLATES["vocabulary"]["medium"]
        assert feedback["vocabulary"] == expected

    def test_low_score_gives_low_tier_feedback(self):
        subcategory_scores = {k: 2.0 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        expected = FEEDBACK_TEMPLATES["sentence_structure"]["low"]
        assert feedback["sentence_structure"] == expected

    def test_score_7_5_is_high_tier(self):
        # Score >= 7.5 should give high tier feedback
        subcategory_scores = {k: 7.5 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        assert feedback["grammar"] == FEEDBACK_TEMPLATES["grammar"]["high"]

    def test_score_4_5_is_medium_tier(self):
        # Score 4.5–7.4 should give medium tier feedback
        subcategory_scores = {k: 4.5 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        assert feedback["grammar"] == FEEDBACK_TEMPLATES["grammar"]["medium"]

    def test_score_4_4_is_low_tier(self):
        # Score < 4.5 should give low tier feedback
        subcategory_scores = {k: 4.4 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        assert feedback["grammar"] == FEEDBACK_TEMPLATES["grammar"]["low"]

    def test_feedback_values_are_strings(self):
        subcategory_scores = {k: 5.0 for k in CATEGORIES}
        feedback = generate_feedback(subcategory_scores)
        for category, text in feedback.items():
            assert isinstance(text, str)
