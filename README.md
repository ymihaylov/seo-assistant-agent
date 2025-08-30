# 🚀 SEO Assistant Agent (PoC)

This project is a **Proof of Concept (PoC)** for an SEO Assistant Agent.  
It provides a **chat-style interface** where authenticated users can describe their business or page, and the AI agent returns optimized SEO suggestions:  
- Page Title  
- Page Content  
- Title Tag  
- Meta Description  
- Meta Keywords  

Users can iteratively refine results by sending additional prompts.

---

## 📦 Tech Stack
- **Backend**: Python 3.12, FastAPI, LangGraph, SQLite (PoC)
- **Frontend**: React 19, Vite, Auth0
- **AI Model**: OpenAI `gpt-4o-mini`

---

## 🔧 Prerequisites
- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [npm](https://docs.npmjs.com/) (comes with Node.js) or Yarn
- [Auth0 account](https://auth0.com/) (for authentication)
- OpenAI API key

---

## ⚙️ Backend Setup (FastAPI)

1. Navigate to the backend directory:
```bash
cd api
```

2. Create and activate a virtual environment: 
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows```
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy environment file
```bash
cp .env.example .env
```
Fill in values for:
- AUTH0_DOMAIN
- AUTH0_AUDIENCE
- OPENAI_API_KEY

**(The link with these secrets is provided in the other documentation in Google Docs)**

5. Run the server:
```bash
uvicorn app.main:app --reload
```
- API runs at: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

## 🎨 Frontend Setup (React + Vite)
1. Navigate to the frontend directory:
```bash
cd seo-assistant-frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Copy environment file:
```bash
cp .env.example .env
```
Fill in values for:
- VITE_API_URL=http://localhost:8000
- VITE_AUTH0_DOMAIN=...
- VITE_AUTH0_CLIENT_ID=...
- VITE_AUTH0_AUDIENCE=...

**(The link with these secrets is provided in the other documentation in Google Docs)**

4. Run the dev server:
```bash
npm run dev
```

## ✅ Notes
- The frontend communicates with the backend asynchronously.
- Use the async endpoints for production; synchronous endpoints are for debugging only.
- SQLite is used here for simplicity. For production use PostgreSQL or MySQL.

## 📘 API Docs
- Interactive API docs: http://localhost:8000/docs
- Postman collection is included in the project attachments.
