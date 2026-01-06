from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from app.models import WalletType, OperationType, Category


# Wallet Schemas
class WalletBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    wallet_type: WalletType
    description: Optional[str] = Field(None, max_length=500)
    interest_rate: Optional[float] = Field(None, ge=0, le=100)

    @field_validator('interest_rate')
    @classmethod
    def validate_interest_rate(cls, v, info):
        wallet_type = info.data.get('wallet_type')
        if wallet_type == WalletType.DEPOSIT and v is None:
            raise ValueError('Interest rate is required for deposit wallets')
        if wallet_type != WalletType.DEPOSIT and v is not None:
            raise ValueError('Interest rate can only be set for deposit wallets')
        return v


class WalletCreate(WalletBase):
    pass


class WalletUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    interest_rate: Optional[float] = Field(None, ge=0, le=100)


class WalletResponse(WalletBase):
    id: int
    balance: float
    last_interest_applied: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Operation Schemas
class OperationBase(BaseModel):
    operation_type: OperationType
    amount: float = Field(..., gt=0)
    category: Category
    description: Optional[str] = Field(None, max_length=500)
    operation_time: Optional[str] = None
    target_wallet_id: Optional[int] = None

    @field_validator('target_wallet_id')
    @classmethod
    def validate_target_wallet(cls, v, info):
        operation_type = info.data.get('operation_type')
        if operation_type == OperationType.TRANSFER and v is None:
            raise ValueError('Target wallet is required for transfer operations')
        if operation_type != OperationType.TRANSFER and v is not None:
            raise ValueError('Target wallet can only be set for transfer operations')
        return v


class OperationCreate(OperationBase):
    wallet_id: int


class OperationResponse(OperationBase):
    id: int
    wallet_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Filter Schemas
class OperationFilter(BaseModel):
    wallet_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[Category] = None
    operation_type: Optional[OperationType] = None


# Summary Schemas
class CategorySummary(BaseModel):
    category: Category
    total_amount: float
    count: int


class OperationSummary(BaseModel):
    total_additions: float
    total_withdrawals: float
    net_change: float
    categories: List[CategorySummary]
    period_start: Optional[datetime]
    period_end: Optional[datetime]