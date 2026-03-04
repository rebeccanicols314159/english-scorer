"""Tests for the vocabulary analyzer."""
import pytest
from tests.scoring.fixtures import (
    ADVANCED_TEXT, BEGINNER_TEXT, REPETITIVE_TEXT, RICH_VOCABULARY_TEXT
)
from app.scoring.analyzers.vocabulary import VocabularyAnalyzer

analyzer = VocabularyAnalyzer()


class TestVocabularyAnalyzerInvariants:
    def test_score_is_between_1_and_10(self):
        assert 1.0 <= analyzer.analyze(ADVANCED_TEXT) <= 10.0

    def test_score_is_deterministic(self):
        assert analyzer.analyze(RICH_VOCABULARY_TEXT) == analyzer.analyze(RICH_VOCABULARY_TEXT)

    def test_score_is_rounded_to_one_decimal(self):
        score = analyzer.analyze(ADVANCED_TEXT)
        assert score == round(score, 1)


class TestVocabularyAnalyzerComparative:
    def test_rich_vocabulary_scores_higher_than_repetitive(self):
        assert analyzer.analyze(RICH_VOCABULARY_TEXT) > analyzer.analyze(REPETITIVE_TEXT)

    def test_advanced_scores_higher_than_beginner(self):
        assert analyzer.analyze(ADVANCED_TEXT) > analyzer.analyze(BEGINNER_TEXT)

    def test_repetitive_text_scores_low(self):
        assert analyzer.analyze(REPETITIVE_TEXT) <= 6.0

    def test_rich_vocabulary_text_scores_high(self):
        assert analyzer.analyze(RICH_VOCABULARY_TEXT) >= 6.5
