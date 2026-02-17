# Deployment Guide - AI Agent RAG System

## Quick Deploy (Recommended Platforms)

### Option 1: Railway (Easiest)

**1) Create Railway Account**
- Go to https://railway.app
- Sign up with GitHub

**2) Add Database (PostgreSQL)**
- New Project → Add PostgreSQL plugin
- Get connection string from Variables

**3) Add Backend Service**
- Connect your GitHub repo
- Service: `backend`
- Root Directory: `backend`
- Environment variables:
  ```
  SUPABASE_DB_URL=<your-postgres-connection-string>
  LLM_PROVIDER=hf
  HF_MODEL=mistralai/Mistral-7B-Instruct-v0.1
  ```
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**4) Deploy**
- Push to GitHub → Railway auto-deploys

---

### Option 2: Render (Alternative)

**1) Create Render Account**
- Go to https://render.com
- Sign up with GitHub

**2) Add PostgreSQL**
- New + → PostgreSQL
- Copy connection string

**3) Deploy Backend**
- New + → Web Service
- Connect GitHub repo
- Settings:
  ```
  Build Command: pip install -r requirements.txt
  Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- Environment:
  ```
  SUPABASE_DB_URL=<postgres-connection>
  LLM_PROVIDER=hf
  HF_MODEL=mistralai/Mistral-7B-Instruct-v0.1
  PYTHONUNBUFFERED=true
  ```

**4) Deploy**
- Click Deploy → done

---

## Local to Git (Prerequisites)

Before deploying, ensure your repo is ready:

```bash
# Navigate to project directory
git init
git add .
git commit -m "Initial commit: AI Agent RAG System"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

---

## Post-Deployment

1. **Test Endpoints**
   ```
   curl https://<your-app>.railway.app/api/health
   curl https://<your-app>.railway.app/
   ```

2. **Run Schema SQL**
   - In deployed database, execute [database/schema.sql](database/schema.sql)

3. **Access Dashboard**
   - Go to `https://<your-app>.railway.app`

---

## Environment Variables Checklist

| Variable | Value | Required |
|----------|-------|----------|
| `SUPABASE_DB_URL` | PostgreSQL connection string | ✅ |
| `LLM_PROVIDER` | `hf` (Hugging Face) | ✅ |
| `HF_MODEL` | Model name | ✅ |
| `HF_API_TOKEN` | (optional, for rate limits) | ❌ |
| `PYTHONUNBUFFERED` | `true` | ✅ |

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'psycopg'"**
- Ensure Python 3.12+
- Check requirements.txt installed

**"Connection refused" on DB**
- Verify SUPABASE_DB_URL in deployed env vars
- SQL schema must be applied to database

**Search returns empty**
- Ensure documents indexed via `/api/embeddings/index`
- Seed demo data via Dashboard or API

---

## Cost Estimate

| Service | Free Tier | Price |
|---------|-----------|-------|
| Railway PostgreSQL | 7 days | $15/month stable |
| Railway Backend | 512MB RAM | $5/month |
| **Total** | Trial | ~$20/month |

Render: Similar ($7-15/month)

---

## Performance Notes

- **Cold starts**: 5-10s first request (both platforms)
- **Embeddings**: 2-5s per document (HF API)
- **Vector search**: <100ms on pgvector
- **Chat response**: 10-30s (depends on LLM)

---

## Next Steps

1. Push code to GitHub
2. Choose Railway or Render
3. Connect repo
4. Set env vars
5. Deploy
6. Run schema SQL on deployed DB
7. Test dashboard

Questions? Check API status endpoint or logs in your platform dashboard.
