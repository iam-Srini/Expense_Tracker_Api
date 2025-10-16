# app/schemas/expense.py

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional


class ExpenseBase(BaseModel):
    amount: float = Field(
        ..., gt=0, description="The amount of the expense"
    )
    description: str = Field(
        ..., max_length=255, description="The description of the expense"
    )
    expense_date: date = Field(
        default_factory=date.today, description="The date of the expense"
    )
    category: Optional[str] = Field(
        None, max_length=100, description="The category of the expense"
    )


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: float | None = Field(
        None, gt=0, description="The amount of the expense"
    )
    description: str | None = Field(
        None, max_length=255, description="The description of the expense"
    )
    expense_date: date | None = Field(
        None, description="The date of the expense"
    )
    category: Optional[str] = Field(
        None, max_length=100, description="The category of the expense"
    )


class ExpenseRead(ExpenseBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
