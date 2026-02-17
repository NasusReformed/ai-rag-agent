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

Edit `.env` and set your Supabase connection:

```bash
# Get this from Supabase: Settings → Database → Connection String (URI mode)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
HF_API_TOKEN=your_huggingface_token
```

**Getting your Supabase URL:**
1. Go to https://supabase.com/dashboard
2. Select your project (or create one)
3. Navigate to Settings → Database
4. Copy the "Connection string" under "URI"
5. Replace `[YOUR-PASSWORD]` with your database password

**Hugging Face Token:**
Get a free token at https://huggingface.co/settings/tokens

### 3. Initialize Database

**Option A: Supabase SQL Editor (Recommended)**
1. Open your Supabase project
2. Go to SQL Editor
3. Create a new query
4. Paste the contents of `database/schema.sql`
5. Run the query

**Option B: psql command line**
```bash
psql $DATABASE_URL < database/schema.sql
```

The pgvector extension comes pre-installed on Supabase.

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

## Next Steps

### Recommended: Supabase (Free Tier)
- 500MB PostgreSQL database
- pgvector extension pre-installed
- Free tier includes 2 projects
- Web-based SQL editor
- Setup: https://supabase.com/dashboard

### Alternatives
- **Railway** - PostgreSQL addon, $5/month
- **Neon** - Serverless PostgreSQL, generous free tier
- **Local PostgreSQL** - Full control, requires setup

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
