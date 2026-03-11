"""Tests for the spelling analyzer."""
import pytest
from tests.scoring.fixtures import CORRECTLY_SPELLED_TEXT, MISSPELLED_TEXT, ADVANCED_TEXT
from app.scoring.analyzers.spelling import SpellingAnalyzer

analyzer = SpellingAnalyzer()


class TestSpellingAnalyzerInvariants:
    def test_score_is_between_1_and_10(self):
        assert 1.0 <= analyzer.analyze(CORRECTLY_SPELLED_TEXT) <= 10.0

    def test_score_is_deterministic(self):
        assert analyzer.analyze(CORRECTLY_SPELLED_TEXT) == analyzer.analyze(CORRECTLY_SPELLED_TEXT)

    def test_score_is_rounded_to_one_decimal(self):
        score = analyzer.analyze(CORRECTLY_SPELLED_TEXT)
        assert score == round(score, 1)


class TestSpellingAnalyzerComparative:
    def test_correct_spelling_scores_higher_than_misspelled(self):
        assert analyzer.analyze(CORRECTLY_SPELLED_TEXT) > analyzer.analyze(MISSPELLED_TEXT)

    def test_correctly_spelled_text_scores_high(self):
        assert analyzer.analyze(CORRECTLY_SPELLED_TEXT) >= 7.0

    def test_misspelled_text_scores_low(self):
        assert analyzer.analyze(MISSPELLED_TEXT) <= 6.0

    def test_advanced_text_scores_high(self):
        # Advanced text should have no spelling errors
        assert analyzer.analyze(ADVANCED_TEXT) >= 7.0
