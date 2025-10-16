# app/routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.repository import UserRepository
from app.db.session import get_db
from app.db.models import User
from app.services.auth_service import get_current_user
from app.schemas import UserCreate, UserRead, UserUpdate

user_router = APIRouter(prefix="/users", tags=["Users"])


# ---------- CREATE USER ---------- #
@user_router.post(
    "/", 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with a unique email.
    Raises 400 if email is already registered.
    """
    user_repo = UserRepository(db)

    if user_repo.get_user_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return user_repo.create_user(user_create)


# ---------- READ USER ---------- #
@user_router.get(
    "/{user_id}", 
    response_model=UserRead,
    summary="Get a user by ID"
)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a user by their ID.
    Raises 404 if the user does not exist.
    """
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Not Authorised to access this user"
        )

    return user


# ---------- UPDATE USER ---------- #
@user_router.put(
    "/{user_id}", 
    response_model=UserRead,
    summary="Update user details"
)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update user fields.
    Raises 404 if the user does not exist.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to update this user"
        )
    

    user_repo = UserRepository(db)
    updated_user = user_repo.update_user(user_id, user_update)


    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    

    return updated_user


# ---------- DELETE USER ---------- #
@user_router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user by ID"
)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a user by ID.
    Raises 404 if the user does not exist.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorised to delete this user"
        )


    user_repo = UserRepository(db)
    if not user_repo.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
