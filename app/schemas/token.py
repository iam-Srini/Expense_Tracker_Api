# app/schemas/token.py

from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for access and refresh tokens returned upon authentication.
    """
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for decoded token data, typically used for verifying the user.
    """
    username: str | None = None
