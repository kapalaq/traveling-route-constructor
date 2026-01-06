from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models import Wallet, WalletType
from app.schemas import WalletCreate, WalletUpdate, WalletResponse

router = APIRouter(prefix="/api/wallets", tags=["wallets"])


@router.post("/", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    """Create a new wallet"""
    # Check for duplicate names
    existing = db.query(Wallet).filter(Wallet.name == wallet.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet with this name already exists"
        )

    db_wallet = Wallet(
        name=wallet.name,
        wallet_type=wallet.wallet_type,
        description=wallet.description,
        interest_rate=wallet.interest_rate,
        last_interest_applied=datetime.utcnow() if wallet.wallet_type == WalletType.DEPOSIT else None
    )

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


@router.get("/", response_model=List[WalletResponse])
def get_wallets(db: Session = Depends(get_db)):
    """Get all wallets"""
    wallets = db.query(Wallet).order_by(Wallet.created_at).all()

    # Apply interest to deposit wallets
    for wallet in wallets:
        if wallet.wallet_type == WalletType.DEPOSIT and wallet.interest_rate:
            _apply_interest(wallet, db)

    return wallets


@router.get("/{wallet_id}", response_model=WalletResponse)
def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    """Get a specific wallet"""
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    # Apply interest if it's a deposit wallet
    if wallet.wallet_type == WalletType.DEPOSIT and wallet.interest_rate:
        _apply_interest(wallet, db)

    return wallet


@router.put("/{wallet_id}", response_model=WalletResponse)
def update_wallet(wallet_id: int, wallet_update: WalletUpdate, db: Session = Depends(get_db)):
    """Update a wallet"""
    db_wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not db_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    # Check for duplicate names if name is being updated
    if wallet_update.name and wallet_update.name != db_wallet.name:
        existing = db.query(Wallet).filter(Wallet.name == wallet_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wallet with this name already exists"
            )

    update_data = wallet_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_wallet, field, value)

    db_wallet.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


@router.delete("/{wallet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wallet(wallet_id: int, db: Session = Depends(get_db)):
    """Delete a wallet"""
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    db.delete(wallet)
    db.commit()
    return None


def _apply_interest(wallet: Wallet, db: Session):
    """Apply compound interest to deposit wallet"""
    if not wallet.last_interest_applied or not wallet.interest_rate:
        return

    now = datetime.utcnow()
    days_passed = (now - wallet.last_interest_applied).days

    if days_passed >= 1:
        # Apply daily compound interest
        daily_rate = wallet.interest_rate / 365 / 100
        wallet.balance = wallet.balance * ((1 + daily_rate) ** days_passed)
        wallet.last_interest_applied = now
        wallet.updated_at = now
        db.commit()