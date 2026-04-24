# Write Like Me

AI writing style transfer — paste your writing samples, and any text gets rewritten in your authentic voice.

## Stack
- **Frontend**: Next.js 14 (App Router) + Tailwind CSS + Supabase Auth
- **Backend**: FastAPI (Python 3.11+) + sentence-transformers + pgvector
- **Database**: Supabase (PostgreSQL + pgvector)
- **LLM**: Claude (Anthropic) or OpenAI GPT-4o — user provides their own key

---

## Setup

### 1. Supabase

1. Create a project at [supabase.com](https://supabase.com)
2. Enable the `pgvector` extension: **Database → Extensions → vector**
3. Run `backend/db/migrations/001_initial.sql` in the SQL editor
4. Enable Email Auth: **Authentication → Providers → Email**
5. Copy your Project URL, anon key, and service role key

### 2. Backend

```bash
cd write-like-me/backend

# Create venv and install
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .

# Download NLTK data (one-time)
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Configure env
cp .env.example .env
# Edit .env with your Supabase credentials

# Run
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd write-like-me/frontend

npm install

cp .env.local.example .env.local
# Edit .env.local with your Supabase URL and anon key

npm run dev
```

App: http://localhost:3000

---

## Usage Flow

1. **Sign up** at `/signup`
2. **Onboarding** at `/onboarding` — paste 5–20 writing samples
3. **Rewrite** at `/rewrite` — paste any text, get it back in your voice
4. **Feedback** — Accept / Edit / Reject to improve your profile over time
5. **Dashboard** at `/dashboard` — see your voice metrics

---

## Deploy

**Backend → Railway**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
Set `ALLOWED_ORIGINS` to your Vercel URL.

**Frontend → Vercel**
```
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
NEXT_PUBLIC_API_BASE_URL=https://your-railway-app.up.railway.app/api/v1
```

---

## Architecture

```
User → Next.js → FastAPI → [embed input] → pgvector search → [top 6 similar samples]
                          → [load voice profile summary]
                          → [build prompt: system + few-shot + input]
                          → LLM (Claude / OpenAI)
                          → [content preservation check: cosine sim ≥ 0.92]
                          → rewritten text
```

**Feedback loop**: accepted/edited rewrites are added as new writing samples → profile improves over time.
