# app/repository/user_repo.py

from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas import UserCreate, UserUpdate
from app.utils.security import hash_password


class UserRepository:
    """Repository layer for handling User database operations."""

    def __init__(self, db: Session):
        self.db = db

    # ---------- READ OPERATIONS ---------- #

    def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address."""
        return self.db.query(User).filter(User.email == email).first()

    # ---------- CREATE ---------- #

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user with a hashed password."""
        hashed_password = hash_password(user_create.password)

        new_user = User(
            name=user_create.name.strip(),
            email=user_create.email.lower(),
            password=hashed_password,
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    # ---------- UPDATE ---------- #

    def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        """Update user details. Hash password if it is changed."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        # Apply partial updates dynamically
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "password":
                value = hash_password(value)
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    # ---------- DELETE ---------- #

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
