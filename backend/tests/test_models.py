"""Tests for Pydantic request/response models."""
import pytest
from pydantic import ValidationError
from app.models import ScoreRequest, ScoreResponse, SubcategoryScores, SubcategoryFeedback, ScoreData


class TestScoreRequest:
    def test_valid_text_accepted(self):
        req = ScoreRequest(text="This is a valid English sentence for testing.")
        assert req.text == "This is a valid English sentence for testing."

    def test_empty_text_rejected(self):
        with pytest.raises(ValidationError) as exc_info:
            ScoreRequest(text="")
        assert "empty" in str(exc_info.value).lower()

    def test_whitespace_only_text_rejected(self):
        with pytest.raises(ValidationError):
            ScoreRequest(text="   \n\t  ")

    def test_text_below_minimum_words_rejected(self):
        # Fewer than 5 words
        with pytest.raises(ValidationError) as exc_info:
            ScoreRequest(text="Too short text.")
        assert "5" in str(exc_info.value)

    def test_text_with_exactly_five_words_accepted(self):
        req = ScoreRequest(text="One two three four five.")
        assert req.text is not None

    def test_text_exceeding_2000_words_rejected(self):
        long_text = " ".join(["word"] * 2001)
        with pytest.raises(ValidationError) as exc_info:
            ScoreRequest(text=long_text)
        assert "2000" in str(exc_info.value)

    def test_text_with_exactly_2000_words_accepted(self):
        text = " ".join(["word"] * 2000)
        req = ScoreRequest(text=text)
        assert req.text is not None

    def test_missing_text_field_raises_validation_error(self):
        with pytest.raises(ValidationError):
            ScoreRequest()


class TestSubcategoryScores:
    def test_valid_scores_accepted(self):
        scores = SubcategoryScores(
            grammar=7.5,
            vocabulary=6.0,
            spelling_mechanics=8.0,
            sentence_structure=7.0,
            coherence_organization=6.5,
            fluency_naturalness=6.8,
        )
        assert scores.grammar == 7.5
        assert scores.vocabulary == 6.0

    def test_has_all_six_subcategories(self):
        scores = SubcategoryScores(
            grammar=5.0,
            vocabulary=5.0,
            spelling_mechanics=5.0,
            sentence_structure=5.0,
            coherence_organization=5.0,
            fluency_naturalness=5.0,
        )
        assert hasattr(scores, "grammar")
        assert hasattr(scores, "vocabulary")
        assert hasattr(scores, "spelling_mechanics")
        assert hasattr(scores, "sentence_structure")
        assert hasattr(scores, "coherence_organization")
        assert hasattr(scores, "fluency_naturalness")


class TestSubcategoryFeedback:
    def test_has_all_six_feedback_fields(self):
        feedback = SubcategoryFeedback(
            grammar="Good grammar.",
            vocabulary="Good vocabulary.",
            spelling_mechanics="Good spelling.",
            sentence_structure="Good structure.",
            coherence_organization="Good organization.",
            fluency_naturalness="Good fluency.",
        )
        assert feedback.grammar == "Good grammar."
        assert feedback.fluency_naturalness == "Good fluency."


class TestScoreData:
    def test_valid_score_data(self):
        data = ScoreData(
            overall_score=7.5,
            proficiency_level="Upper-Intermediate",
            subcategory_scores=SubcategoryScores(
                grammar=8.0,
                vocabulary=7.2,
                spelling_mechanics=9.0,
                sentence_structure=7.0,
                coherence_organization=7.3,
                fluency_naturalness=6.8,
            ),
            feedback=SubcategoryFeedback(
                grammar="Good grammar.",
                vocabulary="Good vocab.",
                spelling_mechanics="Good spelling.",
                sentence_structure="Good structure.",
                coherence_organization="Good organization.",
                fluency_naturalness="Good fluency.",
            ),
            confidence_level="high",
            word_count=145,
        )
        assert data.overall_score == 7.5
        assert data.confidence_level == "high"
        assert data.word_count == 145


class TestScoreResponse:
    def test_success_response(self):
        resp = ScoreResponse(
            success=True,
            data=ScoreData(
                overall_score=7.5,
                proficiency_level="Upper-Intermediate",
                subcategory_scores=SubcategoryScores(
                    grammar=8.0, vocabulary=7.0, spelling_mechanics=9.0,
                    sentence_structure=7.0, coherence_organization=7.0,
                    fluency_naturalness=7.0,
                ),
                feedback=SubcategoryFeedback(
                    grammar="g", vocabulary="v", spelling_mechanics="s",
                    sentence_structure="ss", coherence_organization="co",
                    fluency_naturalness="fn",
                ),
                confidence_level="high",
                word_count=100,
            ),
        )
        assert resp.success is True
        assert resp.data is not None
        assert resp.error is None

    def test_error_response(self):
        resp = ScoreResponse(
            success=False,
            error={"code": "TEXT_TOO_SHORT", "message": "Text is too short."},
        )
        assert resp.success is False
        assert resp.data is None
        assert resp.error["code"] == "TEXT_TOO_SHORT"
