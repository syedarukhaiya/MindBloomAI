# MindBloomAI Architecture

```mermaid
flowchart TD
 U[Young person] --> F[React + TypeScript + Vite]
 F --> API[FastAPI /api/v1]
 API --> AUTH[JWT + user isolation]
 API --> SAFETY[Safety pre-check]
 SAFETY --> CTX[Bloom Context Engine]
 CTX --> DB[(PostgreSQL / SQLite local)]
 CTX --> AI[AI Orchestrator]
 AI --> GEM[Google Cloud Vertex AI / Gemini]
 GEM --> POST[Response policy / safety post-check]
 POST --> F
 API --> MOOD[Mood + Wellbeing]
 API --> DIARY[Private Diary]
 API --> PLAN[Activities + Bloom Plan]
 API --> PRIV[Privacy + Memory]
 API --> SUPPORT[Support Circle + verified resources]
```

The critical Bloom path is: Authentication → input validation → safety pre-check → user-approved context retrieval → prompt construction → Gemini → output policy gate → response.

No raw API key is embedded in the frontend or backend source.
