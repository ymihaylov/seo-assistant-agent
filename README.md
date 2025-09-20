# SEO Assistant Agent (PoC)

A proof of concept **SEO Assistant Agent** implemented as a chat-style application. Users describe their business and web page, and the AI agent returns optimized SEO suggestions that can be iteratively refined through conversation.

**What the agent generates:**
- Page title and content
- Title tag
- Meta description
- Meta keywords

---

## Features

- Multiple chat sessions with persistent history
- Real-time interaction with the AI agent
- Create, rename, and delete sessions
- Iterative refinement — send follow-up prompts to adjust results ("I don't like the title, add more power words")
- Auth0-based authentication with JWT validation on the backend

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite, React Router, Auth0 SPA SDK |
| Backend | Python 3.12, FastAPI, LangGraph, SQLite |
| AI Model | OpenAI `gpt-4o-mini` (JSON mode for structured SEO output) |
| Auth | Auth0 (RS256 JWT, JWKS validation) |

---

## How the Agent Works

LangGraph powers the AI agent by encoding the workflow as a state graph:

```
suggest → validate → score
```

The agent manages conversation context across messages within a session, so follow-up prompts refine the previous output rather than starting fresh.

The frontend always uses the **asynchronous endpoints** — the backend processes prompts via FastAPI `BackgroundTasks` and the frontend polls for the result. Synchronous endpoints exist only for debugging.

---

## Project Structure

```
seo-assistant-agent/
├── api/                        # FastAPI backend
│   ├── app/
│   │   ├── api/endpoints/      # Session, message, and job endpoints
│   │   ├── core/               # Settings, database, auth config
│   │   ├── models/             # SQLAlchemy models
│   │   ├── repositories/       # Data access layer
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   └── services/           # LangGraph agent and business logic
│   ├── requirements.txt
│   └── .env.example
└── seo-assistant-frontend/     # React + Vite frontend
    ├── src/
    │   ├── components/         # UI components (chat, sessions, auth)
    │   ├── hooks/              # Custom React hooks
    │   ├── services/           # API client
    │   └── utils/
    ├── package.json
    └── .env.example
```

---

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/) (includes npm)
- An [Auth0](https://auth0.com/) account
- An [OpenAI](https://platform.openai.com/) API key

---

## Auth0 Setup

Before running the project, create two Auth0 applications:

**1. Single Page Application** (for the frontend)
- Type: Single Page Application
- Allowed Callback URLs: `http://localhost:5173`
- Allowed Logout URLs: `http://localhost:5173`
- Allowed Web Origins: `http://localhost:5173`
- Note the **Domain** and **Client ID**

**2. API** (for the backend)
- Type: API
- Identifier (audience): e.g. `https://seo-assistant-api`
- Signing Algorithm: RS256
- Note the **Domain** and **Audience**

---

## Backend Setup

```bash
cd api
```

Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Copy and fill in the environment file:
```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `AUTH0_DOMAIN` | Your Auth0 domain (e.g. `your-tenant.auth0.com`) |
| `AUTH0_AUDIENCE` | Your Auth0 API identifier |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `OPENAI_MODEL` | Model to use (default: `gpt-4o-mini`) |
| `OPENAI_BASE_URL` | Optional custom OpenAI base URL |

Start the server:
```bash
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

---

## Frontend Setup

```bash
cd seo-assistant-frontend
```

Install dependencies:
```bash
npm install
```

Copy and fill in the environment file:
```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `VITE_API_URL` | Backend URL (e.g. `http://localhost:8000`) |
| `VITE_AUTH0_DOMAIN` | Your Auth0 domain |
| `VITE_AUTH0_CLIENT_ID` | Your Auth0 SPA client ID |
| `VITE_AUTH0_AUDIENCE` | Your Auth0 API identifier |

Start the dev server:
```bash
npm run dev
```

- App: `http://localhost:5173`

---

## Running the Full Stack

Open two terminals and run both services simultaneously:

```bash
# Terminal 1 — backend
cd api && source .venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2 — frontend
cd seo-assistant-frontend && npm run dev
```

Then open `http://localhost:5173` in your browser.

---

## API Overview

- **Sessions**: create, list, update, delete chat sessions
- **Messages**: create, list, delete messages within a session
- **Jobs**: submit a prompt for async processing; poll for result

Interactive API docs: `http://localhost:8000/docs`

A Postman collection is included in the project attachments for easier testing.

---

## Authentication Flow

1. User logs in via Auth0 on the frontend
2. Auth0 issues a JWT access token scoped to the API audience
3. Frontend sends `Authorization: Bearer <token>` on every request
4. Backend validates the token using Auth0's JWKS endpoint (RS256)
5. On first request, the backend auto-creates a user record

---

## Production Readiness — Next Steps

This is a PoC. Known gaps before production use:

- **Database**: Replace SQLite with PostgreSQL or MySQL (concurrency, indexing, JSONB, full-text search)
- **Docker**: Containerize backend and frontend for reproducible deployments
- **Background jobs**: Replace FastAPI `BackgroundTasks` with Celery or RQ — no concurrency limits or retry support currently
- **WebSockets**: Replace polling with real-time push for job progress
- **Pagination**: Messages are fully loaded per session — add pagination or infinite scroll
- **Frontend caching**: Cache session messages locally to reduce re-fetches on tab switch
- **Rate limiting**: No request throttling — users can spam the LLM API
- **Error handling**: Add health endpoints, structured logging, and graceful fallback if DB or LLM API is down
- **Timezone**: Dates stored in `Europe/Sofia` — normalize to UTC in production
- **Session refresh**: No handling for concurrent updates across multiple browser tabs
- **RAG**: A partial implementation using a vector DB (Chroma/Pinecone) for SEO best-practices retrieval exists on a feature branch
- **Model metadata**: Store raw LLM responses for analysis and debugging
- **Fallback strategies**: No fallback under high load
