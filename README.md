# Budget Accounting App

A simple and elegant budget accounting web application built with FastAPI, PostgreSQL, and Jinja2 templates.

## Features

### Wallet Management
- **Multiple Wallet Types**: Create Simple Wallets, Deposits (with automatic interest accumulation), and Stock Wallets
- **Flexible Configuration**: Set custom names, descriptions, and parameters for each wallet
- **Automatic Interest**: Deposit wallets automatically accumulate value based on their effective percentage

### Operations
- **Add Money**: Record income transactions with categories
- **Withdraw Money**: Track expenses across different categories
- **Transfer Between Wallets**: Move money between your wallets
- **Comprehensive Categorization**: 
  - Healthcare
  - Food
  - Home
  - Education
  - Subscriptions
  - Entertainment
  - Restaurants
  - Transport
  - Shopping
  - Salary
  - Other

### Filtering & Analysis
- **Period Filters**: View operations by Today, This Week, This Month, This Year, or Custom Range
- **Category Filters**: Focus on specific spending categories
- **Category Breakdown**: See total spending by category
- **Summary Statistics**: Track total income, expenses, and net change

### User Interface
- **Modern Design**: Clean, intuitive interface with smooth animations
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Side Menu**: Easy access to all wallets
- **Floating Action Buttons**: Quick add/withdraw operations
- **Date Grouping**: Operations organized by date for easy tracking

## Technology Stack

- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 16 (Docker)
- **Frontend**: Jinja2 Templates, Vanilla JavaScript
- **Validation**: Pydantic
- **Styling**: Custom CSS with modern design principles
- **Containerization**: Docker & Docker Compose

## Project Structure

```
budget_app/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── wallets.py          # Wallet API endpoints
│   │   └── operations.py       # Operation API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic schemas
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Application styles
│   │   └── js/
│   │       └── app.js          # Frontend logic
│   ├── templates/
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Main dashboard
│   │   └── profile.html        # Profile page (placeholder)
│   ├── database.py             # Database configuration
│   └── main.py                 # FastAPI application
├── scripts/
├── .env                        # Environment variables
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites
- Python 3.10+ (required for local mode)
- Docker and Docker Compose (only if using Docker mode)

### Quick Start with Local SQLite Database (Recommended for Development)

1. **Clone or navigate to the project directory**:
   ```bash
   cd budget_app
   ```

2. **Run the local startup script**:
   
   **On Linux/Mac**:
   ```bash
   ./scripts/start_local.sh
   ```
   
   **On Windows**:
   ```bash
   scripts\start_local.bat
   ```

3. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

The local mode uses SQLite database (`budget_app.db`) which doesn't require Docker or PostgreSQL installation.

### Quick Start with Docker (For Production)

1. **Clone or navigate to the project directory**:
   ```bash
   cd budget_app
   ```

2. **Update .env to use PostgreSQL**:
   ```bash
   # Change USE_LOCAL_DB to false
   USE_LOCAL_DB=false
   ```

3. **Start the application**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

### Local Development Setup

**Option A: Local SQLite (No Docker Required)**
```bash
# Run the local startup script
./scripts/start_local.sh  # Linux/Mac
# OR
scripts\start_local.bat   # Windows
```

The script will:
- Create a virtual environment
- Install all dependencies
- Initialize the SQLite database
- Start the application on http://localhost:8000

**Option B: Manual Local Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export USE_LOCAL_DB=true  # Linux/Mac
# OR
set USE_LOCAL_DB=true     # Windows

# Run the app
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: Docker with PostgreSQL**

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL**:
   ```bash
   docker-compose up postgres -d
   ```

3. **Update .env file** if needed:
   ```
   DATABASE_URL=postgresql://budget_user:budget_password@localhost:5432/budget_db
   SECRET_KEY=your-secret-key-change-this-in-production
   DEBUG=True
   ```

4. **Run the application**:
   ```bash
   cd app
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Wallets
- `POST /api/wallets/` - Create a new wallet
- `GET /api/wallets/` - Get all wallets
- `GET /api/wallets/{wallet_id}` - Get wallet by ID
- `PUT /api/wallets/{wallet_id}` - Update wallet
- `DELETE /api/wallets/{wallet_id}` - Delete wallet

