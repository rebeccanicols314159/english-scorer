"""Tests for the fluency and naturalness analyzer."""
import pytest
from tests.scoring.fixtures import ADVANCED_TEXT, BEGINNER_TEXT, INTERMEDIATE_TEXT
from app.scoring.analyzers.fluency import FluencyAnalyzer

analyzer = FluencyAnalyzer()


class TestFluencyAnalyzerInvariants:
    def test_score_is_between_1_and_10(self):
        assert 1.0 <= analyzer.analyze(INTERMEDIATE_TEXT) <= 10.0

    def test_score_is_deterministic(self):
        assert analyzer.analyze(ADVANCED_TEXT) == analyzer.analyze(ADVANCED_TEXT)

    def test_score_is_rounded_to_one_decimal(self):
        score = analyzer.analyze(ADVANCED_TEXT)
        assert score == round(score, 1)


class TestFluencyAnalyzerComparative:
    def test_advanced_scores_higher_than_beginner(self):
        assert analyzer.analyze(ADVANCED_TEXT) > analyzer.analyze(BEGINNER_TEXT)

    def test_intermediate_scores_higher_than_beginner(self):
        assert analyzer.analyze(INTERMEDIATE_TEXT) > analyzer.analyze(BEGINNER_TEXT)

    def test_advanced_text_scores_reasonably(self):
        assert analyzer.analyze(ADVANCED_TEXT) >= 5.0
