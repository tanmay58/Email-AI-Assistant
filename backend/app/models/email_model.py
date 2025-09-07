from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class ExtractedInfo(BaseModel):
    phone_numbers: List[str] = []
    alternate_emails: List[EmailStr] = []
    product_names: List[str] = []
    keywords: List[str] = []

class EmailDoc(BaseModel):
    id: Optional[str] = None            # Gmail API message id
    message_id: Optional[str] = None    # Internet message-id header
    sender: Optional[EmailStr] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    received_at: Optional[datetime] = None
    labels: List[str] = []
    sentiment: Optional[str] = None     # positive / negative / neutral
    priority: Optional[str] = None      # urgent / not_urgent
    category: str = "general"           # support | query | request | help | general
    extracted: ExtractedInfo = Field(default_factory=ExtractedInfo)
    ai_draft: Optional[str] = None
    status: str = "pending"             # pending | replied | snoozed
