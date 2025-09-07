
"""from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["email_db"]
emails_collection = db["emails"]

def list_emails():
    Return all stored emails from the database
    return list(emails_collection.find({}, {"_id": 0}))  # hide Mongo _id

def save_email(email_data: dict):
    Insert or update an email in the database
    if not email_data.get("id"):
        raise ValueError("Email must have an id field")

    emails_collection.update_one(
        {"id": email_data["id"]},
        {"$set": email_data},
        upsert=True  # avoid duplicates
    )

def clear_emails():
    Delete all emails (for testing/reset)
    emails_collection.delete_many({})"""
    
    
# app/utils/db.py
from pymongo import MongoClient
import os
from app.config import DATABASE_URL

# Create client and validate connection quickly (small timeout)
client = MongoClient(DATABASE_URL, serverSelectionTimeoutMS=5000)

# Try to trigger connection errors early (will raise if cannot connect)
try:
    client.server_info()
except Exception as e:
    # Re-raise with clearer message
    raise RuntimeError(f"Could not connect to MongoDB using DATABASE_URL={DATABASE_URL!r}: {e}")

# Use default database if present in the URI, otherwise fall back to 'email_db'
_default_db = client.get_default_database()
if _default_db is not None:
    db = _default_db
else:
    db = client["email_db"]

emails_collection = db["emails"]
kb_collection = db["kb"]

def list_emails():
    """Return all stored emails as list of dicts (convert _id to str)."""
    docs = list(emails_collection.find({}))
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return docs

def get_email_by_message_id(message_id: str):
    return emails_collection.find_one({"message_id": message_id})

def upsert_email(doc: dict):
    emails_collection.update_one({"message_id": doc["message_id"]}, {"$set": doc}, upsert=True)
    return emails_collection.find_one({"message_id": doc["message_id"]})
