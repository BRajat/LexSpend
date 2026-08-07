from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class MatterBase(SQLModel):
    firm_id: int
    name: str
    owner: str
    status: str = "open"


# 2. Database Table Model (maps to SQL table)
class Matter(MatterBase, table=True):
    __tablename__ = "matter"
    matter_id: Optional[int] = Field(default=None, primary_key=True)
    firm_id: int = Field(foreign_key="firm.firm_id")

    firm: Optional["Firm"] = Relationship(back_populates="matters")
    budget: Optional["Budget"] = Relationship(
        back_populates="matter", sa_relationship_kwargs={"uselist": False}
    )
    invoices: List["Invoice"] = Relationship(back_populates="matter")


# 3. Input Schema (used when a client creates a matter — no matter_id needed)
class MatterCreate(MatterBase):
    pass


# 4. Response Schema (used when returning data to the client)
class MatterRead(MatterBase):
    matter_id: int
