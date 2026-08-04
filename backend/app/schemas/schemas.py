from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


class UUIDModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


# ---------------------------------------------------------------------------
# Firm
# ---------------------------------------------------------------------------


class FirmBase(BaseModel):
    name: str
    domain: str | None = None


class FirmCreate(FirmBase):
    pass


class FirmRead(UUIDModel, FirmBase):
    created_at: datetime


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    firm_id: uuid.UUID | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UUIDModel, UserBase):
    is_active: bool
    created_at: datetime


# ---------------------------------------------------------------------------
# Matter
# ---------------------------------------------------------------------------


class MatterBase(BaseModel):
    matter_number: str
    description: str | None = None
    budget: Decimal | None = None
    is_open: bool = True


class MatterCreate(MatterBase):
    firm_id: uuid.UUID


class MatterRead(UUIDModel, MatterBase):
    firm_id: uuid.UUID
    created_at: datetime


# ---------------------------------------------------------------------------
# Invoice line item
# ---------------------------------------------------------------------------


class LineItemBase(BaseModel):
    timekeeper: str | None = None
    date: datetime | None = None
    description: str | None = None
    hours: Decimal | None = None
    rate: Decimal | None = None
    amount: Decimal | None = None
    task_code: str | None = None
    activity_code: str | None = None
    sort_order: int = 0


class LineItemCreate(LineItemBase):
    pass


class LineItemRead(UUIDModel, LineItemBase):
    invoice_id: uuid.UUID


# ---------------------------------------------------------------------------
# Invoice
# ---------------------------------------------------------------------------


class InvoiceBase(BaseModel):
    invoice_number: str | None = None
    invoice_date: datetime | None = None
    total_amount: Decimal | None = None
    currency: str = "USD"
    matter_id: uuid.UUID | None = None


class InvoiceCreate(InvoiceBase):
    firm_id: uuid.UUID


class InvoiceRead(UUIDModel, InvoiceBase):
    firm_id: uuid.UUID
    status: str
    ai_extracted: bool
    created_at: datetime
    updated_at: datetime
    line_items: list[LineItemRead] = []


# ---------------------------------------------------------------------------
# PDF parse request / response
# ---------------------------------------------------------------------------


class ParsedInvoice(BaseModel):
    """Structured output produced by the AI PDF extraction pipeline."""

    invoice_number: str | None = Field(None, description="Invoice number or reference")
    invoice_date: str | None = Field(None, description="Invoice date (ISO 8601)")
    vendor_name: str | None = Field(None, description="Law firm / vendor name")
    matter_number: str | None = Field(None, description="Matter or engagement number")
    total_amount: Decimal | None = Field(None, description="Total billed amount")
    currency: str = Field("USD", description="Three-letter currency code")
    line_items: list[LineItemCreate] = Field(
        default_factory=list, description="Individual billing line items"
    )


class ParsePDFResponse(BaseModel):
    parsed: ParsedInvoice
    raw_text_preview: str = Field(
        "", description="First 500 characters of extracted PDF text"
    )
