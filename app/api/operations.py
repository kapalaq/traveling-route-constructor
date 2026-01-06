from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from collections import defaultdict

from app.database import get_db
from app.models import Operation, Wallet, OperationType, Category
from app.schemas import OperationCreate, OperationResponse, OperationSummary, CategorySummary

router = APIRouter(prefix="/api/operations", tags=["operations"])


@router.post("/", response_model=OperationResponse, status_code=status.HTTP_201_CREATED)
def create_operation(operation: OperationCreate, db: Session = Depends(get_db)):
    """Create a new operation"""
    # Verify wallet exists
    wallet = db.query(Wallet).filter(Wallet.id == operation.wallet_id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    # Verify target wallet for transfers
    if operation.operation_type == OperationType.TRANSFER:
        if not operation.target_wallet_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Target wallet is required for transfer operations"
            )
        target_wallet = db.query(Wallet).filter(Wallet.id == operation.target_wallet_id).first()
        if not target_wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target wallet not found"
            )
        if operation.wallet_id == operation.target_wallet_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot transfer to the same wallet"
            )

    # Check if wallet has sufficient balance for withdrawals/transfers
    if operation.operation_type in [OperationType.WITHDRAWAL, OperationType.TRANSFER]:
        if wallet.balance < operation.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )

    # Create operation
    db_operation = Operation(
        wallet_id=operation.wallet_id,
        operation_type=operation.operation_type,
        amount=operation.amount,
        category=operation.category,
        description=operation.description,
        operation_time=operation.operation_time or datetime.utcnow(),
        target_wallet_id=operation.target_wallet_id
    )

    # Update wallet balance
    if operation.operation_type == OperationType.ADDITION:
        wallet.balance += operation.amount
    elif operation.operation_type == OperationType.WITHDRAWAL:
        wallet.balance -= operation.amount
    elif operation.operation_type == OperationType.TRANSFER:
        wallet.balance -= operation.amount
        target_wallet = db.query(Wallet).filter(Wallet.id == operation.target_wallet_id).first()
        target_wallet.balance += operation.amount
        target_wallet.updated_at = datetime.utcnow()

    wallet.updated_at = datetime.utcnow()

    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


@router.get("/", response_model=List[OperationResponse])
def get_operations(
        wallet_id: Optional[int] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        category: Optional[Category] = Query(None),
        operation_type: Optional[OperationType] = Query(None),
        db: Session = Depends(get_db)
):
    """Get operations with optional filters"""
    query = db.query(Operation)

    if wallet_id:
        query = query.filter(Operation.wallet_id == wallet_id)

    if start_date:
        query = query.filter(Operation.operation_time >= start_date)

    if end_date:
        query = query.filter(Operation.operation_time <= end_date)

    if category:
        query = query.filter(Operation.category == category)

    if operation_type:
        query = query.filter(Operation.operation_type == operation_type)

    operations = query.order_by(Operation.operation_time.desc()).all()
    return operations


@router.get("/summary", response_model=OperationSummary)
def get_operations_summary(
        wallet_id: Optional[int] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        db: Session = Depends(get_db)
):
    """Get summary of operations with category breakdown"""
    query = db.query(Operation)

    if wallet_id:
        query = query.filter(Operation.wallet_id == wallet_id)

    if start_date:
        query = query.filter(Operation.operation_time >= start_date)

    if end_date:
        query = query.filter(Operation.operation_time <= end_date)

    operations = query.all()

    # Calculate totals
    total_additions = sum(
        op.amount for op in operations
        if op.operation_type == OperationType.ADDITION
    )
    total_withdrawals = sum(
        op.amount for op in operations
        if op.operation_type in [OperationType.WITHDRAWAL, OperationType.TRANSFER]
    )

    # Calculate category breakdown
    category_data = defaultdict(lambda: {"total": 0.0, "count": 0})
    for op in operations:
        category_data[op.category]["total"] += op.amount
        category_data[op.category]["count"] += 1

    categories = [
        CategorySummary(
            category=cat,
            total_amount=data["total"],
            count=data["count"]
        )
        for cat, data in category_data.items()
    ]

    return OperationSummary(
        total_additions=total_additions,
        total_withdrawals=total_withdrawals,
        net_change=total_additions - total_withdrawals,
        categories=categories,
        period_start=start_date,
        period_end=end_date
    )


@router.get("/{operation_id}", response_model=OperationResponse)
def get_operation(operation_id: int, db: Session = Depends(get_db)):
    """Get a specific operation"""
    operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if not operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not found"
        )
    return operation


@router.delete("/{operation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(operation_id: int, db: Session = Depends(get_db)):
    """Delete an operation (and reverse its effect on wallet balance)"""
    operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if not operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not found"
        )

    # Reverse the operation's effect on wallet balance
    wallet = db.query(Wallet).filter(Wallet.id == operation.wallet_id).first()
    if wallet:
        if operation.operation_type == OperationType.ADDITION:
            wallet.balance -= operation.amount
        elif operation.operation_type == OperationType.WITHDRAWAL:
            wallet.balance += operation.amount
        elif operation.operation_type == OperationType.TRANSFER:
            wallet.balance += operation.amount
            if operation.target_wallet_id:
                target_wallet = db.query(Wallet).filter(Wallet.id == operation.target_wallet_id).first()
                if target_wallet:
                    target_wallet.balance -= operation.amount
                    target_wallet.updated_at = datetime.utcnow()

        wallet.updated_at = datetime.utcnow()

    db.delete(operation)
    db.commit()
    return None