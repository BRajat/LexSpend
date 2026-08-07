from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class LineItemBase(SQLModel):
    invoice_id: int
    timekeeper: Optional[str] = None
    hours: Optional[float] = None
    rate: Optional[float] = None
    amount: float


# 2. Database Table Model (maps to SQL table)
class LineItem(LineItemBase, table=True):
    __tablename__ = "line_item"
    line_item_id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoice.invoice_id")
    invoice: Optional["Invoice"] = Relationship(back_populates="line_items")


# 3. Input Schema (used when a client creates a line item — no line_item_id needed)
class LineItemCreate(LineItemBase):
    pass


# 4. Response Schema (used when returning data to the client)
class LineItemRead(LineItemBase):
    line_item_id: int
