from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class FirmBase(SQLModel):
    name: str
    contact_email: Optional[str] = None
    status: str = "active"


# 2. Database Table Model (maps to SQL table)
class Firm(FirmBase, table=True):
    __tablename__ = "firm"
    firm_id: Optional[int] = Field(default=None, primary_key=True)

    matters: List["Matter"] = Relationship(back_populates="firm")
    users: List["User"] = Relationship(back_populates="firm")
    invoices: List["Invoice"] = Relationship(back_populates="firm")


# 3. Input Schema (used when a client creates a firm — no firm_id needed)
class FirmCreate(FirmBase):
    pass


# 4. Response Schema (used when returning data to the client)
class FirmRead(FirmBase):
    firm_id: int
