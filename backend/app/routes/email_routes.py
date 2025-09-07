
"""from fastapi import APIRouter
from app.services.gmail_service import get_gmail_service
from app.services.ml_service import detect_category
from app.services.nlp_service import analyze_sentiment, detect_priority
from app.utils.db import emails_collection
from datetime import datetime

router = APIRouter()

@router.get("/emails", summary="Fetch and process emails from Gmail")
def fetch_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", maxResults=5).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        snippet = msg_data.get("snippet", "")
        headers = msg_data["payload"]["headers"]

        sender = next((h["value"] for h in headers if h["name"] == "From"), "")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")

        # Apply ML + NLP
        category = detect_category(subject, snippet)
        sentiment = analyze_sentiment(snippet)
        priority = detect_priority(subject + " " + snippet)

        email_doc = {
            "message_id": msg["id"],
            "sender": sender,
            "subject": subject,
            "body": snippet,
            "received_at": datetime.utcnow(),
            "labels": msg_data.get("labelIds", []),
            "category": category,
            "sentiment": sentiment,
            "priority": priority,
            "status": "pending"
        }

        # Save to MongoDB (upsert to avoid duplicates)
        emails_collection.update_one(
            {"message_id": msg["id"]},
            {"$set": email_doc},
            upsert=True
        )

        emails.append(email_doc)

    return {"emails": emails}"""
    
    
# app/routes/email_routes.py
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import logging
from typing import List, Dict, Any

from app.services.gmail_service import get_gmail_service
from app.utils.db import emails_collection  # if you store emails; optional

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.get("/emails", summary="Get Emails")
def fetch_emails(filter: str = Query("all", description="filter=all|unread|support")):
    """
    Fetch emails from DB (if present) or from Gmail service for demo.
    This route is defensive: any exceptions are logged and returned in JSON.
    """
    try:
        # If you have stored emails in DB (preferred), return them first:
        try:
            # if emails collection available, use it
            docs = list(emails_collection.find({}, {"_id": 0}).sort("received_at", -1).limit(200))
            if docs:
                return {"emails": docs}
        except Exception:
            # DB may not be configured — fall back to Gmail fetch
            logger.debug("DB read failed or not configured; falling back to Gmail API.", exc_info=True)

        # Fallback: fetch from Gmail (live)
        service = get_gmail_service()
        if not service:
            return JSONResponse(status_code=200, content={"emails": [], "warning":"Gmail service not available; check token/credentials."})

        # fetch messages list
        results = service.users().messages().list(userId="me", maxResults=20).execute()
        messages = results.get("messages", [])

        emails: List[Dict[str, Any]] = []
        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
            # parse snippet / payload safely
            snippet = msg_data.get("snippet", "")
            payload = msg_data.get("payload", {})
            headers = {h["name"]: h["value"] for h in payload.get("headers", [])} if payload else {}
            subject = headers.get("Subject", "")
            from_addr = headers.get("From", "")
            received = msg_data.get("internalDate")  # milliseconds string
            # convert internalDate if present
            try:
                if received:
                    import datetime
                    received_at = datetime.datetime.fromtimestamp(int(received)/1000).isoformat()
                else:
                    received_at = None
            except Exception:
                received_at = None

            emails.append({
                "id": msg["id"],
                "message_id": msg_data.get("id"),
                "sender": from_addr,
                "subject": subject,
                "body": snippet,
                "received_at": received_at,
                "labels": msg_data.get("labelIds", []),
                "category": "general",
                "sentiment": "unknown",
                "priority": "not_urgent",
                "status": "pending"
            })

        return {"emails": emails}

    except Exception as e:
        # Log full exception with stack trace to help debugging
        logger.exception("Error in fetch_emails: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal server error in fetch_emails. See server logs for traceback."})
    