#!/bin/bash

# Budget App Local Startup Script (Without Docker)

echo "🚀 Starting Budget Accounting App (Local Mode)..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Set environment variable for local database
export USE_LOCAL_DB=true
export PYTHONPATH=.

# Initialize database (create tables)
echo "🗄️  Initializing database..."
python3 -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine); print('✅ Database initialized!')"

# Start the application
echo ""
echo "✅ Starting application..."
echo "📱 Access the application at: http://localhost:8000"
echo "🗄️  Using local SQLite database: budget_app.db"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000