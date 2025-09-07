Email AI Assistant – Project Documentation
1. Project Overview

Email AI Assistant is a full-stack application designed to automate and simplify email workflows using AI. It integrates with Gmail APIs for email access and OpenAI for generating intelligent responses, summaries, and suggestions.

The system is built with a modular architecture where backend services handle authentication, API integration, and business logic, while the frontend provides a clean and interactive UI for end users.

2. Architecture
🔹 Frontend

Framework: React + TailwindCSS

Responsibilities:

User interface for login and email management

Calls backend APIs for authentication and email operations

Displays AI-generated responses, summaries, and suggestions

🔹 Backend

Framework: Python (FastAPI / Flask)

Responsibilities:

OAuth2 flow with Gmail for user login and API access

Securely fetch, read, and send emails

Integrate with OpenAI APIs for AI-based tasks

Expose REST APIs for the frontend

🔹 Config & Secrets Management

Local files (.env, credentials.json) are ignored from version control for security

Example files (.env.example, credentials.json.example) are provided for setup guidance

In production/deployment, environment variables are injected securely via host configuration or CI/CD secrets

🔹 Data Flow

Frontend login → Redirects to Google OAuth → Token returned to backend

Backend stores token → Uses Gmail API for reading/writing emails

AI Integration → Backend sends email content to OpenAI → Returns summaries/suggestions

Frontend renders results → User can view/manage responses in real time

3. Approach Used

Decoupled design: Clear separation between frontend and backend

Secure by default: Secrets never committed; .gitignore protects sensitive files

Example-driven setup: Placeholder example files help others configure their own credentials safely

Scalable integration: APIs are modular, so new AI models or mail providers can be plugged in easily

User-centric: Focus on making email management simple with minimal clicks

4. Setup Instructions (Short)

Clone the repo

Copy example files and fill with real values:

cp backend/.env.example backend/.env
cp backend/app/config/credentials.json.example backend/app/config/credentials.json


Install dependencies (backend + frontend)

Run backend → then run frontend

Login with Gmail → start managing emails with AI support