### Operations
- `POST /api/operations/` - Create a new operation
- `GET /api/operations/` - Get operations (with filters)
- `GET /api/operations/summary` - Get operations summary
- `GET /api/operations/{operation_id}` - Get operation by ID
- `DELETE /api/operations/{operation_id}` - Delete operation

### Query Parameters for Filtering
- `wallet_id`: Filter by wallet
- `start_date`: Start date (ISO 8601)
- `end_date`: End date (ISO 8601)
- `category`: Filter by category
- `operation_type`: Filter by operation type

## Usage Guide

### Creating Your First Wallet

1. Click the hamburger menu (☰) in the top-left corner
2. Click "+ Add Wallet"
3. Fill in the details:
   - **Name**: e.g., "Main Wallet"
   - **Type**: Choose from Simple, Deposit, or Stock
   - **Description**: Optional
   - **Interest Rate**: Required for Deposit wallets (annual percentage)
4. Click "Create Wallet"

### Adding Money (Income)

1. Click the green "+" button in the bottom-left corner
2. Fill in:
   - **Amount**: Enter the amount in KZT
   - **Category**: Choose appropriate category (e.g., Salary)
   - **Date & Time**: Defaults to current time
   - **Description**: Optional notes
3. Click "Add"

### Withdrawing Money (Expense)

1. Click the red "−" button in the bottom-right corner
2. Fill in the operation details
3. Optionally check "Transfer to another wallet" to move money between wallets
4. Click "Withdraw" or "Transfer"

### Filtering Operations

Use the filter dropdowns at the top of the dashboard:
- **Period**: Select time range
- **Category**: Filter by spending category

### Viewing Analytics

- **Balance Card**: Shows current wallet balance
- **Summary Stats**: Displays income and expenses for the selected period
- **Category Breakdown**: Shows spending by category
- **Operations List**: Detailed list of all transactions, grouped by date

## Database Schema

### Wallets Table
- `id`: Primary key
- `name`: Wallet name
- `wallet_type`: Type (simple/deposit/stock)
- `description`: Optional description
- `balance`: Current balance
- `interest_rate`: Annual interest rate (for deposits)
- `last_interest_applied`: Last interest calculation date
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Operations Table
- `id`: Primary key
- `wallet_id`: Foreign key to wallets
- `operation_type`: Type (addition/withdrawal/transfer)
- `amount`: Transaction amount
- `category`: Transaction category
- `description`: Optional notes
- `operation_time`: Transaction timestamp
- `target_wallet_id`: Foreign key for transfers
- `created_at`: Creation timestamp

## Security Features

- **Input Validation**: Pydantic schemas validate all inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Balance Validation**: Prevents withdrawals exceeding balance
- **Type Safety**: Strong typing with Pydantic models
- **Transaction Integrity**: Proper database transactions

## Future Enhancements

- User authentication and authorization
- Multi-user support
- Data export (CSV, PDF)
- Budget planning and goals
- Recurring transactions
- Charts and visualizations
- Mobile app (Flutter)
- Notifications and reminders
- Currency conversion
- Receipt attachment

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Port Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Clear Database
```bash
# Stop containers and remove volumes
docker-compose down -v

# Restart
docker-compose up --build
```

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Style
The project follows PEP 8 guidelines. Use `black` for formatting:
```bash
pip install black
black app/
```

## License

This project is provided as-is for educational and personal use.

## Support

For issues, questions, or contributions, please refer to the project documentation or create an issue in the repository.

## Acknowledgments

Built with:
- FastAPI - Modern, fast web framework
- PostgreSQL - Robust relational database
- Jinja2 - Powerful templating engine
- Docker - Containerization platform