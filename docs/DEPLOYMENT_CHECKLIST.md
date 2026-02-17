# 🚀 Deployment Checklist

Complete step-by-step to deploy your AI Agent RAG System to production.

---

## Phase 1: Prepare Local Code ✅

- [x] Backend API working locally (`http://localhost:8000`)
- [x] Dashboard loads in browser
- [x] `.env` configured with Supabase connection
- [x] Database schema applied to Supabase

### Verify:
```bash
cd backend
uvicorn app.main:app --reload
# Should start on http://localhost:8000
```

---

## Phase 2: Set Up GitHub

Follow: **[GITHUB_SETUP.md](GITHUB_SETUP.md)**

### Quick Steps:
1. Create repo: https://github.com/new
2. Initialize locally:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
3. Push:
   ```bash
   git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
   git branch -M main
   git push -u origin main
   ```

### Verify:
- [ ] Repository visible at https://github.com/YOUR-USER/YOUR-REPO
- [ ] All files present (check main branch)
- [ ] No `.env` file with credentials (check `.gitignore`)

---

## Phase 3: Choose Deployment Platform

**Decision guide**: [PLATFORM_CHOICE.md](PLATFORM_CHOICE.md)

| Platform | Recommendation | Cost |
|----------|---|---|
| Railway | ⭐ Fast, modern | $20/month |
| Render | ✅ Cheap, free tier | $0-15/month |

**Recommendation for interviews**: Railway (no cold starts)

---

## Phase 4: Deploy to Railway

Follow: **[RAILWAY_SETUP.md](RAILWAY_SETUP.md)**

### Quick Steps:
1. Go to https://railway.app
2. Login with GitHub
3. New Project → Select your repo
4. Add PostgreSQL (Railway will auto-add)
5. Set environment variables:
   ```
   SUPABASE_DB_URL=<your-db-connection>
   LLM_PROVIDER=hf
   HF_MODEL=mistralai/Mistral-7B-Instruct-v0.1
   EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
   RAG_TOP_K=4
   PYTHONUNBUFFERED=true
   ```
6. Deploy (auto-starts)

### Verify:
- [ ] Deployment shows "Success" in logs
- [ ] `/api/health` returns `{"status": "ok"}`
- [ ] Dashboard loads at `https://<your-app>.railway.app`

---

## Phase 4 (Alternative): Deploy to Render

Follow: **[RENDER_SETUP.md](RENDER_SETUP.md)**

### Quick Steps:
1. Go to https://render.com
2. New Web Service → Select repo
3. Setup:
   ```
   Root Directory: backend
   Build: pip install -r requirements.txt
   Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Add PostgreSQL service
5. Set env vars (same as Railway above)
6. Deploy

### Verify:
- [ ] Build succeeded (check Logs)
- [ ] Service status: "Running"
- [ ] `/api/health` endpoint responding

---

## Phase 5: Initialize Database Schema

### In Railway:
```bash
railway run psql $DATABASE_URL < database/schema.sql
```

Or use Supabase SQL Editor if using separate Supabase:
```
1. Go to Supabase dashboard
2. SQL Editor
3. Paste database/schema.sql
4. Run All
```

### Verify:
- [ ] Tables created: users, documents, agent_sessions, agent_messages, events, tickets
- [ ] pgvector extension enabled
- [ ] No SQL errors

---

## Phase 6: Test Deployed API

### Health Check:
```powershell
Invoke-RestMethod https://<your-app>.railway.app/api/health
# Should return: {"status":"ok"}
```

### Add Test Data:
1. Open dashboard: `https://<your-app>.railway.app`
2. Go to "Documents" tab
3. Click "Load Demo Data" button
4. Wait for success message

### Test Chat:
1. Go to "Chat" tab
2. Type: "What are your support hours?"
3. Should mention the demo data

### Verify:
- [ ] API responds to requests
- [ ] Demo data loads (button feedback)
- [ ] Chat returns answers
- [ ] Dashboard shows "API Status: OK"

---

