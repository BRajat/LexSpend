# this is standalone test file to show how schema validation works
from pydantic import BaseModel, Field
from typing import List, Optional

class LineItemSchema(BaseModel):
    date: Optional[str] = Field(default=None)
    timekeeper_name: Optional[str] = Field(default=None)
    timekeeper_role: Optional[str] = Field(default=None)
    hours: Optional[float] = Field(default=None)
    rate: Optional[float] = Field(default=None)
    line_total: Optional[float] = Field(default=None)
    description: Optional[str] = Field(default=None)

class ParsedInvoice(BaseModel):
    invoice_number: Optional[str] = Field(default=None)
    invoice_date: Optional[str] = Field(default=None)
    billing_address: Optional[str] = Field(default=None)
    client_name: Optional[str] = Field(default=None)
    matter_name: Optional[str] = Field(default=None)
    invoice_total: Optional[float] = Field(default=None)
    line_items: List[LineItemSchema] = Field(default_factory=list)
    timekeeper_entries: Optional[List[dict]] = Field(default_factory=list)
    hours: Optional[float] = Field(default=None)
    rates: Optional[float] = Field(default=None)
    expenses: Optional[List[dict]] = Field(default_factory=list)

# Test payload matching your error case
raw_data = {
    "invoice_number": None,
    "invoice_date": None,
    "billing_address": None,
    "client_name": None,
    "matter_name": None,
    "invoice_total": None,
    "line_items": None,
    "timekeeper_entries": None,
    "hours": None,
    "rates": None,
    "expenses": None
}

if __name__ == "__main__":
    invoice = ParsedInvoice.model_validate(raw_data)
    print("Successfully parsed:", invoice.model_dump())