# Database & Hosting Options

## Current Setup

This project uses **Supabase** for PostgreSQL hosting and is designed for **local development**.

### Why Supabase?

| Feature | Supabase | Self-Hosted PostgreSQL |
|---------|----------|------------------------|
| **Setup Time** | 2 minutes | 30+ minutes |
| **pgvector** | Pre-installed | Manual installation |
| **Free Tier** | 500MB storage | Unlimited (if you have hardware) |
| **Web Interface** | SQL Editor, Table Editor | Requires pgAdmin/DBeaver |
| **Backups** | Automatic | Manual setup |
| **Cost** | Free tier sufficient | Hardware/electricity costs |

**Verdict:** Supabase is the best choice for portfolio projects and local development.

---

## Deployment Platform Comparison

If you decide to deploy this project to production, here are the options:

### Railway ⭐ Recommended for Production

**Pros:**
- ✅ ML workloads supported (sufficient RAM for sentence-transformers)
- ✅ Integrated PostgreSQL service
- ✅ Fast deployment (1-2 min)
- ✅ Native Docker support
- ✅ Good developer UX

**Cons:**
- ❌ No free tier (7-day trial, then ~$20/month)
- ❌ Requires credit card

**Best For:** Production deployments, professional projects

---

### Render

**Pros:**
- ✅ True free tier (doesn't expire)
- ✅ Simple setup
- ✅ Auto-scaling on paid plans

**Cons:**
- ❌ **Free tier CANNOT run this project** - insufficient RAM for ML models
- ❌ Spins down after 15min inactivity
- ❌ Requires paid plan ($7+/month) for ML workloads

**Free Tier Test Results:**
- ✅ Frontend works
- ✅ Health check works
- ❌ `/api/embeddings/index` → 502 timeout
- ❌ `/api/agent/chat` → 502 timeout

**Best For:** Non-ML projects, static sites

---

### Fly.io

**Pros:**
- ✅ Generous free tier (3 shared VMs)
- ✅ Works with ML models
- ✅ Global edge deployment

**Cons:**
- ❌ More complex setup (requires Dockerfile customization)
- ❌ Requires credit card verification

**Best For:** Developers comfortable with containerization

---

### Hugging Face Spaces

**Pros:**
- ✅ Free tier specifically designed for ML models
- ✅ GPU support available
- ✅ Easy to showcase ML projects

**Cons:**
- ❌ Requires adapting FastAPI to Gradio interface
- ❌ No PostgreSQL hosting (need external DB)

**Best For:** ML-focused demos without database requirements

---

## Recommendation Summary

**For This Project:**
- **Development:** Local + Supabase (current setup)
- **Portfolio/Resume:** GitHub repository only
- **Live Demo:** Railway ($20/month) or Fly.io (free with credit card)
- **Not Recommended:** Render free tier (insufficient resources)

**Cost Comparison (Monthly):**
| Platform | Database | Backend | Total |
|----------|----------|---------|-------|
| Supabase + Local | Free | $0 | **$0** |
| Railway | Included | $15-20 | **$20** |
| Render | $7 | $7 | **$14** |
| Fly.io | External | Free* | **$0-7** |

*Fly.io free tier requires credit card verification

---

## Why Local Development?

For portfolio projects and job applications:
1. ✅ **Zero cost** - No monthly fees
2. ✅ **Full control** - Debug easily, no deployment delays
3. ✅ **Fast iteration** - Make changes instantly
4. ✅ **GitHub repo is enough** - Employers can run it locally
5. ✅ **No infrastructure management** - Focus on code quality

**Employers care about:**
- Clean code and architecture ✅
- Understanding of RAG systems ✅
- Ability to explain technical decisions ✅
- Working demo they can run ✅

**Employers rarely care about:**
- If it's deployed to production ❌
- Uptime and monitoring ❌
- Custom domain ❌

---

## Migration Guide

If you want to switch from Supabase:

### To Local PostgreSQL
```bash
# Install PostgreSQL + pgvector
brew install postgresql pgvector  # macOS
# or
sudo apt install postgresql postgresql-15-pgvector  # Ubuntu

# Start PostgreSQL
brew services start postgresql

# Create database
createdb ai_rag_agent

# Update .env
DATABASE_URL=postgresql://localhost:5432/ai_rag_agent

# Run schema
psql ai_rag_agent < database/schema.sql
```

### To Railway
```bash
railway login
railway link
railway add postgresql
railway variables set HF_API_TOKEN=your_token
railway variables set DATABASE_URL=${{Postgres.DATABASE_URL}}
railway up
```

### To Neon (Serverless PostgreSQL)
1. Sign up at https://neon.tech
2. Create project with pgvector
3. Copy connection string
4. Update DATABASE_URL in .env
5. Run schema via psql or web console


- Gradio/Streamlit integration
- Perfect for ML demos

**If budget-conscious:**
- ✅ **Run locally** (fully functional, no cost)
- ⚠️ Render Starter Plan ($7/month) - should work for ML
- ❌ **NOT Render Free Tier** - ML endpoints will timeout

---

## Implementation Guide

### Choose Railway

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to https://railway.app
# 3. New Project → Select repo
# 4. Add PostgreSQL
# 5. Done (auto-deploys)
```

### Choose Render

```bash
# 1. Push to GitHub  
git push origin main

# 2. Go to https://render.com/register
# 3. New Web Service → Select repo
# 4. New PostgreSQL
# 5. Done (auto-deploys)
```

---

## Platform-Specific Issues

### Railway
- **Issue**: "ModuleNotFoundError"
  - **Fix**: Check Procfile, Root Directory = backend
  
- **Issue**: "Database connection refused"
  - **Fix**: Missing DATABASE_URL in Variables

### Render
- **Issue**: Service spins down
  - **Fix**: Expected on free tier; paid plan auto-scales
  
- **Issue**: Slow first request
  - **Fix**: Cold start normal; upgrade to remove spinning

---

## Cost Analysis (12 months)

### Railway
```
$20/month (Starter)
= $240/year
+ one-time setup: free
```

### Render
```
Free tier: $0
Starter+ tier: $15/month
= $180/year
+ one-time setup: free
```

**Monthly difference**: Render saves $5-20/month

---

## Migration Path

Both platforms are similar; easy to switch if needed:

1. ✅ Deploy on Platform A (e.g., Railway)
2. ✅ Test in production
3. If issues → Push same code to Platform B (e.g., Render)
4. No code changes needed

---

## My Recommendation by Use Case

| Use Case | Platform |
|----------|----------|
| **Interview demo** | Railway (fast, reliable) |
| **Portfolio site** | Render (cost-effective) |
| **Learning** | Both (try both!) |
| **Production app** | Railway (better SLA) |
| **Side project** | Render (free tier) |

---

## Decision Paralysis? 

**Pick Railway** if unsure. It's slightly more expensive but:
- ✅ Faster (good for interviews)
- ✅ Better UX (easier to debug live)
- ✅ No cold starts
- ✅ Modern platform

Spend $20 upfront, get fast deployment, impress interviewers.

---

## Next Steps

1. Choose platform ↑
2. Follow [RAILWAY_SETUP.md](RAILWAY_SETUP.md) or [RENDER_SETUP.md](RENDER_SETUP.md)
3. Push code to GitHub
4. Deploy
5. Test dashboard

Questions? See [DEPLOYMENT.md](DEPLOYMENT.md)
