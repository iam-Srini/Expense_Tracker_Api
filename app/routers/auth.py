# app/routers/auth.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import Token
from app.repository import UserRepository
from app.utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------- LOGIN ---------- #
@auth_router.post("/login", response_model=Token, summary="Authenticate user and return access + refresh tokens")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Authenticate the user using email and password.
    Returns an access token and a refresh token upon success.
    """
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


# ---------- REFRESH TOKEN ---------- #
@auth_router.post("/refresh", response_model=Token, summary="Refresh access token using a valid refresh token")
async def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    """
    Verify the refresh token and return a new access token.
    Keeps the same refresh token if still valid.
    """
    token_data = verify_refresh_token(refresh_token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_access_token = create_access_token({"sub": token_data.username})

    return Token(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
