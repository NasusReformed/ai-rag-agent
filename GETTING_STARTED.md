# Getting Started

This guide will get you from clone to running instance in under 10 minutes.

## Prerequisites

- Python 3.12
- PostgreSQL database (local or cloud)
- Git

## Local Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set your database connection:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
HF_API_TOKEN=your_huggingface_token
```

Get a free Hugging Face token at https://huggingface.co/settings/tokens

### 3. Initialize Database

```bash
# Using psql
psql $DATABASE_URL < database/schema.sql

# Or import via SQL client (DBeaver, pgAdmin, etc.)
```

This creates tables and enables the pgvector extension for semantic search.

### 4. Start Server

```bash
cd backend
uvicorn app.main:app --reload
```

Server runs at http://localhost:8000

### 5. Test the Dashboard

Open http://localhost:8000 in your browser.

- Click "Load Demo Data" to index sample documents
- Try the chat interface
- Test semantic search
- Execute tools

## Production Deployment

For deploying to the cloud, see:
- [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) - Step-by-step deployment guide
- [docs/PLATFORM_CHOICE.md](docs/PLATFORM_CHOICE.md) - Railway vs other platforms

Quick deployment to Railway:

```bash
railway login
railway link
railway add postgresql
railway variables set HF_API_TOKEN=your_token
railway up
```

Then run `database/schema.sql` in the Railway PostgreSQL console.

## Database Options

### Free Tiers
- **Supabase** - 500MB PostgreSQL with pgvector support
- **Railway** - PostgreSQL included with new projects
- **Neon** - Serverless PostgreSQL

### Local Development
```bash
# macOS
brew install postgresql pgvector

# Ubuntu
sudo apt-get install postgresql postgresql-contrib
```

Enable pgvector extension:
```sql
CREATE EXTENSION vector;
```

## Next Steps

- Review [docs/SYSTEM_OVERVIEW.md](docs/SYSTEM_OVERVIEW.md) for architecture details
- Check `api/requests.http` for example API calls
- Explore the codebase structure in [README.md](README.md)

## Common Issues

**pgvector not found**: Ensure the extension is installed and enabled
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

**HF_API_TOKEN invalid**: Generate a new token at https://huggingface.co/settings/tokens

**Port 8000 in use**: Change port with `--port 8001` flag

**Database connection failed**: Verify DATABASE_URL format and credentials
