"""from fastapi import APIRouter
from app.utils.db import list_emails

router = APIRouter()

@router.get("/stats", summary="Get detailed email analytics")
async def get_stats():
    emails = list_emails()
    total = len(emails)

    # Initialize counters
    categories = {"support": 0, "query": 0, "request": 0, "help": 0, "general": 0}
    status_counts = {"pending": 0, "replied": 0, "snoozed": 0}
    sentiments = {"positive": 0, "negative": 0, "neutral": 0}

    for e in emails:
        # Category
        cat = e.get("category", "general").lower()
        categories[cat] = categories.get(cat, 0) + 1

        # Status
        st = e.get("status", "pending").lower()
        status_counts[st] = status_counts.get(st, 0) + 1

        # Sentiment
        sent = e.get("sentiment", "neutral").lower()
        sentiments[sent] = sentiments.get(sent, 0) + 1

    return {
        "total_emails": total,
        "categories": categories,
        "status": status_counts,
        "sentiments": sentiments
    }

    """
    
# app/routes/analytics_routes.py
from fastapi import APIRouter
from app.utils.db import list_emails

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/stats")
def get_stats():
    emails = list_emails()
    total = len(emails)
    categories = {"support":0,"query":0,"request":0,"help":0,"general":0}
    status = {"pending":0,"drafted":0,"replied":0,"snoozed":0}
    sentiments = {"positive":0,"negative":0,"neutral":0}
    for e in emails:
        cat = e.get("category","general")
        categories[cat] = categories.get(cat, 0) + 1
        st = e.get("status","pending")
        status[st] = status.get(st, 0) + 1
        sent = e.get("sentiment","neutral")
        sentiments[sent] = sentiments.get(sent, 0) + 1
    return {"total_emails": total, "categories": categories, "status": status, "sentiments": sentiments}
    