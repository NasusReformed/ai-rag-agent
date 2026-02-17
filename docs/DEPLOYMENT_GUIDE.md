# Deployment Guide

This guide covers deploying the AI RAG Agent to production on Railway, the recommended platform for ML workloads.

## Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- Hugging Face account (free token at https://huggingface.co/settings/tokens)

## Step 1: Push to GitHub

Create a new repository:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/ai-rag-agent.git
git branch -M main
git push -u origin main
```

Verify no sensitive files were pushed:
```bash
git log --all --full-history -- .env
# Should return empty
```

## Step 2: Create Railway Project

1. Visit https://railway.app/new
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Wait for initial deployment

## Step 3: Add PostgreSQL

1. In Railway project dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Copy the connection string from the "Connect" tab

## Step 4: Configure Environment

Add these variables in Railway → Variables tab:

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
HF_API_TOKEN=your_huggingface_token
HF_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
OLLAMA_BASE_URL=http://localhost:11434
LLM_PROVIDER=hf
RAG_TOP_K=4
PYTHONUNBUFFERED=true
```

Railway will auto-link the PostgreSQL `DATABASE_URL`.

## Step 5: Initialize Database

1. Click on PostgreSQL service in Railway
2. Open "Query" tab
3. Paste contents of `database/schema.sql`
4. Execute

Verify pgvector extension:
```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

## Step 6: Deploy Configuration

Create `railway.json` in project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Push changes:
```bash
git add railway.json
git commit -m "Add railway config"
git push
```

Railway will auto-deploy the update.

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

### Database connection timeout

Verify `DATABASE_URL` format:
```
postgresql://user:password@host:port/database
```

Railway's `${{Postgres.DATABASE_URL}}` variable should auto-populate correctly.

### pgvector extension not found

Create extension manually:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Some managed PostgreSQL instances require extensions to be enabled in settings first.

### Health check failing

Railway expects `/api/health` to return HTTP 200. Verify the endpoint works:
```bash
railway logs
# Look for uvicorn startup confirmation
```

### Port binding issues

Railway injects `$PORT` environment variable. Ensure start command uses it:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Model loading timeout

On first startup, sentence-transformers downloads ~500MB model. This can take 2-3 minutes. Railway's health check has 100s timeout.

For faster deploys, consider:
- Pre-baking model in Docker image
- Using Railway's persistent disk to cache models
- Switching to lighter embedding model

## Alternative Platforms

### Render

Not recommended for this project. Free tier has insufficient resources for ML models (~500MB sentence-transformers). Paid tier ($7+/month) should work.

### Hugging Face Spaces

Good alternative for ML-focused deployments:
```bash
# Add Space config
git lfs install
git clone https://huggingface.co/spaces/YOUR-USERNAME/ai-rag-agent
# Copy files + configure as Gradio app
```

Requires adapting FastAPI to Gradio interface.

### Fly.io

Solid choice with good free tier, but more complex setup:
```bash
flyctl launch
flyctl postgres create
flyctl postgres attach
flyctl deploy
```

## Post-Deployment

### Custom Domain

Railway: Settings → Domains → Add custom domain

### Environment Updates

Change variables in Railway dashboard, service will restart automatically.

### Logs

Real-time: Railway dashboard → Logs tab

### Database Management

Use Railway's built-in query editor or connect with:
```bash
psql $DATABASE_URL
```

### Scaling

Railway: Settings → Resources → Adjust CPU/RAM

Minimum for ML model: 1GB RAM

### Monitoring

Railway provides:
- Request metrics
- Resource usage graphs
- Error tracking

For production, consider adding:
- Sentry for error tracking
- Uptime monitoring (UptimeRobot)
- Log aggregation (Better Stack)
