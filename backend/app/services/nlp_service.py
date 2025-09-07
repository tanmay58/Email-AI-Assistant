""""
from textblob import TextBlob

def analyze_sentiment(text: str) -> str:

    Analyze sentiment of given text and return:
    - "positive"
    - "negative"
    - "neutral"

    if not text:
        return "neutral"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"


def detect_priority(text: str) -> str:
    
    Detect urgency of text. Returns:
    - "urgent" if critical words appear
    - "not_urgent" otherwise
    
    if not text:
        return "not_urgent"

    urgent_keywords = ["immediately", "urgent", "asap", "critical", "cannot access", "important", "issue"]
    text_lower = text.lower()

    if any(word in text_lower for word in urgent_keywords):
        return "urgent"
    return "not_urgent"
    
    """
# app/services/nlp_service.py
import re
from typing import Dict, Any

NEGATIVE_KEYWORDS = ["not working", "can't", "cannot", "error", "crash", "failed", "unable", "angry", "frustrat", "problem"]
POSITIVE_KEYWORDS = ["thank", "thanks", "great", "good", "appreciate", "awesome"]

def analyze_sentiment(text: str) -> str:
    if not text:
        return "neutral"
    t = text.lower()
    neg = sum(1 for k in NEGATIVE_KEYWORDS if k in t)
    pos = sum(1 for k in POSITIVE_KEYWORDS if k in t)
    if neg > pos and neg > 0:
        return "negative"
    if pos > neg and pos > 0:
        return "positive"
    return "neutral"

def extract_info(text: str) -> Dict[str, Any]:
    phones = re.findall(r"\+?\d[\d\-\s]{6,}\d", text)
    emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    # keywords: extract words length>=4 as simple proxy
    kw = re.findall(r"\b[a-zA-Z]{4,}\b", text)
    keywords = list(dict.fromkeys([w.lower() for w in kw]))[:40]
    return {
        "phone_numbers": list(dict.fromkeys(phones)),
        "alternate_emails": list(dict.fromkeys(emails)),
        "keywords": keywords
    }
