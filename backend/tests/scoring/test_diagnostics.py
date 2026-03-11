"""Tests for get_diagnostics() on each analyzer — drives the diagnostic API."""
import pytest
from tests.scoring.fixtures import (
    ADVANCED_TEXT, BEGINNER_TEXT, MISSPELLED_TEXT, CORRECTLY_SPELLED_TEXT,
    REPETITIVE_TEXT, RICH_VOCABULARY_TEXT, COHERENT_TEXT, SHORT_TEXT,
    UNIFORM_SENTENCE_TEXT,
)
from app.scoring.analyzers.grammar import GrammarAnalyzer
from app.scoring.analyzers.vocabulary import VocabularyAnalyzer
from app.scoring.analyzers.spelling import SpellingAnalyzer
from app.scoring.analyzers.sentence import SentenceStructureAnalyzer
from app.scoring.analyzers.coherence import CoherenceAnalyzer
from app.scoring.analyzers.fluency import FluencyAnalyzer


# ── Grammar ───────────────────────────────────────────────────────────────────

class TestGrammarDiagnostics:
    def setup_method(self):
        self.a = GrammarAnalyzer()

    def test_returns_error_count(self):
        d = self.a.get_diagnostics(BEGINNER_TEXT)
        assert "error_count" in d
        assert isinstance(d["error_count"], int)

    def test_returns_error_types_list(self):
        d = self.a.get_diagnostics(BEGINNER_TEXT)
        assert "error_types" in d
        assert isinstance(d["error_types"], list)

    def test_clean_text_has_zero_errors(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert d["error_count"] == 0

    def test_beginner_text_has_errors(self):
        d = self.a.get_diagnostics(BEGINNER_TEXT)
        assert d["error_count"] > 0

    def test_agreement_error_type_detected(self):
        d = self.a.get_diagnostics(BEGINNER_TEXT)
        assert "agreement" in d["error_types"]

    def test_diagnostics_are_deterministic(self):
        assert self.a.get_diagnostics(BEGINNER_TEXT) == self.a.get_diagnostics(BEGINNER_TEXT)


# ── Vocabulary ────────────────────────────────────────────────────────────────

class TestVocabularyDiagnostics:
    def setup_method(self):
        self.a = VocabularyAnalyzer()

    def test_returns_ttr(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert "ttr" in d
        assert 0.0 <= d["ttr"] <= 1.0

    def test_returns_avg_word_length(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert "avg_word_length" in d
        assert d["avg_word_length"] > 0

    def test_repetitive_text_has_lower_ttr(self):
        rich_ttr = self.a.get_diagnostics(RICH_VOCABULARY_TEXT)["ttr"]
        rep_ttr = self.a.get_diagnostics(REPETITIVE_TEXT)["ttr"]
        assert rich_ttr > rep_ttr

    def test_diagnostics_are_deterministic(self):
        assert self.a.get_diagnostics(ADVANCED_TEXT) == self.a.get_diagnostics(ADVANCED_TEXT)


# ── Spelling ──────────────────────────────────────────────────────────────────

class TestSpellingDiagnostics:
    def setup_method(self):
        self.a = SpellingAnalyzer()

    def test_returns_error_count(self):
        d = self.a.get_diagnostics(MISSPELLED_TEXT)
        assert "error_count" in d
        assert isinstance(d["error_count"], int)

    def test_returns_error_rate(self):
        d = self.a.get_diagnostics(MISSPELLED_TEXT)
        assert "error_rate" in d
        assert d["error_rate"] >= 0.0

    def test_correct_text_has_zero_errors(self):
        d = self.a.get_diagnostics(CORRECTLY_SPELLED_TEXT)
        assert d["error_count"] == 0

    def test_misspelled_text_has_errors(self):
        d = self.a.get_diagnostics(MISSPELLED_TEXT)
        assert d["error_count"] > 0

    def test_diagnostics_are_deterministic(self):
        assert self.a.get_diagnostics(MISSPELLED_TEXT) == self.a.get_diagnostics(MISSPELLED_TEXT)


# ── Sentence Structure ────────────────────────────────────────────────────────

class TestSentenceDiagnostics:
    def setup_method(self):
        self.a = SentenceStructureAnalyzer()

    def test_returns_avg_sentence_length(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert "avg_sentence_length" in d
        assert d["avg_sentence_length"] > 0

    def test_returns_sentence_count(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert "sentence_count" in d
        assert d["sentence_count"] >= 1

    def test_returns_complex_ratio(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert "complex_ratio" in d
        assert 0.0 <= d["complex_ratio"] <= 1.0

    def test_uniform_text_has_lower_variety_than_advanced(self):
        adv = self.a.get_diagnostics(ADVANCED_TEXT)["complex_ratio"]
        uni = self.a.get_diagnostics(UNIFORM_SENTENCE_TEXT)["complex_ratio"]
        assert adv >= uni

    def test_diagnostics_are_deterministic(self):
        assert self.a.get_diagnostics(ADVANCED_TEXT) == self.a.get_diagnostics(ADVANCED_TEXT)


# ── Coherence ─────────────────────────────────────────────────────────────────

class TestCoherenceDiagnostics:
    def setup_method(self):
        self.a = CoherenceAnalyzer()

    def test_returns_transition_count(self):
        d = self.a.get_diagnostics(COHERENT_TEXT)
        assert "transition_count" in d
        assert isinstance(d["transition_count"], int)

    def test_returns_word_count(self):
        d = self.a.get_diagnostics(COHERENT_TEXT)
        assert "word_count" in d
        assert d["word_count"] > 0

    def test_coherent_text_has_more_transitions_than_beginner(self):
        coh = self.a.get_diagnostics(COHERENT_TEXT)["transition_count"]
        beg = self.a.get_diagnostics(BEGINNER_TEXT)["transition_count"]
        assert coh > beg

    def test_short_text_reports_low_word_count(self):
        d = self.a.get_diagnostics(SHORT_TEXT)
        assert d["word_count"] < 50

    def test_diagnostics_are_deterministic(self):
        assert self.a.get_diagnostics(COHERENT_TEXT) == self.a.get_diagnostics(COHERENT_TEXT)


# ── Fluency ───────────────────────────────────────────────────────────────────

class TestFluencyDiagnostics:
    def setup_method(self):
        self.a = FluencyAnalyzer()

    def test_returns_fre(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert "fre" in d
        assert isinstance(d["fre"], float)

    def test_returns_grade(self):
        d = self.a.get_diagnostics(ADVANCED_TEXT)
        assert "grade" in d
        assert d["grade"] >= 0.0

    def test_advanced_text_has_lower_fre_than_beginner(self):
        adv_fre = self.a.get_diagnostics(ADVANCED_TEXT)["fre"]
        beg_fre = self.a.get_diagnostics(BEGINNER_TEXT)["fre"]
        assert adv_fre < beg_fre

    def test_diagnostics_are_deterministic(self):
        assert self.a.get_diagnostics(ADVANCED_TEXT) == self.a.get_diagnostics(ADVANCED_TEXT)
