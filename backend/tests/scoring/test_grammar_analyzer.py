"""Tests for the grammar analyzer."""
import pytest
from tests.scoring.fixtures import ADVANCED_TEXT, BEGINNER_TEXT, INTERMEDIATE_TEXT
from app.scoring.analyzers.grammar import GrammarAnalyzer

analyzer = GrammarAnalyzer()


class TestGrammarAnalyzerInvariants:
    def test_score_is_between_1_and_10(self):
        assert 1.0 <= analyzer.analyze(INTERMEDIATE_TEXT) <= 10.0

    def test_score_is_deterministic(self):
        assert analyzer.analyze(ADVANCED_TEXT) == analyzer.analyze(ADVANCED_TEXT)

    def test_score_is_rounded_to_one_decimal(self):
        score = analyzer.analyze(INTERMEDIATE_TEXT)
        assert score == round(score, 1)


class TestGrammarAnalyzerComparative:
    def test_advanced_scores_higher_than_beginner(self):
        assert analyzer.analyze(ADVANCED_TEXT) > analyzer.analyze(BEGINNER_TEXT)

    def test_intermediate_scores_higher_than_beginner(self):
        assert analyzer.analyze(INTERMEDIATE_TEXT) > analyzer.analyze(BEGINNER_TEXT)

    def test_advanced_text_scores_well(self):
        assert analyzer.analyze(ADVANCED_TEXT) >= 6.5

    def test_beginner_text_scores_low(self):
        assert analyzer.analyze(BEGINNER_TEXT) <= 6.0


class TestGrammarErrorDetection:
    def test_double_words_lower_score(self):
        clean = "The cat sat on the mat and enjoyed the warmth."
        with_doubles = "The the cat sat on the mat and and enjoyed it."
        assert analyzer.analyze(clean) > analyzer.analyze(with_doubles)

    def test_text_without_errors_scores_high(self):
        text = (
            "She walks to school every morning. "
            "The children are playing in the park. "
            "He has completed all his assignments."
        )
        assert analyzer.analyze(text) >= 7.0
