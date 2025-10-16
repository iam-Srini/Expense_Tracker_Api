# app/routers/api.py

from fastapi import APIRouter

# Import individual routers
from .users import user_router
from .expense import expense_router
from .auth import auth_router

# Main API router that aggregates all sub-routers
api_router = APIRouter()

# Include sub-routers
api_router.include_router(user_router)
api_router.include_router(expense_router)
api_router.include_router(auth_router)