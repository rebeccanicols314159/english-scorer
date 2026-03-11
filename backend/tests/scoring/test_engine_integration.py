"""Integration tests: real analyzers wired into the engine."""
import pytest
from tests.scoring.fixtures import ADVANCED_TEXT, BEGINNER_TEXT, INTERMEDIATE_TEXT
from app.scoring.engine import compute_subcategory_scores, compute_overall_score, WEIGHTS

CATEGORIES = list(WEIGHTS.keys())


class TestEngineIntegration:
    def test_returns_all_six_subcategory_scores(self):
        scores = compute_subcategory_scores(INTERMEDIATE_TEXT)
        assert set(scores.keys()) == set(CATEGORIES)

    def test_all_subcategory_scores_in_range(self):
        scores = compute_subcategory_scores(ADVANCED_TEXT)
        for cat, score in scores.items():
            assert 1.0 <= score <= 10.0, f"{cat}={score} out of range"

    def test_overall_score_in_range(self):
        scores = compute_subcategory_scores(ADVANCED_TEXT)
        overall = compute_overall_score(scores)
        assert 1.0 <= overall <= 10.0

    def test_advanced_overall_higher_than_beginner(self):
        adv = compute_overall_score(compute_subcategory_scores(ADVANCED_TEXT))
        beg = compute_overall_score(compute_subcategory_scores(BEGINNER_TEXT))
        assert adv > beg

    def test_scores_are_deterministic(self):
        assert compute_subcategory_scores(ADVANCED_TEXT) == compute_subcategory_scores(ADVANCED_TEXT)

    def test_scores_rounded_to_one_decimal(self):
        scores = compute_subcategory_scores(ADVANCED_TEXT)
        for score in scores.values():
            assert score == round(score, 1)
