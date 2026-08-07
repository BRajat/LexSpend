from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class BudgetLedgerBase(SQLModel):
    budget_id: int
    invoice_id: int
    amount: float
    entry_type: str = "invoice_approved"
    created_at: str


# 2. Database Table Model (maps to SQL table)
class BudgetLedger(BudgetLedgerBase, table=True):
    __tablename__ = "budget_ledger"
    ledger_id: Optional[int] = Field(default=None, primary_key=True)
    budget_id: int = Field(foreign_key="budget.budget_id")
    invoice_id: int = Field(foreign_key="invoice.invoice_id")
    budget: Optional["Budget"] = Relationship(back_populates="ledgers")
    invoice: Optional["Invoice"] = Relationship(back_populates="budget_ledgers")


# 3. Input Schema (used when a client creates a budget ledger — no ledger_id needed)
class BudgetLedgerCreate(BudgetLedgerBase):
    pass


# 4. Response Schema (used when returning data to the client)
class BudgetLedgerRead(BudgetLedgerBase):
    ledger_id: int
