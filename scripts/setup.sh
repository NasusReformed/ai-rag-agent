#!/bin/bash

echo "🚀 AI Agent RAG System - Setup Script"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r backend/requirements.txt

# Setup .env
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp config/.env.example .env
    echo "⚠️  Edit .env with your Supabase connection string"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env with your Supabase DB URL"
echo "2. Run migrations: psql -f database/schema.sql"
echo "3. Start server: cd backend && uvicorn app.main:app --reload"
echo "4. Open http://localhost:8000 in your browser"
