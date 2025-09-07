import os, pickle, base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



# Gmail API scopes (read + send emails)
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

CREDENTIALS_PATH = "app/config/credentials.json"
TOKEN_PATH = "app/config/token.pickle"

def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    # If no valid creds, do OAuth2 flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(f"Missing credentials.json at {CREDENTIALS_PATH}")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

def send_gmail(to: str, subject: str, body: str):
    """Send an email using Gmail API"""
    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return service.users().messages().send(userId="me", body={"raw": raw}).execute()
