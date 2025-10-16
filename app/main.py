from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import Base
from app.db.session import engine
from app.routers import api_router

# -------------------------------
# Application Initialization
# -------------------------------
app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="API for tracking user expenses, managing authentication, and reporting."
)

# Include all routers
app.include_router(api_router)

# -------------------------------
# Database Initialization
# -------------------------------
try:
    Base.metadata.create_all(bind=engine)
except SQLAlchemyError as e:
    # Log the error or handle appropriately in production
    print(f"Database initialization failed: {e}")

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint providing API info and available routes.
    """
    return {
        "message": "Welcome to Expense Tracker API!",
        "version": app.version,
        "endpoints": {
            "users": "/users",
            "expenses": "/expenses",
            "auth": "/auth",
            "health": "/health"
        }
    }

# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}
