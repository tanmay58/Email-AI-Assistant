""""
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import route modules (these should each define `router = APIRouter()`)
from app.routes import email_routes
from app.routes import analytics_routes
from app.routes import reply_routes
from app.routes import draft_routes

app = FastAPI(
    title="Email AI Assistant",
    description="Backend API for AI-powered email triage, analytics, and draft generation",
    version="0.1.0",
)

# CORS - allow your frontend (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],  # common dev ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers with prefixes and tags
app.include_router(email_routes.router, prefix="/emails", tags=["Emails"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])
app.include_router(reply_routes.router, prefix="/reply", tags=["Reply"])
app.include_router(draft_routes.router, prefix="/drafts", tags=["Drafts"])

# Root / health endpoint
@app.get("/", summary="Service status")
def root():
    return {"message": "Backend is running!"}
    
    """
    
    # app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import email_routes, draft_routes, reply_routes, analytics_routes

app = FastAPI(title="Email AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_routes.router)
app.include_router(draft_routes.router)
app.include_router(reply_routes.router)
app.include_router(analytics_routes.router)

@app.get("/")
def root():
    return {"message": "Backend is running!"}