## Phase 7: Configure DNS (Optional)

If you want a custom domain:

### Railway:
1. Service Settings
2. Domains → Add Domain
3. Point your DNS (CNAME) to Railway URL
4. SSL auto-provisions (~5 min)

### Render:
1. Service Settings
2. Custom Domain
3. Point your DNS CNAME record
4. SSL auto-provisions

---

## Phase 8: Production Checklist

- [ ] **Security**
  - [ ] `.env` not in repo (check `.gitignore`)
  - [ ] Database credentials in platform variables only
  - [ ] CORS configured (already done)
  
- [ ] **Performance**
  - [ ] API responds <1s on `/api/health`
  - [ ] Dashboard loads <3s
  - [ ] Chat response <10s
  
- [ ] **Reliability**
  - [ ] Logs showing no errors
  - [ ] Health endpoint 200 OK
  - [ ] Database connection stable
  
- [ ] **Monitoring**
  - [ ] Check logs regularly
  - [ ] Set up alerts (if platform supports)
  - [ ] Test API monthly

---

## Phase 9: Share & Showcase

### For Interviews:
```
"Our AI Agent is live at: https://your-app.railway.app

Features:
✓ RAG with semantic search
✓ Tool-calling agent
✓ Persistent memory
✓ FastAPI backend
✓ PostgreSQL + pgvector
✓ Production-ready"
```

### Demo Script:
1. Go to dashboard
2. Load demo data (1 click)
3. Ask a question in Chat ("support", "billing", etc.)
4. Show answer from sources
5. Try semantic search tab
6. Show tools tab

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| **"ModuleNotFoundError"** | Check requirements.txt in requirements.txt |
| **DB connection error** | Verify SUPABASE_DB_URL env var |
| **API slow to respond** | Cold start on free tier; upgrade to remove |
| **Empty search results** | Load demo data first, then search |
| **CORS error** | Already fixed; try hard refresh (Ctrl+Shift+R) |

---

## Scaling Later

### If you get traffic:

**Railway**:
1. Service → Instance Type
2. Choose larger size
3. Auto-redeploy (~2 min downtime)

**Render**:
1. Service → Settings
2. Choose Starter tier ($7/month)
3. Auto-scaling included

---

## Next Steps After Deployment

1. ✅ **Deployment Phase Complete**
2. ⏭️ Test with real users
3. ⏭️ Add more documents to KB
4. ⏭️ Integrate Claude API (optional upgrade)
5. ⏭️ Set up n8n workflows (optional)
6. ⏭️ Monitor and optimize

---

## Quick Reference URLs

| Task | URL |
|------|-----|
| GitHub Setup | [GITHUB_SETUP.md](GITHUB_SETUP.md) |
| Railway Deploy | [RAILWAY_SETUP.md](RAILWAY_SETUP.md) |
| Render Deploy | [RENDER_SETUP.md](RENDER_SETUP.md) |
| Choose Platform | [PLATFORM_CHOICE.md](PLATFORM_CHOICE.md) |
| General Guide | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Your Dashboard | https://your-app.railway.app (after deploy) |

---

## Timeline Estimate

| Phase | Time |
|-------|------|
| GitHub Setup | 5 min |
| Deploy to Railway | 10 min |
| Initialize Database | 5 min |
| Test & Verify | 5 min |
| **Total** | **25 minutes** |

---

## Need Help?

1. Check **Common Issues & Fixes** section ↑
2. Read platform-specific guide ([RAILWAY_SETUP.md](RAILWAY_SETUP.md) or [RENDER_SETUP.md](RENDER_SETUP.md))
3. Check deployment logs for errors
4. Verify environment variables are set
5. Test locally first: `uvicorn app.main:app --reload`

---

## Congratulations! 🎉

Your AI Agent RAG System is now in production and ready to:
- ✅ Demonstrate in interviews
- ✅ Share with others
- ✅ Handle real requests
- ✅ Persist data
- ✅ Scale as needed

**Next:** Share the URL and explain the architecture to interviewers!
