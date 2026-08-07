from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


# 1. Shared base fields (no database table, used for inheritance)
class AuditLogBase(SQLModel):
    invoice_id: Optional[int] = None
    user_id: Optional[int] = None
    action: str
    notes: Optional[str] = None
    timestamp: str


# 2. Database Table Model (maps to SQL table)
class AuditLog(AuditLogBase, table=True):
    __tablename__ = "audit_log"
    log_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    invoice_id: int = Field(foreign_key="invoice.invoice_id")
    invoice: Optional["Invoice"] = Relationship(back_populates="audit_logs")
    user: Optional["User"] = Relationship(back_populates="audit_logs")


# 3. Input Schema (used when a client creates an audit log — no log_id needed)
class AuditLogCreate(AuditLogBase):
    pass


# 4. Response Schema (used when returning data to the client)
class AuditLogRead(AuditLogBase):
    log_id: int
