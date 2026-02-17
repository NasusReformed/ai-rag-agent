# Railway Deployment - Step by Step

## Prerequisites

- GitHub account: https://github.com
- Railway account: https://railway.app
- Code pushed to GitHub repo

## Step 1: Sign in to Railway

1. Go to https://railway.app
2. Click "Start Now" or sign in with GitHub
3. Authorize Railway to access your GitHub account

## Step 2: Create New Project

1. Click "+ New Project" in top-right
2. Select "Deploy from GitHub repo" → "Configure GitHub App"
3. Choose your repository (e.g., `portfolio-ai-agent`)

## Step 3: Add PostgreSQL Database

1. In Railway project, click "+ Add"
2. Select "PostgreSQL"
3. A new service appears - click on it
4. Go to "Variables" tab
5. Copy the `DATABASE_URL`

## Step 4: Configure Backend Service

Railway auto-detects `Procfile`, so it will:
- Read `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Install from `backend/requirements.txt`
- Start the server

To verify/edit:
1. Click on the service name
2. Go to "Settings" tab
3. Verify "Root Directory" is `backend` (Railway usually detects this)

## Step 5: Set Environment Variables

1. In the service, go to "Variables" tab
2. Add these variables:

```
SUPABASE_DB_URL=<DATABASE_URL from PostgreSQL service>
LLM_PROVIDER=hf
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.1
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_TOP_K=4
APP_ENV=production
PYTHONUNBUFFERED=true
```

Or if using Railway's PostgreSQL:
```
DATABASE_URL=<Railway PostgreSQL connection string>
```

(Same as SUPABASE_DB_URL)

## Step 6: Deploy

1. Go back to "Deployments"
2. Click latest deployment
3. Watch build logs

If there are errors:
- Click "View logs" to see what went wrong
- Common issue: Missing DATABASE_URL variable
- Fix: Add it to Variables and redeploy

## Step 7: Initialize Database Schema

Once API is running:

1. Go to "Variables" on PostgreSQL service
2. Copy `DATABASE_URL`
3. Connect with any PostgreSQL client:
   ```bash
   psql "postgres://..."
   ```
4. Paste the content of [database/schema.sql](database/schema.sql)
5. Run the SQL

Or use Railway terminal:
```bash
railway run psql "$(railway variable get DATABASE_URL)" < database/schema.sql
```

## Step 8: Test Deployment

```bash
curl https://<your-railway-url>.up.railway.app/api/health
# Should return: {"status": "ok"}
```

Access Dashboard:
```
https://<your-railway-url>.up.railway.app
```

## Troubleshooting

### Build fails

Check logs:
```
Service → Deployments → Latest → View logs
```

**"ModuleNotFoundError"** → Missing in requirements.txt  
**"No module named app"** → Root Directory issue (should be `backend`)

### Database connection fails

```
SUPABASE_DB_URL invalid or not set
```

Solution:
1. Verify variable exists in Variables tab
2. Test connection: `psql "your-db-url"`
3. Redeploy after fixing

### Deployed but no data

1. Schema not applied → Run schema.sql (see Step 7)
2. Documents not indexed → Use Dashboard to add docs
3. API not responding → Check logs (Service → Deployments)

## Monitoring

Once deployed:

1. **Logs**: Service → Deployments → View logs
2. **Variables**: Service → Variables (edit env vars)
3. **Status**: Dashboard (bottom-left API status indicator)
4. **Metrics**: Service → Metrics (coming soon on Railway)

## Scaling

To increase server size:
1. Service → Settings
2. "Instance Type" → Choose larger
3. Auto-redeploy

Default (free tier): 1 shared CPU, 512MB RAM  
Recommended: 2 CPU, 1GB RAM (~$15/month)

## Next Steps

1. ✅ API deployed
2. ✅ Database ready
3. Push a code change to trigger auto-deploy
4. Test n8n webhook: `POST /api/automation/n8n/webhook`
5. Monitor logs for issues
