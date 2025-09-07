
"""backend/app/config.py
import os
from dotenv import load_dotenv

# Load .env file (backend/.env)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH)

# --- OPENAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./emails.db")

# --- App ---
APP_ENV = os.getenv("APP_ENV", "development")
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")

"""

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Environment variables
APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./emails.db")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Security key
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_fallback_key")
