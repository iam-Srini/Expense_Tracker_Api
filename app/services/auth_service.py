# app/services/auth_service.py

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db
from app.repository import UserRepository
from app.utils.security import verify_password, verify_access_token


def authenticate_user(self, email: str, password: str) -> User | None:
    """
    Authenticate a user by email and password.
    Returns the user if credentials are valid, else None.
    """
    user = self.get_user_by_email(email)
    if user and verify_password(password, user.password):
        return user
    return None


# OAuth2 scheme for dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User | None:
    """
    Retrieve the current user from the access token.
    Raises 401 if token is invalid or user does not exist.
    """
    token_data = verify_access_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(token_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
