# app/repository/expense_repo.py

from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Expense
from app.schemas import ExpenseCreate, ExpenseUpdate


class ExpenseRepository:
    """Repository layer for handling Expense database operations."""

    def __init__(self, db: Session):
        self.db = db

    # ---------- CRUD OPERATIONS ---------- #

    def get_expense_by_id(self, expense_id: int) -> Expense | None:
        """Retrieve a single expense by its ID."""
        return self.db.query(Expense).filter(Expense.id == expense_id).first()

    def get_expenses_by_user_id(self, user_id: int) -> list[Expense]:
        """Retrieve all expenses for a specific user."""
        return (
            self.db.query(Expense)
            .filter(Expense.user_id == user_id)
            .order_by(Expense.expense_date.desc())
            .all()
        )

    def create_expense(self, expense_create: ExpenseCreate, user_id: int) -> Expense:
        """Create a new expense for a user."""
        new_expense = Expense(
            amount=expense_create.amount,
            description=expense_create.description,
            expense_date=expense_create.expense_date or date.today(),
            category=expense_create.category,
            user_id=user_id,
        )
        self.db.add(new_expense)
        self.db.commit()
        self.db.refresh(new_expense)
        return new_expense

    def update_expense(self, expense_id: int, expense_update: ExpenseUpdate) -> Expense | None:
        """Update an existing expense by ID."""
        expense = self.get_expense_by_id(expense_id)
        if not expense:
            return None

        # Apply partial updates
        for field, value in expense_update.dict(exclude_unset=True).items():
            setattr(expense, field, value)

        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID."""
        expense = self.get_expense_by_id(expense_id)
        if not expense:
            return False
        self.db.delete(expense)
        self.db.commit()
        return True

    # ---------- AGGREGATION ---------- #

    def get_monthly_expenses_by_category(self, user_id: int, year: int, month: int) -> list[dict]:
        """Aggregate expenses by category for a given month and year."""
        results = (
            self.db.query(
                Expense.category,
                func.sum(Expense.amount).label("total_amount"),
            )
            .filter(
                Expense.user_id == user_id,
                func.extract("year", Expense.expense_date) == year,
                func.extract("month", Expense.expense_date) == month,
            )
            .group_by(Expense.category)
            .all()
        )

        return [
            {
                "category": category or "Uncategorized",
                "total_amount": float(total_amount or 0),
            }
            for category, total_amount in results
        ]
