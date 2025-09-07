from fastapi import FastAPI
from app.routes import email_routes, analytics_routes, reply_routes

app = FastAPI(title="AI-Powered Communication Assistant")

# include routers
app.include_router(email_routes.router, prefix="/emails", tags=["Emails"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])
app.include_router(reply_routes.router, prefix="/replies", tags=["Replies"])

@app.get("/", summary="Root endpoint")
def root():
    return {"message": "AI Communication Assistant is running 🚀"}
