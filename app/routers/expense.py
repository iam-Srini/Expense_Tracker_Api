# app/routers/expense.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.repository import ExpenseRepository
from app.services.auth_service import get_current_user

expense_router = APIRouter(prefix="/expenses", tags=["Expenses"])


# ---------- CREATE EXPENSE ---------- #
@expense_router.post(
    "/", 
    response_model=ExpenseRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense"
)
def create_expense(
    expense_create: ExpenseCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new expense entry for the authenticated user.
    """
    expense_repo = ExpenseRepository(db)
    new_expense = expense_repo.create_expense(expense_create, user.id)
    return new_expense


# ---------- GET SINGLE EXPENSE ---------- #
@expense_router.get(
    "/{expense_id}", 
    response_model=ExpenseRead, 
    summary="Get a specific expense by ID"
)
def read_expense(
    expense_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a single expense by its ID.
    Ensures that the expense belongs to the authenticated user.
    """
    expense_repo = ExpenseRepository(db)
    expense = expense_repo.get_expense_by_id(expense_id)
    if not expense or expense.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )
    return expense


# ---------- GET ALL USER EXPENSES ---------- #
@expense_router.get(
    "/user/me",
    response_model=list[ExpenseRead],
    summary="List all expenses for the authenticated user"
)
def read_expenses_by_user(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve all expenses for the currently authenticated user.
    """
    expense_repo = ExpenseRepository(db)
    return expense_repo.get_expenses_by_user_id(user.id)


# ---------- UPDATE EXPENSE ---------- #
@expense_router.put(
    "/{expense_id}", 
    response_model=ExpenseRead,
    summary="Update an existing expense"
)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing expense.
    Ensures that the expense belongs to the authenticated user.
    """
    expense_repo = ExpenseRepository(db)
    expense = expense_repo.get_expense_by_id(expense_id)

    if not expense or expense.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    updated_expense = expense_repo.update_expense(expense_id, expense_update)
    if not updated_expense:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update expense",
        )
    return updated_expense


# ---------- DELETE EXPENSE ---------- #
@expense_router.delete(
    "/{expense_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense"
)
def delete_expense(
    expense_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete an expense by its ID.
    Ensures that the expense belongs to the authenticated user.
    """
    expense_repo = ExpenseRepository(db)
    expense = expense_repo.get_expense_by_id(expense_id)

    if not expense or expense.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    success = expense_repo.delete_expense(expense_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete expense",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------- MONTHLY SUMMARY ---------- #
@expense_router.get(
    "/summary/{year}/{month}",
    summary="Get monthly expense summary by category"
)
def get_monthly_expenses_summary(
    year: int,
    month: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return a summary of total expenses grouped by category 
    for a given month and year for the authenticated user.
    """
    expense_repo = ExpenseRepository(db)
    summary = expense_repo.get_monthly_expenses_by_category(user.id, year, month)
    return {
        "year": year,
        "month": month,
        "summary": summary,
    }
