# Local Setup Guide - Budget Accounting App

This guide helps you run the Budget Accounting App **without Docker** using a local SQLite database.

## Why Use Local SQLite?

- ✅ **No Docker required** - Works on any system with Python
- ✅ **Instant setup** - No database server installation needed
- ✅ **Perfect for development** - Fast and lightweight
- ✅ **Easy to backup** - Just copy the `budget_app.db` file
- ✅ **Cross-platform** - Works on Windows, Mac, and Linux

## Prerequisites

### Required
- **Python 3.10 or higher**
  - Check version: `python3 --version` or `python --version`
  - Download from: https://www.python.org/downloads/

### Optional (but recommended)
- **pip** (usually comes with Python)
  - Check version: `pip3 --version` or `pip --version`

## Quick Start (Automated)

### On Linux/Mac

```bash
cd budget_app
./scripts/start_local.sh
```

### On Windows

```bash
cd budget_app
scripts\start_local.bat
```

That's it! The script will:
1. Create a virtual environment
2. Install all dependencies
3. Initialize the SQLite database
4. Start the application

## Manual Setup (Step by Step)

If you prefer to set up manually or the automated script doesn't work:

### 1. Navigate to Project Directory

```bash
cd budget_app
```

### 2. Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
```

**Windows:**
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Jinja2
- And other required packages

### 5. Set Environment Variable (Optional)

The app will use SQLite by default, but you can explicitly set it:

**Linux/Mac:**
```bash
export USE_LOCAL_DB=true
```

**Windows (Command Prompt):**
```bash
set USE_LOCAL_DB=true
```

**Windows (PowerShell):**
```bash
$env:USE_LOCAL_DB="true"
```

Or edit the `.env` file and ensure:
```
USE_LOCAL_DB=true
```

### 6. Initialize Database

The database will be created automatically when you start the app, but you can initialize it manually:

```bash
python3 -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

This creates `budget_app.db` in the project root.

### 7. Start the Application

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or from the project root:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Access the Application

Open your browser and go to:
```
http://localhost:8000
```

## Verifying Your Setup

After starting the app, you should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

And in your project directory, you should see:
```
budget_app.db  (SQLite database file)
```

## Switching Between SQLite and PostgreSQL

### Use SQLite (Local)
Edit `.env`:
```
USE_LOCAL_DB=true
```

### Use PostgreSQL (Docker)
Edit `.env`:
```
USE_LOCAL_DB=false
DATABASE_URL=postgresql://budget_user:budget_password@localhost:5432/budget_db
```

Then start PostgreSQL:
```bash
docker-compose up postgres -d
```

## Database Location

- **SQLite**: `budget_app.db` in the project root
- **PostgreSQL**: Docker container volume

## Backup Your Data

### SQLite
Simply copy the database file:
```bash
cp budget_app.db budget_app_backup_$(date +%Y%m%d).db
```

### Restore from Backup
```bash
cp budget_app_backup_20240105.db budget_app.db
```

## Troubleshooting

### "python3: command not found"

Try using `python` instead:
```bash
python --version
python -m venv venv
```

### "No module named 'app'"

Make sure you're in the correct directory:
```bash
# Should be in the project root
pwd  # or cd on Windows
ls   # Should see: app/ scripts/ requirements.txt etc.
```

### "Address already in use"

Port 8000 is already taken. Either:
1. Stop the other application using port 8000
2. Use a different port:
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### Permission Denied (Linux/Mac)

Make the script executable:
```bash
chmod +x scripts/start_local.sh
```

### Virtual Environment Issues

Delete and recreate:
```bash
rm -rf venv  # or rmdir /s venv on Windows
python3 -m venv venv
```

### Database Locked Error

SQLite is being accessed by another process. Close all instances of the app.

### "ModuleNotFoundError: No module named 'fastapi'"

Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Development Tips

### Auto-reload is Enabled

The `--reload` flag means the server will automatically restart when you edit Python files.

### View Database Contents

You can view the SQLite database using:

**Command Line:**
```bash
sqlite3 budget_app.db
.tables
SELECT * FROM wallets;
.quit
```

**GUI Tools:**
- DB Browser for SQLite: https://sqlitebrowser.org/
- DBeaver: https://dbeaver.io/
- DataGrip: https://www.jetbrains.com/datagrip/

### Clear Database

To start fresh:
```bash
rm budget_app.db
# Restart the app - it will create a new database
```

### Check Logs

The terminal where you ran `uvicorn` shows all logs in real-time.

## Performance Notes

SQLite is:
- ✅ Perfect for development and personal use
- ✅ Fast for read operations
- ✅ Handles thousands of operations easily
- ⚠️ Single-writer (but fine for single-user app)
- ⚠️ Not recommended for high-concurrency production

For production with multiple users, use PostgreSQL with Docker.

## Next Steps

Once your app is running:
1. Open http://localhost:8000
2. Create your first wallet (default "Main Wallet" is created automatically)
3. Add your first operation
4. Explore the features!

See [QUICKSTART.md](QUICKSTART.md) for usage guide.

## Stopping the Application

Press `Ctrl+C` in the terminal where the app is running.

To deactivate the virtual environment:
```bash
deactivate
```

## FAQ

**Q: Do I need to keep the terminal open?**
A: Yes, the application runs in the terminal. Closing it stops the server.

**Q: Can I access from another device?**
A: Yes! Use your computer's IP address: `http://YOUR_IP:8000`

**Q: Is my data safe?**
A: Yes! It's stored locally in `budget_app.db`. Make regular backups.

**Q: Can I use this on a server?**
A: For production, use PostgreSQL with Docker for better performance and reliability.

**Q: How do I update the app?**
A: Pull new code, activate venv, and run `pip install -r requirements.txt --upgrade`

---

**Enjoy your Budget Accounting App! 💰**