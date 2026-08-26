# MindBloomAI

**Your mind deserves a safe place to bloom.**

MindBloomAI is a private, safety-aware AI wellbeing companion designed around the emotional realities of youth: exams, career pressure, social challenges, loneliness, social comparison and burnout. It is not a therapist, diagnostic system, crisis replacement or medical advice platform.

## Product flow
Share → Understand → Reflect → Bloom → Reach support when needed.

## What is implemented

### Core Features
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

### NEW: Community & Personal Features
- **MindBloom Circles**: Safe peer wellbeing gathering spaces with moderation
- **Story Garden**: Anonymous story sharing platform with supportive reactions
- **Future Letters**: Write and schedule letters to your future self
- **Gratitude Capsules**: Save moments to revisit later
- **Small Wins Wall**: Share personal achievements anonymously
- **Kindness Messages**: Send anonymous encouragement to community
- **Memory Garden**: Visual progress tracking of wellbeing activities
- **Reflection Prompts**: Guided daily prompts for deeper reflection

## Google Cloud AI
The production AI path is a real Vertex AI Gemini integration through `google-genai`. Configure Google Application Default Credentials and set: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GEMINI_MODEL`. If credentials are absent, Bloom explicitly uses a **DEVELOPMENT FALLBACK** so the demo never falsely claims Gemini.

## Technology Stack

### Backend
- Python 3.9+
- FastAPI 0.141+
- SQLAlchemy 2.0+
- Alembic (database migrations)
- Pydantic (validation)
- Argon2 (password hashing)
- PyJWT (authentication)
- PostgreSQL-compatible (SQLite for dev)

### Frontend
- React 19
- TypeScript
- Vite
- Glassmorphism CSS design system

### Database
- PostgreSQL (production)
- SQLite (development)
- Supabase-ready

## Run locally

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Backend Setup
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Copy environment variables (already done, or customize):
# cp .env.example .env

# Initialize database
alembic upgrade head

# Run development server
uvicorn app.main:app --reload

# Server will be available at http://127.0.0.1:8000
# API docs at http://127.0.0.1:8000/docs
```

### Frontend Setup
```bash
cd frontend

npm install

# Development server
npm run dev

# Build for production
npm run build

# Type checking
npm run type-check
```

Frontend defaults to `http://127.0.0.1:8000/api/v1`; override with `VITE_API_BASE_URL` in `.env`.

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Moods & Tracking
- `GET /api/v1/moods` - Get mood history
- `POST /api/v1/moods` - Log mood check-in

### Diary
- `GET /api/v1/diary` - Get diary entries
- `POST /api/v1/diary` - Create diary entry
- `GET /api/v1/diary/{id}` - Get specific entry

### Circles (Community)
- `GET /api/v1/circles` - List all circles
- `POST /api/v1/circles` - Create circle
- `POST /api/v1/circles/{id}/join` - Join circle
- `POST /api/v1/circles/{id}/leave` - Leave circle
- `GET /api/v1/circles/my-circles` - Get user's circles

### Stories (Anonymous Sharing)
- `GET /api/v1/stories` - Get all stories
- `POST /api/v1/stories` - Share anonymous story
- `POST /api/v1/stories/{id}/reactions` - Add reaction
- `POST /api/v1/stories/{id}/report` - Report story

### Personal Reflection
- `POST /api/v1/future-letters` - Create letter to future self
- `GET /api/v1/gratitude-capsules` - Get gratitude capsules
- `POST /api/v1/gratitude-capsules` - Create capsule
- `GET /api/v1/small-wins` - Get small wins
- `POST /api/v1/small-wins` - Share small win
- `GET /api/v1/garden` - Get memory garden progress

### AI & Wellbeing
- `POST /api/v1/bloom/chat` - Chat with Bloom AI
- `POST /api/v1/bloom/reflection` - Get AI reflection on diary entry
- `GET /api/v1/recommendations` - Get personalized recommendations
- `GET /api/v1/wellbeing/insights` - Get wellbeing insights

