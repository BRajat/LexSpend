"""Invoice CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.invoice import Invoice, InvoiceCreate, InvoiceRead


router = APIRouter(prefix="/invoices", tags=["invoices"])


class InvoiceUpdate(InvoiceCreate):
    matter_id: Optional[int] = None
    firm_id: Optional[int] = None
    invoice_no: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    confidence_score: Optional[float] = None


@router.get("/", response_model=List[InvoiceRead], summary="List all invoices")
async def list_invoices(session: AsyncSession = Depends(get_session)) -> List[Invoice]:
    result = await session.execute(select(Invoice))
    return result.scalars().all()


@router.get("/{invoice_id}", response_model=InvoiceRead, summary="Get a single invoice by ID")
async def get_invoice(invoice_id: int, session: AsyncSession = Depends(get_session)) -> Invoice:
    invoice = await session.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with id {invoice_id} not found.")
    return invoice


@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED, summary="Create a new invoice")
async def create_invoice(invoice_in: InvoiceCreate, session: AsyncSession = Depends(get_session)) -> Invoice:
    invoice = Invoice.model_validate(invoice_in)
    session.add(invoice)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create invoice.") from exc
    await session.refresh(invoice)
    return invoice


@router.put("/{invoice_id}", response_model=InvoiceRead, summary="Update an existing invoice")
async def update_invoice(invoice_id: int, invoice_in: InvoiceUpdate, session: AsyncSession = Depends(get_session)) -> Invoice:
    invoice = await session.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with id {invoice_id} not found.")

    update_data = invoice_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(invoice, key, value)

    session.add(invoice)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update invoice.") from exc
    await session.refresh(invoice)
    return invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an invoice")
async def delete_invoice(invoice_id: int, session: AsyncSession = Depends(get_session)) -> None:
    invoice = await session.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with id {invoice_id} not found.")
    await session.delete(invoice)
    await session.commit()
