# Implementation Matrix

| Requirement | Status | Implementation |
|---|---|---|
| FastAPI | Done | Modular `/api/v1` service |
| React + TypeScript + Vite | Done | Responsive app shell |
| PostgreSQL / SQLAlchemy | Done | PostgreSQL-compatible SQLAlchemy models; SQLite local dev |
| Alembic | Done | Migration chain through mood context + wellbeing features |
| JWT auth | Done | Registration, login, protected routes |
| Mood | Done | Mood + stress + energy + context |
| Diary | Done | CRUD + Bloom reflection |
| Reminders | Done | Persistent reminder API + UI |
| Gamification | Done | Points, levels, garden, achievements |
| Bloom AI | Done | Conversation, context, listener mode |
| Google Cloud Gemini | Done | Real Vertex AI provider via `google-genai`; credentials required |
| Context Engine | Done | Recent moods, reflections, approved memory |
| Safety | Done | Deterministic pre-check + post-generation gate |
| Multilingual | Done | English, Hindi, Kannada selector passed to AI |
| Voice | Prototype | Browser speech input/output, explicitly not mislabeled as Google Cloud |
| Privacy Center | Done | Memory, export, account deletion APIs + UI |
| Trusted Support Circle | Done | Secure contact API + user-scoped records |
| Support Finder | Safe foundation | Verified resource table; provider directory intentionally empty until verified integration |
| Bloom Circle | Prototype scope | Not enabled as an unsafe unrestricted social network |
| Weekly reflection | Done | AI endpoint with non-AI fallback clearly labeled |
| Explainability | Done | Evidence returned for recent mood/reflection context |
| Demo mode | Done | Separate demo account/data via `/demo/session` |
| Documentation | Done | Architecture, AI, safety, privacy, setup, API, demo, submission |
