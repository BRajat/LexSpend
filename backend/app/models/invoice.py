from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class InvoiceBase(SQLModel):
    matter_id: int
    firm_id: int
    invoice_no: str
    invoice_date: str
    total_amount: float
    status: str = "submitted"
    confidence_score: Optional[float] = None


# 2. Database Table Model (maps to SQL table)
class Invoice(InvoiceBase, table=True):
    __tablename__ = "invoice"
    invoice_id: Optional[int] = Field(default=None, primary_key=True)
    firm_id: int = Field(foreign_key="firm.firm_id")
    matter_id: int = Field(foreign_key="matter.matter_id")

    matter: Optional["Matter"] = Relationship(back_populates="invoices")
    firm: Optional["Firm"] = Relationship(back_populates="invoices")
    line_items: List["LineItem"] = Relationship(back_populates="invoice")
    budget_ledgers: List["BudgetLedger"] = Relationship(back_populates="invoice")
    audit_logs: List["AuditLog"] = Relationship(back_populates="invoice")


# 3. Input Schema (used when a client creates an invoice — no invoice_id needed)
class InvoiceCreate(InvoiceBase):
    pass


# 4. Response Schema (used when returning data to the client)
class InvoiceRead(InvoiceBase):
    invoice_id: int
