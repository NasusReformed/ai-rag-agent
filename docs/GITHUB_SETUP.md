# GitHub Setup & First Push

## Prerequisites

1. **Git installed**: https://git-scm.com/download/win (Windows) or https://git-scm.com (Mac/Linux)
2. **GitHub account**: https://github.com/signup
3. **Code ready**: All project files in your local directory

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Enter:
   ```
   Repository name: portfolio-ai-agent
   (or any name you prefer)
   ```
3. Add description:
   ```
   AI Agent RAG System - Production-ready portfolio project
   ```
4. Choose **Public** (so others can see it)
5. Skip "Initialize with README" (we already have one)
6. Click **"Create repository"**

## Step 2: Initialize Git Locally

Open **Terminal/PowerShell** in your project directory:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Agent RAG System with FastAPI, PostgreSQL, and web dashboard"
```

## Step 3: Set Remote & Push

Replace `YOUR-USERNAME` and `portfolio-ai-agent` with your actual values:

```bash
# Add remote
git remote add origin https://github.com/YOUR-USERNAME/portfolio-ai-agent.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify on GitHub

1. Go to https://github.com/YOUR-USERNAME/portfolio-ai-agent
2. You should see all your files
3. Go to the repository settings (⚙️ icon)
4. Under "Code and automation" → "Pages"
5. Source → select `main` branch
6. Save

## Step 5: Connect to Railway or Render

### If using Railway:
1. Go to https://railway.app
2. Login with GitHub
3. New Project
4. Search for `portfolio-ai-agent`
5. Select it
6. Continue following [RAILWAY_SETUP.md](RAILWAY_SETUP.md)

### If using Render:
1. Go to https://render.com
2. Login with GitHub
3. New Web Service
4. Connect GitHub → select repo
5. Continue following [RENDER_SETUP.md](RENDER_SETUP.md)

## Troubleshooting

### "fatal: not a git repository"
```powershell
git init  # Run this first
```

### "Permission denied (publickey)"
Setup SSH key:
```powershell
# Generate key (press Enter 3x)
ssh-keygen -t ed25519

# Copy key to GitHub
type $env:USERPROFILE\.ssh\id_ed25519.pub
# Paste in GitHub Settings → SSH Keys
```

Or use HTTPS instead (password-based):
```powershell
git remote set-url origin https://github.com/YOUR-USERNAME/portfolio-ai-agent.git
```

### "branch 'main' set up to track 'origin/main'"
This is normal - just means your local is synced with remote.

### "Everything up-to-date"
Good! Your code is on GitHub.

## Next Steps

1. ✅ Code on GitHub
2. ⏭️ Deploy to Railway/Render (see RAILWAY_SETUP.md or RENDER_SETUP.md)
3. ⏭️ Test deployed API
4. ⏭️ Share URL: `https://your-app.onrender.com` or `https://your-app.railway.app`

## Useful Git Commands

```powershell
# See status
git status

# Check committed files
git log --oneline

# Make changes and push
git add .
git commit -m "Description of changes"
git push

# Test locally before pushing
git diff
```

## File Structure on GitHub

Your repo will look like:

```
portfolio-ai-agent/
  ├── README.md
  ├── DEPLOYMENT.md
  ├── RAILWAY_SETUP.md
  ├── RENDER_SETUP.md
  ├── PLATFORM_CHOICE.md
  ├── Procfile
  ├── Dockerfile
  ├── docker-compose.yml
  ├── requirements.txt
  ├── .env.example
  ├── .gitignore
  ├── backend/
  │   ├── requirements.txt
  │   └── app/
  │       ├── main.py
  │       ├── api/
  │       ├── agent/
  │       ├── rag/
  │       ├── tools/
  │       ├── embeddings/
  │       ├── core/
  │       └── static/
  └── database/
      └── schema.sql
```

Ready? Follow [RAILWAY_SETUP.md](RAILWAY_SETUP.md) or [RENDER_SETUP.md](RENDER_SETUP.md) next!
