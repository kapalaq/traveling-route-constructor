from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.api import wallets, operations
from app.models import Wallet

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budget Accounting App", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(wallets.router)
app.include_router(operations.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Main page"""
    # Get all wallets
    wallets_list = db.query(Wallet).all()

    # If no wallets exist, create a default main wallet
    if not wallets_list:
        from app.models.models import WalletType
        main_wallet = Wallet(
            name="Main Wallet",
            wallet_type=WalletType.SIMPLE,
            description="Your primary wallet"
        )
        db.add(main_wallet)
        db.commit()
        db.refresh(main_wallet)
        wallets_list = [main_wallet]

    wallets_dict = [
        w.toJSON()
        for w in wallets_list
    ]

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "wallets": wallets_dict}
    )


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """Profile page (placeholder)"""
    return templates.TemplateResponse(
        "profile.html",
        {"request": request}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)