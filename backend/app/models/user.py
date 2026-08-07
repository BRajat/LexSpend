from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class UserBase(SQLModel):
    name: str
    email: str
    password_hash: str
    role: str
    firm_id: Optional[int] = None


# 2. Database Table Model (maps to SQL table)
class User(UserBase, table=True):
    __tablename__ = "user"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)

    firm_id: Optional[int] = Field(default=None, foreign_key="firm.firm_id")
    firm: Optional["Firm"] = Relationship(back_populates="users")
    audit_logs: List["AuditLog"] = Relationship(back_populates="user")


# 3. Input Schema (used when a client creates a user — no user_id needed)
class UserCreate(UserBase):
    pass


# 4. Response Schema (used when returning data to the client)
class UserRead(UserBase):
    user_id: int
