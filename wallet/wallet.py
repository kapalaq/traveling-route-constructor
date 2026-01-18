"""Wallet class that manages all transactions."""
from typing import List, Dict, Optional
from collections import defaultdict
from models.transaction import Transaction, TransactionType
from models.category import CategoryManager
from strategies.sorting import SortingContext


class Wallet:
    """Main wallet class that holds and manages all transactions."""
    
    def __init__(self):
        self._transactions: List[Transaction] = []
        self._category_manager = CategoryManager()
        self._sorting_context = SortingContext()
    
    @property
    def category_manager(self) -> CategoryManager:
        return self._category_manager
    
    @property
    def sorting_context(self) -> SortingContext:
        return self._sorting_context
    
    @property
    def balance(self) -> float:
        """Calculate total balance."""
        return sum(t.signed_amount for t in self._transactions)
    
    @property
    def total_income(self) -> float:
        """Calculate total income."""
        return sum(t.amount for t in self._transactions 
                   if t.transaction_type == TransactionType.INCOME)
    
    @property
    def total_expenses(self) -> float:
        """Calculate total expenses."""
        return sum(t.amount for t in self._transactions 
                   if t.transaction_type == TransactionType.EXPENSE)
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the wallet."""
        self._category_manager.add_category(
            transaction.category, 
            transaction.transaction_type
        )
        self._transactions.append(transaction)
    
    def get_transaction(self, index: int) -> Optional[Transaction]:
        """Get a transaction by its display index (1-based)."""
        sorted_transactions = self._sorting_context.sort(self._transactions)
        if 1 <= index <= len(sorted_transactions):
            return sorted_transactions[index - 1]
        return None
    
    def update_transaction(self, index: int, updated: Transaction) -> bool:
        """Update a transaction by its display index."""
        sorted_transactions = self._sorting_context.sort(self._transactions)
        if 1 <= index <= len(sorted_transactions):
            old_transaction = sorted_transactions[index - 1]
            # Find in original list by ID
            for i, t in enumerate(self._transactions):
                if t.id == old_transaction.id:
                    updated.id = old_transaction.id
                    self._transactions[i] = updated
                    return True
        return False
    
    def delete_transaction(self, index: int) -> bool:
        """Delete a transaction by its display index."""
        sorted_transactions = self._sorting_context.sort(self._transactions)
        if 1 <= index <= len(sorted_transactions):
            transaction_to_delete = sorted_transactions[index - 1]
            self._transactions = [
                t for t in self._transactions 
                if t.id != transaction_to_delete.id
            ]
            return True
        return False
    
    def get_sorted_transactions(self) -> List[Transaction]:
        """Get all transactions sorted by current strategy."""
        return self._sorting_context.sort(self._transactions)
    
    def get_category_totals(self) -> Dict[str, float]:
        """Get total amount per category (only non-zero)."""
        totals: Dict[str, float] = defaultdict(float)
        for t in self._transactions:
            totals[t.category] += t.signed_amount
        return {k: v for k, v in totals.items() if v != 0}
    
    def get_category_percentages(self) -> Dict[str, float]:
        """Get percentage contribution of each category to total absolute value."""
        total_absolute = sum(abs(t.amount) for t in self._transactions)
        if total_absolute == 0:
            return {}
        
        category_absolutes: Dict[str, float] = defaultdict(float)
        for t in self._transactions:
            category_absolutes[t.category] += abs(t.amount)
        
        return {
            category: (amount / total_absolute) * 100 
            for category, amount in category_absolutes.items()
            if amount > 0
        }
    
    def transaction_count(self) -> int:
        """Return the number of transactions."""
        return len(self._transactions)
