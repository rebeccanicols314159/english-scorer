"""Tests for the FastAPI HTTP endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, rate_limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    rate_limiter.reset()
    yield
    rate_limiter.reset()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    async def test_health_returns_200(self, client):
        response = await client.get("/health")
        assert response.status_code == 200

    async def test_health_returns_ok_status(self, client):
        response = await client.get("/health")
        data = response.json()
        assert data["status"] == "ok"


class TestScoreEndpoint:
    VALID_TEXT = (
        "The quick brown fox jumps over the lazy dog. "
        "This is a test sentence for the English scorer application. "
        "It should produce valid scores across all subcategories. "
        "Grammar and vocabulary are important aspects of language learning. "
        "Regular practice helps improve overall English proficiency significantly."
    )

    async def test_valid_text_returns_200(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        assert response.status_code == 200

    async def test_response_has_success_true(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        assert response.json()["success"] is True

    async def test_response_has_data_field(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        data = response.json()
        assert "data" in data
        assert data["data"] is not None

    async def test_response_overall_score_in_range(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        overall = response.json()["data"]["overall_score"]
        assert 1.0 <= overall <= 10.0

    async def test_response_has_proficiency_level(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        level = response.json()["data"]["proficiency_level"]
        assert isinstance(level, str)
        assert len(level) > 0

    async def test_response_has_cefr_level(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        cefr = response.json()["data"]["cefr_level"]
        assert cefr in {"A1", "A2", "B1", "B2", "C1", "C1+", "C2"}

    async def test_response_has_all_subcategory_scores(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        subcategories = response.json()["data"]["subcategory_scores"]
        expected_keys = {
            "grammar", "vocabulary", "spelling_mechanics",
            "sentence_structure", "coherence_organization", "fluency_naturalness"
        }
        assert set(subcategories.keys()) == expected_keys

    async def test_subcategory_scores_in_range(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        subcategories = response.json()["data"]["subcategory_scores"]
        for category, score in subcategories.items():
            assert 1.0 <= score <= 10.0, f"{category} score {score} out of range"

    async def test_response_has_all_feedback_fields(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        feedback = response.json()["data"]["feedback"]
        expected_keys = {
            "grammar", "vocabulary", "spelling_mechanics",
            "sentence_structure", "coherence_organization", "fluency_naturalness"
        }
        assert set(feedback.keys()) == expected_keys

    async def test_feedback_values_are_strings(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        feedback = response.json()["data"]["feedback"]
        for category, text in feedback.items():
            assert isinstance(text, str)
            assert len(text) > 0

    async def test_response_has_confidence_level(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        confidence = response.json()["data"]["confidence_level"]
        assert confidence in {"low", "medium", "high", "very_high"}

    async def test_response_has_word_count(self, client):
        response = await client.post("/api/score", json={"text": self.VALID_TEXT})
        word_count = response.json()["data"]["word_count"]
        assert isinstance(word_count, int)
        assert word_count > 0

    async def test_empty_text_returns_422(self, client):
        response = await client.post("/api/score", json={"text": ""})
        assert response.status_code == 422

    async def test_too_short_text_returns_422(self, client):
        response = await client.post("/api/score", json={"text": "Hi there."})
        assert response.status_code == 422

    async def test_too_long_text_returns_422(self, client):
        long_text = " ".join(["word"] * 2001)
        response = await client.post("/api/score", json={"text": long_text})
        assert response.status_code == 422

    async def test_missing_text_field_returns_422(self, client):
        response = await client.post("/api/score", json={})
        assert response.status_code == 422

    async def test_non_json_body_returns_422(self, client):
        response = await client.post(
            "/api/score",
            content="not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422

    async def test_error_response_has_success_false(self, client):
        response = await client.post("/api/score", json={"text": "Too short."})
        assert response.json()["success"] is False

    async def test_error_response_has_error_field(self, client):
        response = await client.post("/api/score", json={"text": "Too short."})
        assert "error" in response.json()

    async def test_error_response_has_code_invalid_input(self, client):
        response = await client.post("/api/score", json={"text": "Too short."})
        assert response.json()["error"]["code"] == "INVALID_INPUT"

    async def test_error_response_has_message(self, client):
        response = await client.post("/api/score", json={"text": "Too short."})
        message = response.json()["error"]["message"]
        assert isinstance(message, str) and len(message) > 0

    async def test_short_text_has_low_confidence(self, client):
        # < 30 words should return "low" confidence
        short_text = "I go to store. She like cat. He run fast. We are happy people here."
        response = await client.post("/api/score", json={"text": short_text})
        confidence = response.json()["data"]["confidence_level"]
        assert confidence == "low"

    async def test_long_text_has_very_high_confidence(self, client):
        # > 500 words should return "very_high" confidence (12 words × 45 = 540 words)
        long_text = " ".join([
            "The English language has a rich history spanning many centuries of development."
        ] * 45)
        response = await client.post("/api/score", json={"text": long_text})
        confidence = response.json()["data"]["confidence_level"]
        assert confidence == "very_high"


class TestLanguageDetection:
    FRENCH_TEXT = (
        "Le français est une langue romane dont les locuteurs sont appelés francophones. "
        "Elle est parlée sur les cinq continents par environ trois cent millions de personnes. "
        "La langue française est issue du latin vulgaire parlé en Gaule romaine."
    )
    SPANISH_TEXT = (
        "El español es una lengua romance que pertenece a la familia indoeuropea. "
        "Es el segundo idioma más hablado del mundo por número de hablantes nativos. "
        "Se habla principalmente en España y en América Latina."
    )
    GERMAN_TEXT = (
        "Die deutsche Sprache ist eine westgermanische Sprache. "
        "Sie wird von etwa 100 Millionen Menschen als Muttersprache gesprochen. "
        "Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union."
    )

    async def test_french_text_returns_422(self, client):
        response = await client.post("/api/score", json={"text": self.FRENCH_TEXT})
        assert response.status_code == 422

    async def test_spanish_text_returns_422(self, client):
        response = await client.post("/api/score", json={"text": self.SPANISH_TEXT})
        assert response.status_code == 422

    async def test_german_text_returns_422(self, client):
        response = await client.post("/api/score", json={"text": self.GERMAN_TEXT})
        assert response.status_code == 422

    async def test_non_english_error_code(self, client):
        response = await client.post("/api/score", json={"text": self.FRENCH_TEXT})
        assert response.json()["error"]["code"] == "NOT_ENGLISH"

    async def test_non_english_success_false(self, client):
        response = await client.post("/api/score", json={"text": self.FRENCH_TEXT})
        assert response.json()["success"] is False

    async def test_non_english_has_message(self, client):
        response = await client.post("/api/score", json={"text": self.FRENCH_TEXT})
        message = response.json()["error"]["message"]
        assert isinstance(message, str) and len(message) > 0

    async def test_english_text_still_scores(self, client):
        response = await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        assert response.status_code == 200
        assert response.json()["success"] is True


class TestRateLimiting:
    async def test_requests_within_limit_succeed(self, client):
        for _ in range(5):
            response = await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
            assert response.status_code == 200

    async def test_exceeding_limit_returns_429(self, client):
        rate_limiter.limit = 3
        for _ in range(3):
            await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        response = await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        assert response.status_code == 429

    async def test_429_response_has_success_false(self, client):
        rate_limiter.limit = 1
        await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        response = await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        assert response.json()["success"] is False

    async def test_429_response_has_rate_limited_code(self, client):
        rate_limiter.limit = 1
        await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        response = await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        assert response.json()["error"]["code"] == "RATE_LIMITED"

    async def test_429_response_has_message(self, client):
        rate_limiter.limit = 1
        await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        response = await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        message = response.json()["error"]["message"]
        assert isinstance(message, str) and len(message) > 0

    async def test_rate_limit_does_not_apply_to_health(self, client):
        rate_limiter.limit = 1
        await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        await client.post("/api/score", json={"text": TestScoreEndpoint.VALID_TEXT})
        response = await client.get("/health")
        assert response.status_code == 200
