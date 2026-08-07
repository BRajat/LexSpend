"""Budget ledger CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.budget_ledger import BudgetLedger, BudgetLedgerCreate, BudgetLedgerRead


router = APIRouter(prefix="/budget-ledgers", tags=["budget_ledgers"])


class BudgetLedgerUpdate(BudgetLedgerCreate):
    budget_id: Optional[int] = None
    invoice_id: Optional[int] = None
    amount: Optional[float] = None
    entry_type: Optional[str] = None
    created_at: Optional[str] = None


@router.get("/", response_model=List[BudgetLedgerRead], summary="List all budget ledger entries")
async def list_budget_ledgers(session: AsyncSession = Depends(get_session)) -> List[BudgetLedger]:
    result = await session.execute(select(BudgetLedger))
    return result.scalars().all()


@router.get("/{ledger_id}", response_model=BudgetLedgerRead, summary="Get a single budget ledger entry by ID")
async def get_budget_ledger(ledger_id: int, session: AsyncSession = Depends(get_session)) -> BudgetLedger:
    ledger = await session.get(BudgetLedger, ledger_id)
    if not ledger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget ledger entry with id {ledger_id} not found.")
    return ledger


@router.post("/", response_model=BudgetLedgerRead, status_code=status.HTTP_201_CREATED, summary="Create a new budget ledger entry")
async def create_budget_ledger(ledger_in: BudgetLedgerCreate, session: AsyncSession = Depends(get_session)) -> BudgetLedger:
    ledger = BudgetLedger.model_validate(ledger_in)
    session.add(ledger)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create budget ledger entry.") from exc
    await session.refresh(ledger)
    return ledger


@router.put("/{ledger_id}", response_model=BudgetLedgerRead, summary="Update an existing budget ledger entry")
async def update_budget_ledger(ledger_id: int, ledger_in: BudgetLedgerUpdate, session: AsyncSession = Depends(get_session)) -> BudgetLedger:
    ledger = await session.get(BudgetLedger, ledger_id)
    if not ledger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget ledger entry with id {ledger_id} not found.")

    update_data = ledger_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ledger, key, value)

    session.add(ledger)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update budget ledger entry.") from exc
    await session.refresh(ledger)
    return ledger


@router.delete("/{ledger_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a budget ledger entry")
async def delete_budget_ledger(ledger_id: int, session: AsyncSession = Depends(get_session)) -> None:
    ledger = await session.get(BudgetLedger, ledger_id)
    if not ledger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget ledger entry with id {ledger_id} not found.")
    await session.delete(ledger)
    await session.commit()
