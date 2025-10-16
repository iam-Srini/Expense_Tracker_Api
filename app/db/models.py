from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import String, ForeignKey, Float, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# -----------------------------------
# Base Class
# -----------------------------------
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


# -----------------------------------
# User Model
# -----------------------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    # Token fields
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    refresh_token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    expenses: Mapped[List["Expense"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


# -----------------------------------
# Expense Model
# -----------------------------------
class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    expense_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Foreign Key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationship
    user: Mapped["User"] = relationship(back_populates="expenses", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<Expense(id={self.id}, amount={self.amount}, "
            f"description='{self.description}', date={self.expense_date}, category='{self.category}')>"
        )
