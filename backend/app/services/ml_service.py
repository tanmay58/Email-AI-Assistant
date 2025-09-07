import re

CATEGORIES = ["support", "query", "request", "help"]

def detect_category(subject: str = "", body: str = "") -> str:
    """Detect category based on keywords in subject/body"""
    text = (subject or "") + " " + (body or "")
    text = text.lower()
    for c in CATEGORIES:
        if re.search(rf"\b{c}\b", text):   # match whole word
            return c
    return "general"

def detect_priority(subject: str = "", body: str = "") -> str:
    """Detect urgency of an email"""
    urgent_keywords = ["urgent", "immediately", "asap", "critical", "cannot access", "important"]
    text = (subject or "") + " " + (body or "")
    text = text.lower()
    if any(kw in text for kw in urgent_keywords):
        return "urgent"
    return "not urgent"

def detect_sentiment(body: str = "") -> str:
    """Very simple sentiment detection (hackathon fast path).
       Replace with HuggingFace model for stronger results.
    """
    positive_keywords = ["thank", "great", "good", "awesome", "happy", "excellent"]
    negative_keywords = ["bad", "issue", "problem", "not working", "angry", "upset", "complain"]

    body = (body or "").lower()

    if any(kw in body for kw in negative_keywords):
        return "negative"
    elif any(kw in body for kw in positive_keywords):
        return "positive"
    else:
        return "neutral"
