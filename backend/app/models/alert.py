from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class AlertBase(SQLModel):
    budget_id: int
    type: str
    message: str
    created_at: str


# 2. Database Table Model (maps to SQL table)
class Alert(AlertBase, table=True):
    __tablename__ = "alert"
    alert_id: Optional[int] = Field(default=None, primary_key=True)
    budget_id: int = Field(foreign_key="budget.budget_id")
    budget: Optional["Budget"] = Relationship(back_populates="alerts")


# 3. Input Schema (used when a client creates an alert — no alert_id needed)
class AlertCreate(AlertBase):
    pass


# 4. Response Schema (used when returning data to the client)
class AlertRead(AlertBase):
    alert_id: int
