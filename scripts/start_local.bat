@echo off
REM Budget App Local Startup Script (Without Docker) - Windows

echo Starting Budget Accounting App (Local Mode)...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet


REM Set environment variable for local database
set USE_LOCAL_DB=true
set PYTHONPATH=.

REM Initialize database (create tables)
echo Initializing database...
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine); print('Database initialized!')"

REM Start the application
echo.
echo Starting application...
echo Access the application at: http://localhost:8000
echo Using local SQLite database: budget_app.db
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000