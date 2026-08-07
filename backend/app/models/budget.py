from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class BudgetBase(SQLModel):
    matter_id: int
    allocated_amt: float
    threshold_pct: float = 80.0


# 2. Database Table Model (maps to SQL table)
class Budget(BudgetBase, table=True):
    __tablename__ = "budget"
    budget_id: Optional[int] = Field(default=None, primary_key=True)
    matter_id: int = Field(foreign_key="matter.matter_id", unique=True)

    matter: Optional["Matter"] = Relationship(back_populates="budget")
    ledgers: List["BudgetLedger"] = Relationship(back_populates="budget")
    alerts: List["Alert"] = Relationship(back_populates="budget")


# 3. Input Schema (used when a client creates a budget — no budget_id needed)
class BudgetCreate(BudgetBase):
    pass


# 4. Response Schema (used when returning data to the client)
class BudgetRead(BudgetBase):
    budget_id: int
