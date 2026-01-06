from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class WalletType(str, enum.Enum):
    SIMPLE = "simple"
    DEPOSIT = "deposit"
    STOCK = "stock"


class OperationType(str, enum.Enum):
    ADDITION = "addition"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"


class Category(str, enum.Enum):
    HEALTHCARE = "healthcare"
    FOOD = "food"
    HOME = "home"
    EDUCATION = "education"
    SUBSCRIPTIONS = "subscriptions"
    ENTERTAINMENT = "entertainment"
    RESTAURANTS = "restaurants"
    TRANSPORT = "transport"
    SHOPPING = "shopping"
    SALARY = "salary"
    OTHER = "other"


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    wallet_type = Column(SQLEnum(WalletType), nullable=False)
    description = Column(String, nullable=True)
    balance = Column(Float, default=0.0)

    # For deposit wallets
    interest_rate = Column(Float, nullable=True)  # Annual interest rate in percentage
    last_interest_applied = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    operations = relationship("Operation", back_populates="wallet", foreign_keys="[Operation.wallet_id]", cascade="all, delete-orphan")

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "wallet_type": self.wallet_type.value if self.wallet_type else None,
            "description": self.description,
            "balance": self.balance,
            "interest_rate": self.interest_rate,
            "last_interest_applied": self.last_interest_applied.isoformat() if self.last_interest_applied else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    operation_type = Column(SQLEnum(OperationType), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(SQLEnum(Category), nullable=False)
    description = Column(String, nullable=True)
    operation_time = Column(DateTime, default=datetime.utcnow)

    # For transfer operations
    target_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    wallet = relationship("Wallet", back_populates="operations", foreign_keys=[wallet_id])
    target_wallet = relationship("Wallet", foreign_keys=[target_wallet_id])

    def toJSON(self):
        return {
            "id": self.id,
            "wallet_id": self.wallet_id,
            "operation_type": self.operation_type.value if self.operation_type else None,
            "amount": self.amount,
            "category": self.category.value if self.category else None,
            "description": self.description,
            "operation_time": self.operation_time.isoformat() if self.operation_time else None,
            "target_wallet_id": self.target_wallet_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }