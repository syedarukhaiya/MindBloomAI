# Setup

1. Install Python 3.12 and Node.js.
2. Create `backend/.env` from `.env.example`.
3. For PostgreSQL, set `DATABASE_URL` to a `postgresql+psycopg://...` URL.
4. Run `alembic upgrade head`.
5. Start FastAPI and Vite.
6. For live Gemini, configure Google Cloud Application Default Credentials or a service-account path and set project/location/model.
