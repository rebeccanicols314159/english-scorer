"""Language detection — rejects non-English text before scoring."""
from langdetect import detect, LangDetectException
from langdetect import DetectorFactory

# Make detection deterministic
DetectorFactory.seed = 0


def is_english(text: str) -> bool:
    """Return True if text is detected as English."""
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False
