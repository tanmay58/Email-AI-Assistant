"""rom fastapi import APIRouter
from app.services.gmail_service import get_gmail_service
from app.utils.db import emails_collection
import base64
from email.mime.text import MIMEText

router = APIRouter()

@router.post("/", summary="Send a reply to an email")
async def send_reply(email_id: str, reply_text: str):
    service = get_gmail_service()

    # Fetch the original email (for threading)
    original = service.users().messages().get(userId="me", id=email_id).execute()
    headers = original["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")

    # Prepare reply
    message = MIMEText(reply_text)
    message["to"] = sender
    message["subject"] = "Re: " + subject
    message["In-Reply-To"] = original["id"]

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()

    # Update MongoDB status
    emails_collection.update_one(
        {"message_id": email_id},
        {"$set": {"status": "replied"}}
    )

    return {
        "status": "success",
        "email_id": email_id,
        "reply_text": reply_text,
        "gmail_id": send_message["id"],
        "message": "Reply sent and status updated to 'replied'." 
        }"""
        
        
# app/routes/reply_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.gmail_service import get_gmail_service
from app.utils.db import get_email_by_message_id, upsert_email
from email.mime.text import MIMEText
import base64

router = APIRouter(prefix="/reply", tags=["Reply"])

class ReplyRequest(BaseModel):
    message_id: str
    reply_text: str

@router.post("/")
def send_reply(req: ReplyRequest):
    email = get_email_by_message_id(req.message_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    service = get_gmail_service()
    # fetch original message to get headers/thread
    orig = service.users().messages().get(userId="me", id=req.message_id, format="full").execute()
    headers = {h["name"]: h["value"] for h in orig.get("payload", {}).get("headers", [])}
    to_addr = headers.get("From")
    subj = headers.get("Subject", "")

    if not to_addr:
        raise HTTPException(status_code=400, detail="Could not determine 'From' address to reply to.")

    message = MIMEText(req.reply_text)
    message["to"] = to_addr
    message["subject"] = f"Re: {subj}"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    sent = service.users().messages().send(userId="me", body={"raw": raw, "threadId": orig.get("threadId")}).execute()

    # update DB status
    email["status"] = "replied"
    upsert_email(email)

    return {"status": "success", "gmail_id": sent.get("id"), "message": "Reply sent and status updated to 'replied'."}
        
        
    
