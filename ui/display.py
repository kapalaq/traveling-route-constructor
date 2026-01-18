"""Display utilities for the budget planner."""
from typing import List, Dict
from models.transaction import Transaction
from wallet.wallet import Wallet
from strategies.sorting import SortingContext


class Display:
    """Handles all display/output operations."""
    
    SEPARATOR = "=" * 50
    
    @staticmethod
    def clear_screen():
        """Print some newlines to simulate clearing."""
        print("\n" * 2)
    
    @staticmethod
    def show_header(text: str):
        """Display a header."""
        print(f"\n{Display.SEPARATOR}")
        print(f"  {text}")
        print(Display.SEPARATOR)
    
    @staticmethod
    def show_balance(wallet: Wallet):
        """Display the total balance."""
        balance = wallet.balance
        sign = "+" if balance >= 0 else ""
        print(f"\n💰 Total Balance: {sign}{balance:.2f}")
    
    @staticmethod
    def show_category_breakdown(wallet: Wallet):
        """Display category contributions."""
        totals = wallet.get_category_totals()
        percentages = wallet.get_category_percentages()
        
        if not totals:
            print("\n📊 No transactions yet")
            return
        
        print("\n📊 Category Breakdown:")
        for category, total in sorted(totals.items()):
            pct = percentages.get(category, 0)
            sign = "+" if total >= 0 else ""
            print(f"   {category}: {sign}{total:.2f} ({pct:.1f}%)")
    
    @staticmethod
    def show_transactions(wallet: Wallet):
        """Display all transactions in sorted order."""
        transactions = wallet.get_sorted_transactions()
        strategy_name = wallet.sorting_context.current_strategy.name
        
        print(f"\n📋 Transactions (Sorted by: {strategy_name}):")
        
        if not transactions:
            print("   No transactions")
            return
        
        for i, t in enumerate(transactions, 1):
            print(f"   {i}. {t}")
    
    @staticmethod
    def show_transaction_detail(transaction: Transaction):
        """Display detailed transaction information."""
        Display.show_header("Transaction Details")
        print(transaction.detailed_str())
    
    @staticmethod
    def show_dashboard(wallet: Wallet):
        """Display the main dashboard."""
        Display.show_header("Budget Planner Dashboard")
        Display.show_balance(wallet)
        Display.show_category_breakdown(wallet)
        Display.show_transactions(wallet)
    
    @staticmethod
    def show_help():
        """Display available commands."""
        print("\n📌 Available Commands:")
        print("   +          - Add income transaction")
        print("   -          - Add expense transaction")
        print("   show N     - Show details of transaction N")
        print("   edit N     - Edit transaction N")
        print("   delete N   - Delete transaction N")
        print("   sort       - Change sorting method")
        print("   percent    - Show category percentages")
        print("   help       - Show this help message")
        print("   quit       - Exit the program")
    
    @staticmethod
    def show_categories(categories, transaction_type_name: str):
        """Display available categories."""
        print(f"\n📁 Available {transaction_type_name} Categories:")
        for i, cat in enumerate(sorted(categories), 1):
            print(f"   {i}. {cat}")
        print(f"   {len(categories) + 1}. [Add new category]")
    
    @staticmethod
    def show_sorting_options():
        """Display available sorting options."""
        strategies = SortingContext.get_available_strategies()
        print("\n🔄 Sorting Options:")
        for key, name in strategies.items():
            print(f"   {key}. {name}")
    
    @staticmethod
    def show_success(message: str):
        """Display a success message."""
        print(f"\n✅ {message}")
    
    @staticmethod
    def show_error(message: str):
        """Display an error message."""
        print(f"\n❌ {message}")
    
    @staticmethod
    def show_info(message: str):
        """Display an info message."""
        print(f"\nℹ️  {message}")
