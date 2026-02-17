@echo off
echo 🚀 AI Agent RAG System - Setup Script
echo =====================================

REM Check Python version
python --version
if errorlevel 1 (
    echo ❌ Python not found. Install Python 3.12+
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r backend\requirements.txt

REM Setup .env
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy config\.env.example .env
    echo ⚠️  Edit .env with your Supabase connection string
)

echo.
echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Edit .env with your Supabase DB URL
echo 2. Run migrations in Supabase: database/schema.sql
echo 3. Start server: cd backend ^&^& uvicorn app.main:app --reload
echo 4. Open http://localhost:8000 in your browser
pause