## Database Migrations

The project uses Alembic for database versioning:

```bash
cd backend

# Show current migration status
alembic current

# Upgrade to latest migration
alembic upgrade head

# Create new migration (after model changes)
alembic revision --autogenerate -m "description"

# Downgrade to previous migration
alembic downgrade -1
```

## Tests

### Backend Tests
```bash
cd backend
python -m pytest -v  # Verbose output
python -m pytest -q  # Quiet output
python -m pytest tests/test_api.py  # Specific test file
```

### Frontend Type Checking
```bash
cd frontend
npm run type-check
```

## Safety & Privacy

### Security Measures
- High-risk language is intercepted before normal generation
- All user data is isolated by user_id
- Passwords are hashed with Argon2
- JWT tokens expire after 120 minutes
- CORS is configured for approved origins
- Private diary entries are access-controlled

### MindBloomAI Principles
- Does not diagnose, prescribe, or claim medical certainty
- Does not fabricate crisis resources or provider numbers
- Does not contact emergency services automatically
- Does not claim to be emergency care
- Encourages users to seek professional help when appropriate
- Respects user privacy and consent
- Only uses approved, user-permitted context for AI interactions

## Configuration

### Environment Variables

**Backend (.env)**
- `DATABASE_URL`: PostgreSQL connection string
- `GOOGLE_CLOUD_PROJECT`: GCP project ID for Gemini AI (optional)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCP credentials JSON
- `JWT_SECRET_KEY`: Secret key for token signing (change in production)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `AI_ENABLED`: Enable/disable AI features (default: true)

**Frontend (.env)**
- `VITE_API_BASE_URL`: Backend API base URL
- `VITE_DEMO_MODE`: Enable demo mode with sample data

## Deployment

### Production Database
Replace `DATABASE_URL` with PostgreSQL:
```
postgresql+psycopg://user:password@host:5432/mindbloom
```

### Production Build
```bash
# Backend
export JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
# Deploy with proper secrets management (not in .env)

# Frontend
npm run build
# Deploy dist/ folder to static hosting
```

## Demo Flow

1. Land on MindBloomAI landing page
2. Register or login (or try demo)
3. Complete mood check-in with context
4. Receive personalized wellbeing suggestions
5. Chat with Bloom AI companion
6. Create a private diary reflection
7. Receive AI reflection on your entry
8. Browse and join MindBloom Circles
9. View or share anonymous stories
10. Track progress in your Bloom Garden

## Project Structure

```
MindBloomAi/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── controllers/  # API route handlers
│   │   │   └── router.py    # API router
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Business logic
│   │   ├── security/        # Auth & JWT
│   │   ├── core/            # Configuration
│   │   └── db/              # Database setup
│   ├── alembic/             # Database migrations
│   ├── tests/               # Test suite
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── lib/             # Utilities and API client
│   │   ├── types/           # TypeScript types
│   │   ├── App.tsx          # Main app component
│   │   └── main.tsx         # Entry point
│   ├── package.json         # Node dependencies
│   ├── tsconfig.json        # TypeScript config
│   └── vite.config.ts       # Vite configuration
│
└── docs/                    # Documentation
```

## Contributing

The codebase follows these patterns:

- **Backend**: FastAPI controllers return Pydantic schema responses
- **Frontend**: React hooks handle state, components are pure UI
- **Database**: SQLAlchemy ORM with proper relationships and indexing
- **API**: RESTful endpoints with proper HTTP status codes
- **Testing**: Unit tests mock external services

## Support & Resources

- **Documentation**: See `docs/` folder
- **API Reference**: http://localhost:8000/docs (Swagger UI)
- **Architecture**: See `docs/architecture.md`
- **Safety**: See `docs/safety.md`
- **Privacy**: See `docs/privacy.md`

## License

See LICENSE file

---

**Built for the hackathon with 💜 for emotional wellbeing.**

