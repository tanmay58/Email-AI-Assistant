"""# backend/app/routes/draft_routes.py (update)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.db import emails_collection
from app.services.ai_services import generate_draft_reply

router = APIRouter(prefix="/drafts", tags=["Drafts"])

class DraftRequest(BaseModel):
    message_id: str

@router.post("/generate")
def create_draft(payload: DraftRequest):
    email = emails_collection.find_one({"message_id": payload.message_id})
    if not email:
        raise HTTPException(404, "Email not found")
    subject = email.get("subject", "")
    body = email.get("body", "")
    category = email.get("category")
    sentiment = email.get("sentiment")
    extracted = email.get("extracted", {})

    draft_text, contexts = generate_draft_reply(subject, body, category, sentiment, extracted)

    # save draft + contexts (as simple list)
    emails_collection.update_one(
        {"message_id": payload.message_id},
        {"$set": {"ai_draft": draft_text, "ai_contexts": contexts, "status": "drafted"}}
    )

    return {"message_id": payload.message_id, "ai_draft": draft_text, "contexts": contexts}"""
    
    
# app/routes/draft_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback, logging

from app.utils.db import get_email_by_message_id, upsert_email
from app.services.ai_services import generate_draft_reply

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/drafts", tags=["Drafts"])

class DraftRequest(BaseModel):
    message_id: str

@router.post("/generate")
def generate_draft(req: DraftRequest):
    # 1) fetch email from DB
    email = get_email_by_message_id(req.message_id)
    if not email:
        logger.warning("Draft generation: email not found message_id=%s", req.message_id)
        raise HTTPException(status_code=404, detail=f"Email with message_id={req.message_id} not found")

    subject = email.get("subject", "")
    body = email.get("body", "")

    # 2) call AI generator with try/except to surface errors
    try:
        draft, contexts = generate_draft_reply(
            subject=subject,
            body=body,
            category=email.get("category", "general"),
            sentiment=email.get("sentiment", "neutral"),
            extracted=email.get("extracted", {})
        )
    except Exception as e:
        tb = traceback.format_exc()
        logger.error("Error generating draft for %s: %s\n%s", req.message_id, e, tb)
        # return 502 Bad Gateway if external service failed (OpenAI)
        raise HTTPException(status_code=502, detail=f"AI generation failed: {str(e)}")

    # 3) upsert email with draft and contexts (make contexts JSON safe)
    try:
        email["ai_draft"] = draft
        email["ai_contexts"] = contexts
        email["status"] = "drafted"
        upsert_email(email)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error("Error upserting email after draft generation: %s\n%s", e, tb)
        raise HTTPException(status_code=500, detail="Failed to save draft to DB")

    return {"message_id": req.message_id, "ai_draft": draft, "contexts": contexts}
    