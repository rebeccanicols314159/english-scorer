"""Pydantic models for request and response validation."""
from pydantic import BaseModel, field_validator
from typing import Optional


class ScoreRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        words = v.split()
        if len(words) < 5:
            raise ValueError("Text must be at least 5 words")
        if len(words) > 2000:
            raise ValueError("Text must not exceed 2000 words")
        return v


class SubcategoryScores(BaseModel):
    grammar: float
    vocabulary: float
    spelling_mechanics: float
    sentence_structure: float
    coherence_organization: float
    fluency_naturalness: float


class SubcategoryFeedback(BaseModel):
    grammar: str
    vocabulary: str
    spelling_mechanics: str
    sentence_structure: str
    coherence_organization: str
    fluency_naturalness: str


class ScoreData(BaseModel):
    overall_score: float
    proficiency_level: str
    cefr_level: str
    subcategory_scores: SubcategoryScores
    feedback: SubcategoryFeedback
    confidence_level: str
    word_count: int


class ScoreResponse(BaseModel):
    success: bool
    data: Optional[ScoreData] = None
    error: Optional[dict] = None
