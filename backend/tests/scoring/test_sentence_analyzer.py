"""Tests for the sentence structure analyzer."""
import pytest
from tests.scoring.fixtures import ADVANCED_TEXT, UNIFORM_SENTENCE_TEXT, INTERMEDIATE_TEXT
from app.scoring.analyzers.sentence import SentenceStructureAnalyzer

analyzer = SentenceStructureAnalyzer()


class TestSentenceStructureInvariants:
    def test_score_is_between_1_and_10(self):
        assert 1.0 <= analyzer.analyze(INTERMEDIATE_TEXT) <= 10.0

    def test_score_is_deterministic(self):
        assert analyzer.analyze(ADVANCED_TEXT) == analyzer.analyze(ADVANCED_TEXT)

    def test_score_is_rounded_to_one_decimal(self):
        score = analyzer.analyze(ADVANCED_TEXT)
        assert score == round(score, 1)


class TestSentenceStructureComparative:
    def test_varied_sentences_score_higher_than_uniform(self):
        assert analyzer.analyze(ADVANCED_TEXT) > analyzer.analyze(UNIFORM_SENTENCE_TEXT)

    def test_uniform_sentences_scores_lower(self):
        # All sentences same short length → limited variety
        assert analyzer.analyze(UNIFORM_SENTENCE_TEXT) <= 7.0

    def test_advanced_text_scores_well(self):
        assert analyzer.analyze(ADVANCED_TEXT) >= 5.0
