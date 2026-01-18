"""Sorting strategies for transactions using Strategy Pattern."""
from abc import ABC, abstractmethod
from typing import List
from models.transaction import Transaction


class SortingStrategy(ABC):
    """Abstract base class for sorting strategies."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the sorting strategy."""
        pass
    
    @abstractmethod
    def sort(self, transactions: List[Transaction]) -> List[Transaction]:
        """Sort transactions according to the strategy."""
        pass


class MostRecentSorting(SortingStrategy):
    """Sort transactions by date, most recent first."""
    
    @property
    def name(self) -> str:
        return "Most Recent"
    
    def sort(self, transactions: List[Transaction]) -> List[Transaction]:
        return sorted(transactions, key=lambda t: t.datetime_created, reverse=True)


class HighToLowSorting(SortingStrategy):
    """Sort transactions by absolute amount, highest first."""
    
    @property
    def name(self) -> str:
        return "High to Low"
    
    def sort(self, transactions: List[Transaction]) -> List[Transaction]:
        return sorted(transactions, key=lambda t: abs(t.amount), reverse=True)


class CategoryAlphabeticalSorting(SortingStrategy):
    """Sort transactions alphabetically by category."""
    
    @property
    def name(self) -> str:
        return "Alphabetical by Category"
    
    def sort(self, transactions: List[Transaction]) -> List[Transaction]:
        return sorted(transactions, key=lambda t: t.category.lower())


class SortingContext:
    """Context class that uses sorting strategies."""
    
    STRATEGIES = {
        '1': MostRecentSorting,
        '2': HighToLowSorting,
        '3': CategoryAlphabeticalSorting,
    }
    
    def __init__(self):
        self._strategy: SortingStrategy = MostRecentSorting()
    
    @property
    def current_strategy(self) -> SortingStrategy:
        return self._strategy
    
    def set_strategy(self, strategy_key: str) -> bool:
        """Set sorting strategy by key."""
        if strategy_key in self.STRATEGIES:
            self._strategy = self.STRATEGIES[strategy_key]()
            return True
        return False
    
    def sort(self, transactions: List[Transaction]) -> List[Transaction]:
        """Sort transactions using current strategy."""
        return self._strategy.sort(transactions)
    
    @classmethod
    def get_available_strategies(cls) -> dict:
        """Return available sorting strategies."""
        return {key: cls.STRATEGIES[key]().name for key in cls.STRATEGIES}
