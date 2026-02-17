# Setup Guide

This guide covers setting up the AI RAG Agent for local development using Supabase as the database backend.

## Prerequisites

- Python 3.12+
- Git
- Supabase account (free at https://supabase.com)
- Hugging Face account (free token at https://huggingface.co/settings/tokens)

## Step 1: Clone Repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-rag-agent.git
cd ai-rag-agent
```

## Step 2: Create Supabase Project

1. Visit https://supabase.com/dashboard
2. Click "New project"
3. Fill in project details:
   - Name: `ai-rag-agent`
   - Database Password: (save this securely)
   - Region: Choose closest to you
4. Wait for project creation (~2 minutes)

## Step 3: Get Database Connection

1. In your project dashboard, go to **Settings** → **Database**
2. Scroll to "Connection string"
3. Select **URI** mode
4. Copy the connection string (looks like):
   ```
   postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
5. Note: The password is already included if you copy from the dashboard

## Step 4: Initialize Database Schema

**Option A: Supabase SQL Editor**
1. Go to **SQL Editor** in your project
2. Click "New query"
3. Open `database/schema.sql` from the repository
4. Copy all contents and paste into the editor
5. Click "Run" (or press Ctrl+Enter)
6. Verify success: Check for `pg_extension` table in Table Editor

**Option B: Command Line**
```bash
# Set your connection string
export DATABASE_URL="postgresql://postgres:..."

# Run schema
psql $DATABASE_URL < database/schema.sql
```

The schema creates:
- Documents table with vector embeddings
- Agent sessions and messages tables
- Users, events, and tickets tables
- pgvector extension (pre-installed on Supabase)

## Step 7: Verify Deployment

Check service health:
```bash
curl https://your-app.railway.app/api/health
# Should return: {"status":"ok"}
```

Test frontend:
```
https://your-app.railway.app
```

Load demo data and test chat functionality.

## Troubleshooting

### Build fails with "Module not found"

Ensure `backend/requirements.txt` includes all dependencies:
```bash
cd backend
pip freeze > requirements.txt
```

## Step 5: Configure Local Environment

Create `.env` file in project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# Supabase connection (from Step 3)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Hugging Face token (from https://huggingface.co/settings/tokens)
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
HF_MODEL=meta-llama/Llama-3.2-3B-Instruct

# Embeddings model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# RAG configuration
RAG_TOP_K=4

# LLM provider
LLM_PROVIDER=hf
```

**Never commit `.env` to git** - it's already in `.gitignore`.

## Step 6: Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

This installs:
- FastAPI and uvicorn (web server)
- sentence-transformers (embeddings)
- psycopg[pool] (PostgreSQL driver)
- Other dependencies (~500MB total)

First run will download the embedding model (~80MB).

## Step 7: Start Server

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Step 8: Verify Setup

Open http://localhost:8000 in your browser.

**Quick test:**
1. Click "Load Demo Data" button
2. Go to Chat tab
3. Ask: "What are the support hours?"
4. Verify response uses RAG context

**API test:**
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"ok"}
```

## Troubleshooting

### Database connection failed

**Symptom:** `error connecting in 'pool-1': connection failed`

**Solutions:**
1. Verify DATABASE_URL format:
   ```
   postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
2. Check password has no special characters that need URL encoding
3. Ensure Supabase project is not paused (free tier pauses after 7 days inactivity)
4. Test connection directly:
   ```bash
   psql $DATABASE_URL -c "SELECT version();"
   ```

### pgvector extension not found

**Symptom:** `ERROR: extension "vector" does not exist`

**Solution:**
Supabase has pgvector pre-installed. If you see this error:
```sql
-- Run in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

### Port 8000 already in use

**Symptom:** `WinError 10013` or `Address already in use`

**Solutions:**
```bash
# Windows
Get-Process | Where-Object {$_.Name -like "*python*"} | Stop-Process -Force

# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

### HF_API_TOKEN authentication failed

**Symptom:** `401 Unauthorized` when calling Hugging Face API

**Solutions:**
1. Generate new token at https://huggingface.co/settings/tokens
2. Ensure token has "Read access to contents of all public gated repos you can access"
3. Verify token in `.env` starts with `hf_`
4. Try a different model (some require acceptance of terms):
   ```bash
   HF_MODEL=mistralai/Mistral-7B-Instruct-v0.1
   ```

### Model download timeout

**Symptom:** First startup takes 2-3 minutes

**Explanation:**
On first run, sentence-transformers downloads the embedding model (~80MB). This is normal and only happens once. The model is cached at:
- Windows: `C:\Users\USERNAME\.cache\huggingface`
- Linux/macOS: `~/.cache/huggingface`

### Memory issues

**Symptom:** Process killed or out of memory

**Solution:**
The sentence-transformers model requires ~500MB RAM. Ensure:
- At least 2GB free RAM
- No other heavy processes running
- Virtual environment is activated

## Database Management

### Access Supabase Database

**Via Web UI:**
1. Go to Supabase Dashboard
2. Select your project
3. Click "Table Editor" or "SQL Editor"

**Via psql:**
```bash
psql $DATABASE_URL
```

**Via GUI Client:**
Use DBeaver, pgAdmin, or TablePlus with the connection string.

### Reset Database

```bash
# Drop all tables
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Re-run schema
psql $DATABASE_URL < database/schema.sql
```

### Seed Demo Data

Load sample documents via API:
```bash
curl -X POST http://localhost:8000/api/demo/seed-data
```

Or use the "Load Demo Data" button in the web UI.

## Production Considerations

While this project is designed for local development and portfolio demonstration, if you want to deploy it:

### Recommended Platforms
- **Railway** - Best for ML workloads, ~$20/month
- **Fly.io** - Good free tier, more setup required
- **Hugging Face Spaces** - Free for public repos, ML-optimized

### Not Recommended
- **Render Free Tier** - Insufficient RAM for sentence-transformers
- **Heroku Free Tier** - Discontinued
- **Vercel/Netlify** - Not suitable for ML backends

### Pre-Deployment Checklist
- [ ] Remove demo/debug endpoints
- [ ] Add rate limiting
- [ ] Configure CORS properly
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Use environment-specific configs
- [ ] Add health check endpoints
- [ ] Configure logging

## Next Steps

- Review [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) for architecture details
- Check `api/requests.http` for example API calls
- Explore the web dashboard at http://localhost:8000
- Read the code in `backend/app/` to understand implementation
