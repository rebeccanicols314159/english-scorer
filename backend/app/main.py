"""FastAPI application entry point."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models import ScoreRequest, ScoreResponse, ScoreData, SubcategoryScores, SubcategoryFeedback
from app.rate_limiter import RateLimiter
from app.scoring.engine import (
    count_words,
    compute_subcategory_scores,
    compute_all_diagnostics,
    compute_overall_score,
    get_confidence_level,
    get_proficiency_level,
)
from app.scoring.feedback import generate_feedback
from app.scoring.language_detection import is_english

app = FastAPI(title="English Scorer API", version="0.1.0")

# 10 requests per 60 seconds per IP
rate_limiter = RateLimiter(limit=10, window=60)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path == "/api/score":
        ip = request.client.host if request.client else "unknown"
        if not rate_limiter.is_allowed(ip):
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMITED",
                        "message": "Too many requests. Please wait a moment before trying again.",
                    },
                },
            )
    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = [err.get("msg", "Invalid input") for err in exc.errors()]
    message = messages[0] if messages else "Invalid input"
    # Strip the "Value error, " prefix Pydantic v2 adds to field_validator messages
    message = message.removeprefix("Value error, ")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {"code": "INVALID_INPUT", "message": message},
        },
    )


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

    if not is_english(text):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": "NOT_ENGLISH",
                    "message": "Text does not appear to be in English. Please submit English text.",
                },
            },
        )

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
