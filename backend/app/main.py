"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import ScoreRequest, ScoreResponse, ScoreData, SubcategoryScores, SubcategoryFeedback
from app.scoring.engine import (
    count_words,
    compute_subcategory_scores,
    compute_all_diagnostics,
    compute_overall_score,
    get_confidence_level,
    get_proficiency_level,
)
from app.scoring.feedback import generate_feedback

app = FastAPI(title="English Scorer API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/score", response_model=ScoreResponse)
def score_text(request: ScoreRequest) -> ScoreResponse:
    text = request.text
    word_count = count_words(text)

    subcategory_scores = compute_subcategory_scores(text)
    diagnostics = compute_all_diagnostics(text)
    overall_score = compute_overall_score(subcategory_scores)
    confidence_level = get_confidence_level(word_count)
    proficiency_level = get_proficiency_level(overall_score)
    feedback = generate_feedback(subcategory_scores, diagnostics)

    return ScoreResponse(
        success=True,
        data=ScoreData(
            overall_score=overall_score,
            proficiency_level=proficiency_level,
            subcategory_scores=SubcategoryScores(**subcategory_scores),
            feedback=SubcategoryFeedback(**feedback),
            confidence_level=confidence_level,
            word_count=word_count,
        ),
    )
