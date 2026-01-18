"""Transaction model representing a single financial transaction."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class TransactionType(Enum):
    """Enum representing transaction types."""
    INCOME = "+"
    EXPENSE = "-"


@dataclass
class Transaction:
    """Represents a single financial transaction."""
    amount: float
    transaction_type: TransactionType
    category: str
    description: str = ""
    datetime_created: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    @property
    def signed_amount(self) -> float:
        """Return amount with sign based on transaction type."""
        if self.transaction_type == TransactionType.EXPENSE:
            return -abs(self.amount)
        return abs(self.amount)
    
    def __str__(self) -> str:
        sign = "+" if self.transaction_type == TransactionType.INCOME else "-"
        return f"{self.category} - {sign}{abs(self.amount):.2f}"
    
    def detailed_str(self) -> str:
        """Return detailed string representation."""
        sign = "+" if self.transaction_type == TransactionType.INCOME else "-"
        return (
            f"ID: {self.id}\n"
            f"Type: {self.transaction_type.value} ({'Income' if self.transaction_type == TransactionType.INCOME else 'Expense'})\n"
            f"Amount: {sign}{abs(self.amount):.2f}\n"
            f"Category: {self.category}\n"
            f"Description: {self.description or 'N/A'}\n"
            f"Date: {self.datetime_created.strftime('%Y-%m-%d %H:%M:%S')}"
        )
