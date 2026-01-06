# Quick Start Guide - Budget Accounting App

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Application

**Option A: Local SQLite (No Docker - Easiest!)**
```bash
cd budget_app

# Linux/Mac
./scripts/start_local.sh

# Windows
scripts\start_local.bat
```

**Option B: Using the startup script with Docker**
```bash
cd budget_app
./scripts/start.sh
```

**Option C: Using Docker Compose directly**
```bash
cd budget_app
docker-compose up --build
```

**Option D: Pure Python (Manual)**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac: venv\Scripts\activate.bat for Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export USE_LOCAL_DB=true  # set USE_LOCAL_DB=true for Windows

# Run the app
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

### Step 3: Start Tracking Your Budget!

Your app comes with a default "Main Wallet" ready to use.

---

## 📖 Common Tasks

### Creating a New Wallet

1. Click the **☰ menu icon** (top-left)
2. Click **"+ Add Wallet"**
3. Fill in:
   - **Name**: My Savings
   - **Type**: Deposit
   - **Interest Rate**: 5.0 (for deposits only)
   - **Description**: Emergency fund
4. Click **"Create Wallet"**

### Recording Income

1. Click the **green + button** (bottom-left)
2. Enter:
   - **Amount**: 150000
   - **Category**: Salary
   - **Description**: Monthly salary
3. Click **"Add"**

### Recording an Expense

1. Click the **red − button** (bottom-right)
2. Enter:
   - **Amount**: 5000
   - **Category**: Food
   - **Description**: Groceries
3. Click **"Withdraw"**

### Transferring Between Wallets

1. Click the **red − button** (bottom-right)
2. Check **"Transfer to another wallet"**
3. Select target wallet
4. Enter amount and details
5. Click **"Transfer"**

### Filtering Your Operations

**By Period:**
- Select from: Today, This Week, This Month, This Year, or Custom Range

**By Category:**
- Choose any category to see only those transactions

---

## 💡 Pro Tips

### Deposit Wallets
- Automatically accumulate interest based on the annual rate you set
- Interest is calculated daily using compound interest formula
- Check your balance regularly to see it grow!

### Categories
Choose the right category for better insights:
- **Salary** - Regular income
- **Food** - Groceries and daily food
- **Healthcare** - Medical expenses
- **Home** - Rent, utilities, maintenance
- **Education** - Courses, books, tuition
- **Subscriptions** - Streaming, software, memberships
- **Entertainment** - Movies, games, hobbies
- **Restaurants** - Dining out
- **Transport** - Gas, public transport, car
- **Shopping** - Clothes, electronics, misc
- **Other** - Anything else

### Best Practices
1. **Record transactions immediately** - Don't wait until the end of the day
2. **Use descriptive notes** - Future you will appreciate it
3. **Check your summary regularly** - Stay aware of your spending patterns
4. **Set up multiple wallets** - Separate savings, daily expenses, investments
5. **Review category breakdown** - Identify areas to reduce spending

---

## 🔧 Troubleshooting

### Application won't start
```bash
# Check if ports are available
lsof -i :8000
lsof -i :5432

# Stop and restart
docker-compose down
docker-compose up --build
```

### Database issues
```bash
# Reset database (⚠️ WARNING: Deletes all data)
docker-compose down -v
docker-compose up --build
```

### Can't see my operations
- Check that you're viewing the correct wallet (top selector)
- Verify your date filter isn't too restrictive
- Make sure you've created at least one operation

---

## 🎯 Example Workflow

### Setting up your first month:

1. **Create wallets:**
   - Main Wallet (Simple) - for daily expenses
   - Savings (Deposit, 5% interest) - for emergency fund
   - Investment (Stock) - for long-term investments

2. **Record your income:**
   - Add salary to Main Wallet
   - Transfer 20% to Savings
   - Transfer 10% to Investment

3. **Track your expenses:**
   - Record all daily expenses in Main Wallet
   - Use appropriate categories
   - Add descriptions for important purchases

4. **Review at month end:**
   - Check category breakdown
   - See where money went
   - Adjust next month's budget

---

## 📊 Understanding Your Dashboard

### Balance Card (Center Top)
- Shows current balance of selected wallet
- Updates in real-time

### Summary Stats
- **Income**: Total additions in selected period
- **Expenses**: Total withdrawals/transfers in selected period

### Category Breakdown
- Visual breakdown of spending by category
- Shows transaction count per category
- Sorted by amount (highest first)

### Operations List
- All transactions grouped by date
- Shows: amount, category, time, description
- Click **×** to delete an operation

---

## 🛠️ Advanced Features

### Custom Date Ranges
1. Select **"Custom Range"** from period filter
2. Set start and end dates
3. View operations for that specific period

### Interest Calculation (Deposits)
- Formula: `New Balance = Old Balance × (1 + daily_rate)^days`
- Daily rate = `Annual Rate / 365 / 100`
- Applied automatically when viewing wallet

### Transfer Operations
- Deducts from source wallet
- Adds to target wallet
- Both wallets updated simultaneously
- Cannot transfer to same wallet

---

## 📱 Keyboard Shortcuts (Coming Soon)

- `Ctrl/Cmd + N` - New operation
- `Ctrl/Cmd + W` - New wallet
- `Ctrl/Cmd + F` - Focus filter
- `Esc` - Close modal/menu

---

## 🆘 Getting Help

### View Application Logs
```bash
docker-compose logs -f app
```

### View Database Logs
```bash
docker-compose logs -f postgres
```

### Access Database Directly
```bash
docker exec -it budget_postgres psql -U budget_user -d budget_db
```

### Stop Application
```bash
docker-compose down
```

### Stop and Remove All Data
```bash
docker-compose down -v
```

---

## 🎨 Customization

### Change Colors
Edit `app/static/css/style.css` and modify CSS variables:
```css
:root {
    --primary: #2C5F2D;      /* Main color */
    --secondary: #FF6B35;    /* Accent color */
    --success: #00B894;      /* Success/Income */
    --danger: #FF6B6B;       /* Danger/Expense */
}
```

### Add New Categories
1. Edit `app/models/models.py` - add to `Category` enum
2. Edit `app/templates/base.html` - add to category select
3. Edit `app/templates/index.html` - add to category filter
4. Restart application

---

## 📈 Next Steps

Once comfortable with basics:
1. Set monthly budget goals
2. Track spending trends
3. Optimize savings rate
4. Plan for major purchases
5. Build emergency fund

---

## 💬 Feedback

Enjoying the app? Have suggestions? The profile page is a placeholder for future enhancements including:
- User authentication
- Multi-currency support
- Budget goals and alerts
- Export functionality
- Mobile app version

---

**Happy Budgeting! 💰**