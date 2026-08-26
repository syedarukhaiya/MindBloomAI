# MindBloomAI

**Your mind deserves a safe place to bloom.**

MindBloomAI is a private, safety-aware AI wellbeing companion designed around the emotional realities of Indian youth: exams, career pressure, parental expectations, loneliness, social comparison and burnout. It is not a therapist, diagnostic system, crisis replacement or medical advice platform.

## Product flow
Share → Understand → Reflect → Bloom → Reach support when needed.

## What is implemented
- FastAPI + SQLAlchemy + Alembic + PostgreSQL-compatible architecture
- JWT authentication and user data isolation
- Mood tracking with stress/energy/context
- Private diary CRUD + AI reflection
- Bloom conversational AI with listener mode
- Safety pre-check and post-generation policy gate
- Google Cloud Vertex AI / Gemini provider abstraction
- Context engine using user-owned moods, reflections and approved memory
- Emotional pattern/trend APIs and weekly reflection
- Micro-interventions and Bloom Garden/gamification
- Multilingual language preference: English, Hindi, Kannada (provider-driven generation)
- Privacy center: memory controls, export, account deletion
- Trusted Support Circle
- Support resources without fabricated provider listings
- Smart reminders
- Responsive glassmorphism frontend
- Demo mode with clearly labelled demo data

## Google Cloud AI
The production AI path is a real Vertex AI Gemini integration through `google-genai`. Configure Google Application Default Credentials and: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GEMINI_MODEL`. If credentials are absent, Bloom explicitly uses a **DEVELOPMENT FALLBACK** so the demo never falsely claims Gemini.

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend defaults to `http://127.0.0.1:8000/api/v1`; override with `VITE_API_BASE_URL`.

## Tests
`cd backend && pytest -q`

## Safety
High-risk language is intercepted before normal generation. MindBloomAI does not diagnose, prescribe, fabricate crisis numbers, contact a person automatically, or claim to have contacted emergency services. Real-world support resources must be verified and maintained.

## Demo
See `docs/demo.md` for the 3-minute judge flow.
