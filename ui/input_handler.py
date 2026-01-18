"""Input handling utilities for the budget planner."""
from datetime import datetime
from typing import Optional, Tuple, Set
from models.transaction import Transaction, TransactionType
from ui.display import Display


class InputHandler:
    """Handles all user input operations."""
    
    @staticmethod
    def get_command() -> str:
        """Get a command from user."""
        return input("\n> ").strip().lower()
    
    @staticmethod
    def get_amount() -> Optional[float]:
        """Get a valid amount from user."""
        try:
            amount_str = input("Enter amount: ").strip()
            amount = float(amount_str)
            if amount <= 0:
                Display.show_error("Amount must be positive")
                return None
            return amount
        except ValueError:
            Display.show_error("Invalid amount. Please enter a number.")
            return None
    
    @staticmethod
    def get_category(categories: Set[str], transaction_type: TransactionType) -> Optional[str]:
        """Get a category from user, with option to add new."""
        type_name = "Income" if transaction_type == TransactionType.INCOME else "Expense"
        Display.show_categories(categories, type_name)
        
        sorted_categories = sorted(categories)
        choice = input("Select category (number or name): ").strip()
        
        # Check if it's a number
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(sorted_categories):
                return sorted_categories[choice_num - 1]
            elif choice_num == len(sorted_categories) + 1:
                # Add new category
                new_category = input("Enter new category name: ").strip()
                if new_category:
                    return new_category
                Display.show_error("Category name cannot be empty")
                return None
            else:
                Display.show_error("Invalid selection")
                return None
        except ValueError:
            # It's a name - check if it exists or add it
            if choice in categories:
                return choice
            # Ask if they want to add it
            confirm = input(f"Category '{choice}' doesn't exist. Add it? (y/n): ").strip().lower()
            if confirm == 'y':
                return choice
            return None
    
    @staticmethod
    def get_description() -> str:
        """Get an optional description from user."""
        return input("Enter description (optional): ").strip()
    
    @staticmethod
    def get_datetime() -> datetime:
        """Get datetime from user, defaulting to now."""
        date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        
        if not date_str:
            return datetime.now()
        
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            Display.show_info("Invalid date format. Using current date.")
            return datetime.now()
    
    @staticmethod
    def get_transaction_input(
        transaction_type: TransactionType,
        categories: Set[str]
    ) -> Optional[Transaction]:
        """Get all inputs for a new transaction step by step."""
        type_name = "Income" if transaction_type == TransactionType.INCOME else "Expense"
        Display.show_header(f"New {type_name} Transaction")
        
        # Step 1: Amount
        amount = InputHandler.get_amount()
        if amount is None:
            return None
        
        # Step 2: Category
        category = InputHandler.get_category(categories, transaction_type)
        if category is None:
            return None
        
        # Step 3: Description
        description = InputHandler.get_description()
        
        # Step 4: Date
        date = InputHandler.get_datetime()
        
        return Transaction(
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            description=description,
            datetime_created=date
        )
    
    @staticmethod
    def get_edit_input(
        transaction: Transaction,
        categories: Set[str]
    ) -> Optional[Transaction]:
        """Get inputs for editing a transaction."""
        Display.show_header("Edit Transaction")
        Display.show_info("Press Enter to keep current value")
        
        print(f"\nCurrent values:")
        print(transaction.detailed_str())
        print()
        
        # Amount
        amount_str = input(f"Amount [{transaction.amount}]: ").strip()
        if amount_str:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    Display.show_error("Amount must be positive")
                    return None
            except ValueError:
                Display.show_error("Invalid amount")
                return None
        else:
            amount = transaction.amount
        
        # Category
        print(f"\nCurrent category: {transaction.category}")
        change_cat = input("Change category? (y/n): ").strip().lower()
        if change_cat == 'y':
            category = InputHandler.get_category(categories, transaction.transaction_type)
            if category is None:
                return None
        else:
            category = transaction.category
        
        # Description
        desc_input = input(f"Description [{transaction.description or 'N/A'}]: ").strip()
        description = desc_input if desc_input else transaction.description
        
        # Date
        current_date = transaction.datetime_created.strftime("%Y-%m-%d")
        date_str = input(f"Date [{current_date}]: ").strip()
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                Display.show_info("Invalid date format. Keeping current date.")
                date = transaction.datetime_created
        else:
            date = transaction.datetime_created
        
        return Transaction(
            amount=amount,
            transaction_type=transaction.transaction_type,
            category=category,
            description=description,
            datetime_created=date
        )
    
    @staticmethod
    def confirm(message: str) -> bool:
        """Get a yes/no confirmation from user."""
        response = input(f"{message} (y/n): ").strip().lower()
        return response == 'y'
    
    @staticmethod
    def parse_indexed_command(command: str) -> Tuple[Optional[str], Optional[int]]:
        """Parse commands like 'show 1', 'edit 2', 'delete 3'."""
        parts = command.split()
        if len(parts) != 2:
            return None, None
        
        action = parts[0]
        try:
            index = int(parts[1])
            return action, index
        except ValueError:
            return None, None
