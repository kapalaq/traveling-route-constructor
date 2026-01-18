"""Command handlers for the budget planner using Command Pattern."""
from abc import ABC, abstractmethod
from typing import Optional
from wallet.wallet import Wallet
from models.transaction import TransactionType
from ui.display import Display
from ui.input_handler import InputHandler


class Command(ABC):
    """Abstract base class for commands."""
    
    @abstractmethod
    def execute(self) -> bool:
        """Execute the command. Returns True if app should continue."""
        pass


class AddTransactionCommand(Command):
    """Command to add a new transaction."""
    
    def __init__(self, wallet: Wallet, transaction_type: TransactionType):
        self._wallet = wallet
        self._transaction_type = transaction_type
    
    def execute(self) -> bool:
        categories = self._wallet.category_manager.get_categories(self._transaction_type)
        transaction = InputHandler.get_transaction_input(self._transaction_type, categories)
        
        if transaction:
            self._wallet.add_transaction(transaction)
            Display.show_success("Transaction added successfully!")
        else:
            Display.show_error("Transaction cancelled")
        
        return True


class ShowTransactionCommand(Command):
    """Command to show transaction details."""
    
    def __init__(self, wallet: Wallet, index: int):
        self._wallet = wallet
        self._index = index
    
    def execute(self) -> bool:
        transaction = self._wallet.get_transaction(self._index)
        
        if transaction:
            Display.show_transaction_detail(transaction)
        else:
            Display.show_error(f"Transaction #{self._index} not found")
        
        return True


class EditTransactionCommand(Command):
    """Command to edit a transaction."""
    
    def __init__(self, wallet: Wallet, index: int):
        self._wallet = wallet
        self._index = index
    
    def execute(self) -> bool:
        transaction = self._wallet.get_transaction(self._index)
        
        if not transaction:
            Display.show_error(f"Transaction #{self._index} not found")
            return True
        
        categories = self._wallet.category_manager.get_categories(transaction.transaction_type)
        updated = InputHandler.get_edit_input(transaction, categories)
        
        if updated:
            if self._wallet.update_transaction(self._index, updated):
                Display.show_success("Transaction updated successfully!")
            else:
                Display.show_error("Failed to update transaction")
        else:
            Display.show_error("Edit cancelled")
        
        return True


class DeleteTransactionCommand(Command):
    """Command to delete a transaction."""
    
    def __init__(self, wallet: Wallet, index: int):
        self._wallet = wallet
        self._index = index
    
    def execute(self) -> bool:
        transaction = self._wallet.get_transaction(self._index)
        
        if not transaction:
            Display.show_error(f"Transaction #{self._index} not found")
            return True
        
        Display.show_transaction_detail(transaction)
        
        if InputHandler.confirm("Are you sure you want to delete this transaction?"):
            if self._wallet.delete_transaction(self._index):
                Display.show_success("Transaction deleted successfully!")
            else:
                Display.show_error("Failed to delete transaction")
        else:
            Display.show_info("Deletion cancelled")
        
        return True


class ChangeSortingCommand(Command):
    """Command to change sorting strategy."""
    
    def __init__(self, wallet: Wallet):
        self._wallet = wallet
    
    def execute(self) -> bool:
        Display.show_sorting_options()
        choice = input("Select sorting method: ").strip()
        
        if self._wallet.sorting_context.set_strategy(choice):
            Display.show_success(
                f"Sorting changed to: {self._wallet.sorting_context.current_strategy.name}"
            )
        else:
            Display.show_error("Invalid sorting option")
        
        return True


class ShowPercentagesCommand(Command):
    """Command to show category percentages."""
    
    def __init__(self, wallet: Wallet):
        self._wallet = wallet
    
    def execute(self) -> bool:
        percentages = self._wallet.get_category_percentages()
        
        if not percentages:
            Display.show_info("No transactions to calculate percentages")
            return True
        
        Display.show_header("Category Percentages")
        for category, pct in sorted(percentages.items(), key=lambda x: -x[1]):
            print(f"   {category}: {pct:.1f}%")
        
        return True


class HelpCommand(Command):
    """Command to show help."""
    
    def execute(self) -> bool:
        Display.show_help()
        return True


class QuitCommand(Command):
    """Command to quit the application."""
    
    def execute(self) -> bool:
        Display.show_info("Thank you for using Budget Planner. Goodbye!")
        return False


class RefreshCommand(Command):
    """Command to refresh/show dashboard."""
    
    def __init__(self, wallet: Wallet):
        self._wallet = wallet
    
    def execute(self) -> bool:
        Display.show_dashboard(self._wallet)
        return True


class CommandFactory:
    """Factory for creating commands."""
    
    def __init__(self, wallet: Wallet):
        self._wallet = wallet
    
    def create_command(self, command_str: str) -> Optional[Command]:
        """Create a command based on user input."""
        command_str = command_str.strip().lower()
        
        # Simple commands
        if command_str == '+':
            return AddTransactionCommand(self._wallet, TransactionType.INCOME)
        elif command_str == '-':
            return AddTransactionCommand(self._wallet, TransactionType.EXPENSE)
        elif command_str == 'sort':
            return ChangeSortingCommand(self._wallet)
        elif command_str == 'percent':
            return ShowPercentagesCommand(self._wallet)
        elif command_str == 'help':
            return HelpCommand()
        elif command_str in ('quit', 'exit', 'q'):
            return QuitCommand()
        elif command_str == '' or command_str == 'refresh':
            return RefreshCommand(self._wallet)
        
        # Indexed commands
        action, index = InputHandler.parse_indexed_command(command_str)
        if action and index:
            if action == 'show':
                return ShowTransactionCommand(self._wallet, index)
            elif action == 'edit':
                return EditTransactionCommand(self._wallet, index)
            elif action == 'delete':
                return DeleteTransactionCommand(self._wallet, index)
        
        return None
