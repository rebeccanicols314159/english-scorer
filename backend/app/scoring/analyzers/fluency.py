"""Fluency and naturalness analyzer using textstat.

Metrics (from DESIGN.md):
- Flesch Reading Ease (primary readability metric)
- Flesch-Kincaid Grade Level (complexity)

Scoring rationale for a proficiency scorer:
- Very simple text (Flesch ≥ 70) → lower score: easy sentences signal lower proficiency
- Standard to difficult text (Flesch 30–70) → higher scores: shows command of the language
- Very difficult / dense text (Flesch < 30) → high but slightly capped: may indicate
  over-complexity rather than natural fluency

Flesch Reading Ease scale: 100 = very easy, 0 = very hard.
"""
import textstat
from .base import BaseAnalyzer


def _fre_to_score(fre: float) -> float:
    """Piecewise linear map from Flesch Reading Ease to 1–10 proficiency score."""
    if fre >= 70:
        # Too simple: score from 3.0 (FRE=100) to 5.0 (FRE=70)
        return 3.0 + (100.0 - fre) / 30.0 * 2.0
    elif fre >= 30:
        # Standard to difficult: score from 5.0 (FRE=70) to 8.0 (FRE=30)
        return 5.0 + (70.0 - fre) / 40.0 * 3.0
    else:
        # Very difficult: score from 7.5 (FRE=30) to 8.5 (FRE=0) — slight cap
        return 7.5 + (30.0 - fre) / 30.0 * 1.0


class FluencyAnalyzer(BaseAnalyzer):
    def get_diagnostics(self, text: str) -> dict:
        return {
            "fre": round(textstat.flesch_reading_ease(text), 2),
            "grade": round(textstat.flesch_kincaid_grade(text), 2),
        }

    def analyze(self, text: str) -> float:
        fre = textstat.flesch_reading_ease(text)
        grade = textstat.flesch_kincaid_grade(text)

        fre_score = _fre_to_score(fre)

        # Grade-level bonus: college-level writing (grade 10+) adds up to 1 point
        grade_bonus = min(max((grade - 5.0) / 10.0, 0.0), 1.0)

        raw = fre_score + grade_bonus
        return round(self._clamp(raw), 1)
