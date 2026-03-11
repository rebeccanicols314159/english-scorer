"""Tests for the coherence and organisation analyzer."""
import pytest
from tests.scoring.fixtures import COHERENT_TEXT, SHORT_TEXT, ADVANCED_TEXT, BEGINNER_TEXT
from app.scoring.analyzers.coherence import CoherenceAnalyzer

analyzer = CoherenceAnalyzer()


class TestCoherenceAnalyzerInvariants:
    def test_score_is_between_1_and_10(self):
        assert 1.0 <= analyzer.analyze(ADVANCED_TEXT) <= 10.0

    def test_score_is_deterministic(self):
        assert analyzer.analyze(COHERENT_TEXT) == analyzer.analyze(COHERENT_TEXT)

    def test_score_is_rounded_to_one_decimal(self):
        score = analyzer.analyze(ADVANCED_TEXT)
        assert score == round(score, 1)


class TestCoherenceAnalyzerComparative:
    def test_text_with_transitions_scores_higher_than_without(self):
        assert analyzer.analyze(COHERENT_TEXT) > analyzer.analyze(BEGINNER_TEXT)

    def test_short_text_scores_lower_than_developed_text(self):
        # < 50 words → limited coherence assessment
        assert analyzer.analyze(SHORT_TEXT) < analyzer.analyze(ADVANCED_TEXT)

    def test_coherent_text_scores_well(self):
        assert analyzer.analyze(COHERENT_TEXT) >= 5.0
