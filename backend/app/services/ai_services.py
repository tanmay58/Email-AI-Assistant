# app/services/ai_services.py
"""
AI draft generation — uses OpenAI Python client v1 (openai>=1.0.0).
If OPENAI_API_KEY is missing or the API call fails, a small local template reply
is returned so the app remains demo-friendly during hackathons / offline tests.
"""

from typing import Tuple, List, Dict
import logging
import os

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.services.rag_service import retrieve_contexts

logger = logging.getLogger("uvicorn.error")

# Try new OpenAI client
try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except Exception:
    OpenAI = None
    _OPENAI_AVAILABLE = False

SYSTEM_PROMPT = (
    "You are a helpful, empathetic customer support assistant. "
    "Use only the provided context snippets for factual information. "
    "If the information is insufficient, ask a clarifying question. "
    "Keep replies short (2-6 sentences) and end with a clear next step."
)

def _build_user_prompt(subject: str, body: str, category: str, sentiment: str, extracted: dict, contexts: list) -> str:
    ctx_text = ""
    for i, c in enumerate(contexts):
        meta = c.get("meta", {}) or {}
        fname = meta.get("filename") or meta.get("id") or ""
        snippet = c.get("text", "")
        snippet_short = snippet if len(snippet) <= 1500 else snippet[:1500] + "..."
        ctx_text += f"[{i+1}] {snippet_short}\n-- source: {fname}\n\n"

    extracted_summary = ""
    if extracted:
        extracted_summary = f"Extracted: phones={extracted.get('phone_numbers',[])}, emails={extracted.get('alternate_emails',[])}, keywords={extracted.get('keywords',[])}"

    prompt = (
        f"Email subject: {subject}\n"
        f"Email body: {body}\n\n"
        f"Category: {category}\n"
        f"Sentiment: {sentiment}\n"
        f"{extracted_summary}\n\n"
        f"Relevant contexts (top {len(contexts)}):\n{ctx_text}\n"
        "Instruction:\n"
        "Write a short (2-6 sentences) professional reply. If sentiment is negative, start with empathy. "
        "Use only the provided contexts for facts; if you cannot answer from them, ask a clarifying question. "
        "End with the next expected step for the customer."
    )
    return prompt

def _local_template_reply(subject: str, body: str, category: str, sentiment: str, extracted: dict) -> str:
    # Lightweight fallback for demo/offline
    if sentiment == "negative":
        intro = "Sorry you're experiencing this — I understand how frustrating it can be."
    elif sentiment == "positive":
        intro = "Thanks for the update — that's great to hear!"
    else:
        intro = "Thanks for reaching out."
    next_step = "Could you please share any error messages or screenshots so we can investigate?"
    return f"{intro} {next_step}"

def generate_draft_reply(
    subject: str,
    body: str,
    category: str = "general",
    sentiment: str = "neutral",
    extracted: dict = None,
    top_k_contexts: int = 3,
) -> Tuple[str, List[Dict]]:
    """
    Returns (draft_text, contexts)
    """

    extracted = extracted or {}
    # 1) retrieve contexts using RAG (may be empty)
    query = f"{subject}\n\n{body}"
    contexts = retrieve_contexts(query, top_k=top_k_contexts) or []

    # If OpenAI not available or no API key -> fallback template
    if not OPENAI_API_KEY or not _OPENAI_AVAILABLE:
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set — using local template reply.")
        elif not _OPENAI_AVAILABLE:
            logger.warning("OpenAI client not installed/compatible — using local template reply.")
        return _local_template_reply(subject, body, category, sentiment, extracted), contexts

    # Build messages
    user_prompt = _build_user_prompt(subject, body, category, sentiment, extracted, contexts)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    # instantiate OpenAI client (v1)
    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        resp = client.chat.completions.create(
            model=OPENAI_MODEL or "gpt-3.5-turbo",
            messages=messages,
            max_tokens=450,
            temperature=0.2,
        )
        # response shape: resp.choices[0].message.content
        draft_text = resp.choices[0].message.content.strip()
        return draft_text, contexts
    except Exception as e:
        logger.error("OpenAI call failed: %s", e, exc_info=True)
        # fallback to template on API failure so UI still works
        return _local_template_reply(subject, body, category, sentiment, extracted), contexts
