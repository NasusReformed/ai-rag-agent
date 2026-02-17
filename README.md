# AI RAG Agent

Production-ready conversational AI with semantic search and tool execution capabilities.

## Overview

This system combines retrieval-augmented generation (RAG) with agentic tool calling to create an intelligent assistant that can search knowledge bases, execute business logic, and maintain conversation context.

**Tech Stack:** FastAPI, PostgreSQL (pgvector), sentence-transformers, Hugging Face Inference API

## Features

- Semantic search across document collections using vector embeddings
- Tool registry with 5 built-in operations (CRM, search, calculations)
- Persistent conversation sessions with full message history
- Web-based dashboard for chat, document management, and tool execution
- RESTful API with comprehensive endpoint coverage

## Architecture

```
Frontend (Static)
    ↓
FastAPI Backend
    ├── Agent Service (RAG + Tools)
    ├── Embedding Service (sentence-transformers)
    ├── Tool Registry
    └── Session Manager
    ↓
PostgreSQL + pgvector
```

## Quick Start

### Local Development

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Configure database
cp .env.example .env
# Set DATABASE_URL to your Supabase PostgreSQL instance

# Initialize schema
psql $DATABASE_URL < database/schema.sql

# Run server
cd backend
uvicorn app.main:app --reload
```

Visit http://localhost:8000 to access the dashboard.

### Database Setup (Supabase)

1. Create a project at https://supabase.com
2. Get your PostgreSQL connection string from Settings → Database
3. Run the schema:
   - Option A: Use Supabase SQL Editor and paste `database/schema.sql`
   - Option B: Connect via `psql` using the connection string
4. The pgvector extension is pre-installed on Supabase

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions.

## Project Structure

```
backend/
├── app/
│   ├── agent/          # AI agent logic
│   ├── api/            # REST endpoints
│   ├── embeddings/     # Vector encoding
│   ├── rag/            # Retrieval system
│   ├── tools/          # Tool implementations
│   ├── core/           # Config & database
│   ├── static/         # Web dashboard
│   └── main.py
├── requirements.txt
└── .env.example

database/
├── schema.sql          # PostgreSQL + pgvector setup
└── seed.sql            # Demo data

docs/
├── DEPLOYMENT_GUIDE.md
├── PLATFORM_CHOICE.md
└── SYSTEM_OVERVIEW.md

api/
└── requests.http      # Example HTTP requests
```

## API Endpoints

- `POST /api/agent/chat` - Send message to agent
- `POST /api/embeddings/index` - Index documents
- `GET /api/embeddings/search` - Semantic search
- `POST /api/tools/execute` - Execute tool directly
- `GET /api/health` - Health check

See `api/requests.http` for example requests.

## Environment Variables

Required configuration in `.env`:

```bash
# Supabase PostgreSQL connection
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Hugging Face API token (free at https://huggingface.co/settings/tokens)
HF_API_TOKEN=hf_...
HF_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Development

The codebase follows standard Python conventions:
- Type hints throughout
- Async/await for I/O operations
- Connection pooling for database
- Environment-based configuration

Testing locally requires PostgreSQL with pgvector extension.

## License

MIT
