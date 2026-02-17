# Render Deployment - Step by Step

## Prerequisites

- GitHub account: https://github.com  
- Render account: https://render.com
- Code pushed to GitHub repo

## Step 1: Connect GitHub to Render

1. Go to https://render.com/register
2. Click "Sign up with GitHub"
3. Authorize Render
4. Verify email

## Step 2: Create PostgreSQL Database

1. Dashboard → "New+"
2. Select "PostgreSQL"
3. Name: `ai-agent-db`
4. Plan: Free tier (or Starter $9/month)
5. Click "Create Database"
6. Copy connection string (save it)

## Step 3: Deploy Backend

1. Dashboard → "+ New"
2. Select "Web Service"
3. Connect your GitHub repo
4. Settings:
   ```
   Name: ai-agent-api
   Environment: Python 3.12
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

## Step 4: Add Environment Variables

In the service settings, under "Environment":

```
SUPABASE_DB_URL=<PostgreSQL connection string from Step 2>
LLM_PROVIDER=hf
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.1
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_TOP_K=4
APP_ENV=production
PYTHONUNBUFFERED=true
```

## Step 5: Deploy

1. Click "Create Web Service"
2. Watch build logs
3. Deployment takes 2-3 minutes
4. Get URL: `your-service.onrender.com`

## Step 6: Initialize Database Schema

1. Get PostgreSQL connection: Render Dashboard → Database → "Info"
2. Use CLI or web client:
   ```bash
   psql <connection-string>
   ```
3. Copy-paste [database/schema.sql](database/schema.sql)
4. Run

Or from Render shell (if available):
```bash
psql $SUPABASE_DB_URL < database/schema.sql
```

## Step 7: Test

```bash
curl https://your-service.onrender.com/api/health
# Returns: {"status": "ok"}
```

Dashboard:
```
https://your-service.onrender.com
```

## Troubleshooting

### Build fails

Check logs: Service → Logs

**"psycopg" error** → Wrong Python version (needs 3.12)  
**"Module not found"** → Missing from requirements.txt

### Works locally, fails on Render

Check `/logs/build.log` for:
- Missing dependencies
- Wrong database URL
- Module import errors

### Database not connected

1. Verify `SUPABASE_DB_URL` in Environment
2. Test locally: `psql $SUPABASE_DB_URL`
3. Redeploy after fixing

## Auto-Deploy

Every push to `main` branch triggers deployment:
1. GitHub → Render webhook
2. Render pulls latest code
3. Runs build command
4. Redeploys service (0 downtime)

To disable:
- Service → Settings → Auto-deploy: OFF

## Scaling

Free tier limits:
- 0.5 CPU / 512MB RAM
- Spinning down after 15min inactivity
- No persistent storage

To upgrade:
1. Service → Settings
2. Instance Type → Starter/Pro
3. Paid plan from $15/month

## Cost Breakdown

| Component | Price |
|-----------|-------|
| PostgreSQL | $7/month (free tier) |
| API Server | $7/month (free tier) |
| **Total** | $14/month |

Free tier: 50 requests/day max

## Monitoring

1. **Logs**: Service → Logs
2. **Metrics**: Service → Metrics
3. **Database**: Database → Logs
4. Health check: API → /api/health endpoint

## Advanced: Custom Domain

1. Service → Settings
2. Custom Domain
3. Point your domain DNS to Render
4. SSL auto-provisioned

## Next Steps

1. ✅ API deployed  
2. ✅ Database created
3. Schema initialized
4. Test Dashboard
5. Monitor logs
6. Scale as needed
