"""Budget CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.budget import Budget, BudgetCreate, BudgetRead


router = APIRouter(prefix="/budgets", tags=["budgets"])


class BudgetUpdate(BudgetCreate):
    matter_id: Optional[int] = None
    allocated_amt: Optional[float] = None
    threshold_pct: Optional[float] = None


@router.get("/", response_model=List[BudgetRead], summary="List all budgets")
async def list_budgets(session: AsyncSession = Depends(get_session)) -> List[Budget]:
    result = await session.execute(select(Budget))
    return result.scalars().all()


@router.get("/{budget_id}", response_model=BudgetRead, summary="Get a single budget by ID")
async def get_budget(budget_id: int, session: AsyncSession = Depends(get_session)) -> Budget:
    budget = await session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget with id {budget_id} not found.")
    return budget


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED, summary="Create a new budget")
async def create_budget(budget_in: BudgetCreate, session: AsyncSession = Depends(get_session)) -> Budget:
    budget = Budget.model_validate(budget_in)
    session.add(budget)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create budget.") from exc
    await session.refresh(budget)
    return budget


@router.put("/{budget_id}", response_model=BudgetRead, summary="Update an existing budget")
async def update_budget(budget_id: int, budget_in: BudgetUpdate, session: AsyncSession = Depends(get_session)) -> Budget:
    budget = await session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget with id {budget_id} not found.")

    update_data = budget_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(budget, key, value)

    session.add(budget)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update budget.") from exc
    await session.refresh(budget)
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a budget")
async def delete_budget(budget_id: int, session: AsyncSession = Depends(get_session)) -> None:
    budget = await session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget with id {budget_id} not found.")
    await session.delete(budget)
    await session.commit()
