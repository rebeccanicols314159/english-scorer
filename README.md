# English Scorer

A web application that scores English writing proficiency for non-native speakers. Paste any text (5–2000 words) and receive an instant overall score, a visual breakdown across six categories, and actionable feedback.

## Features

- **Overall score** (1–10) with proficiency level (Beginner → Proficient) and confidence rating
- **Six-category breakdown** with colour-coded progress bars: Grammar, Vocabulary, Spelling & Mechanics, Sentence Structure, Coherence & Organisation, Fluency & Naturalness
- **Actionable feedback** per category with colour-coded indicators
- **Example texts** (Beginner / Intermediate / Advanced / Proficient) to try the scorer instantly
- **PDF export** — download a full report with coloured bars and indicators, timestamped filename
- **Language detection** — rejects non-English submissions
- **Rate limiting** — prevents abuse

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.14, FastAPI, Pydantic v2 |
| NLP | NLTK, pyspellchecker, textstat |
| Frontend | React, Vite, Tailwind CSS v4 |
| PDF export | jsPDF |
| Backend tests | pytest, pytest-asyncio, httpx |
| Frontend tests | Vitest, Testing Library |

## Scoring categories

| Category | Weight | Analyser |
|---|---|---|
| Grammar | 25% | NLTK POS tagging — subject-verb agreement, double words |
| Vocabulary | 20% | Type-token ratio, content-word length, polysyllabic ratio |
| Sentence Structure | 20% | Sentence length distribution, complex sentence ratio |
| Coherence & Organisation | 15% | Transition word density, paragraph structure |
| Spelling & Mechanics | 10% | pyspellchecker error rate |
| Fluency & Naturalness | 10% | Flesch Reading Ease (textstat) |

## Getting started

### Backend

```bash
cd backend
python3 -m pip install -e .
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`. The Vite dev server proxies `/api` to the backend automatically.

## Running tests

```bash
# Backend (138 tests)
cd backend && python3 -m pytest tests/ -v

# Frontend (116 tests)
cd frontend && npm test
```

## API

```
POST /api/score
Content-Type: application/json

{ "text": "Your English text here..." }
```

Response:

```json
{
  "overall_score": 7.5,
  "proficiency_level": "Upper-Intermediate",
  "confidence_level": "high",
  "word_count": 145,
  "subcategory_scores": {
    "grammar": 8.0,
    "vocabulary": 7.2,
    "spelling_mechanics": 9.0,
    "sentence_structure": 7.0,
    "coherence_organization": 7.3,
    "fluency_naturalness": 6.8
  },
  "feedback": {
    "grammar": "Excellent grammar. Your writing shows strong command...",
    ...
  }
}
```
