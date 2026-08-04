import uuid
import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class InvoiceStatus(str, enum.Enum):
    pending = "pending"
    reviewed = "reviewed"
    approved = "approved"
    disputed = "disputed"
    paid = "paid"


class AuditAction(str, enum.Enum):
    create = "create"
    update = "update"
    delete = "delete"
    approve = "approve"
    dispute = "dispute"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class Firm(Base):
    """Law firm / vendor organisation."""

    __tablename__ = "firms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    users: Mapped[list["User"]] = relationship("User", back_populates="firm")
    matters: Mapped[list["Matter"]] = relationship("Matter", back_populates="firm")
    invoices: Mapped[list["Invoice"]] = relationship("Invoice", back_populates="firm")


class User(Base):
    """Platform user – belongs to one firm (or is an admin)."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    firm_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id", ondelete="SET NULL"), nullable=True
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    firm: Mapped["Firm | None"] = relationship("Firm", back_populates="users")
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="user"
    )


class Matter(Base):
    """Legal matter / engagement."""

    __tablename__ = "matters"
    __table_args__ = (UniqueConstraint("firm_id", "matter_number"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    firm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id", ondelete="CASCADE"), nullable=False
    )
    matter_number: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    budget: Mapped[float | None] = mapped_column(Numeric(15, 2))
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    firm: Mapped["Firm"] = relationship("Firm", back_populates="matters")
    invoices: Mapped[list["Invoice"]] = relationship("Invoice", back_populates="matter")


class Invoice(Base):
    """Invoice submitted by a law firm against a matter."""

    __tablename__ = "invoices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    firm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id", ondelete="CASCADE"), nullable=False
    )
    matter_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("matters.id", ondelete="SET NULL"), nullable=True
    )
    invoice_number: Mapped[str | None] = mapped_column(String(100))
    invoice_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    total_amount: Mapped[float | None] = mapped_column(Numeric(15, 2))
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus), default=InvoiceStatus.pending
    )
    pdf_key: Mapped[str | None] = mapped_column(Text)  # S3 / storage key
    raw_text: Mapped[str | None] = mapped_column(Text)
    ai_extracted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    firm: Mapped["Firm"] = relationship("Firm", back_populates="invoices")
    matter: Mapped["Matter | None"] = relationship("Matter", back_populates="invoices")
    line_items: Mapped[list["InvoiceLineItem"]] = relationship(
        "InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="invoice"
    )


class InvoiceLineItem(Base):
    """Individual billable line within an invoice."""

    __tablename__ = "invoice_line_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
    )
    timekeeper: Mapped[str | None] = mapped_column(String(255))
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    description: Mapped[str | None] = mapped_column(Text)
    hours: Mapped[float | None] = mapped_column(Numeric(8, 2))
    rate: Mapped[float | None] = mapped_column(Numeric(10, 2))
    amount: Mapped[float | None] = mapped_column(Numeric(15, 2))
    task_code: Mapped[str | None] = mapped_column(String(50))
    activity_code: Mapped[str | None] = mapped_column(String(50))
    sort_order: Mapped[int] = mapped_column(BigInteger, default=0)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="line_items")


class AuditLog(Base):
    """Immutable audit trail for invoice state changes."""

    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    invoice_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("invoices.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction), nullable=False)
    details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    invoice: Mapped["Invoice | None"] = relationship(
        "Invoice", back_populates="audit_logs"
    )
    user: Mapped["User | None"] = relationship("User", back_populates="audit_logs")
