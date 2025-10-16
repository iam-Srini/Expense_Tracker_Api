# app/utils/security.py

from passlib.hash import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, PyJWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas import TokenData


# ---------------------------
# Password hashing utilities
# ---------------------------
def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    """
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    """
    return bcrypt.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Alias for hash_password for consistency.
    """
    return hash_password(password)


# ---------------------------
# JWT token utilities
# ---------------------------
def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with a limited expiration.
    """
    encode_data = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_data.update({"exp": expires, "scope": "access_token"})
    encoded_jwt = jwt.encode(encode_data, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> TokenData:
    """
    Verify the access token and return the token data.
    Raises HTTP 401 if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        scope: str = payload.get("scope")

        if scope != "access_token":
            raise InvalidTokenError("Invalid token: incorrect scope")
        if username is None:
            raise InvalidTokenError("Invalid token: missing subject")

        return TokenData(username=username)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token with a longer expiration.
    """
    encode_data = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    encode_data.update({"exp": expires, "scope": "refresh_token"})
    encoded_jwt = jwt.encode(encode_data, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> TokenData:
    """
    Verify the refresh token and return the token data.
    Raises HTTP 401 if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        scope: str = payload.get("scope")

        if scope != "refresh_token":
            raise InvalidTokenError("Invalid token: incorrect scope")
        if username is None:
            raise InvalidTokenError("Invalid token: missing subject")

        return TokenData(username=username)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
