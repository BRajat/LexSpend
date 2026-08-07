"""Line item CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.line_item import LineItem, LineItemCreate, LineItemRead


router = APIRouter(prefix="/line-items", tags=["line_items"])


class LineItemUpdate(LineItemCreate):
    invoice_id: Optional[int] = None
    timekeeper: Optional[str] = None
    hours: Optional[float] = None
    rate: Optional[float] = None
    amount: Optional[float] = None


@router.get("/", response_model=List[LineItemRead], summary="List all line items")
async def list_line_items(session: AsyncSession = Depends(get_session)) -> List[LineItem]:
    result = await session.execute(select(LineItem))
    return result.scalars().all()


@router.get("/{line_item_id}", response_model=LineItemRead, summary="Get a single line item by ID")
async def get_line_item(line_item_id: int, session: AsyncSession = Depends(get_session)) -> LineItem:
    line_item = await session.get(LineItem, line_item_id)
    if not line_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Line item with id {line_item_id} not found.")
    return line_item


@router.post("/", response_model=LineItemRead, status_code=status.HTTP_201_CREATED, summary="Create a new line item")
async def create_line_item(line_item_in: LineItemCreate, session: AsyncSession = Depends(get_session)) -> LineItem:
    line_item = LineItem.model_validate(line_item_in)
    session.add(line_item)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create line item.") from exc
    await session.refresh(line_item)
    return line_item


@router.put("/{line_item_id}", response_model=LineItemRead, summary="Update an existing line item")
async def update_line_item(line_item_id: int, line_item_in: LineItemUpdate, session: AsyncSession = Depends(get_session)) -> LineItem:
    line_item = await session.get(LineItem, line_item_id)
    if not line_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Line item with id {line_item_id} not found.")

    update_data = line_item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(line_item, key, value)

    session.add(line_item)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update line item.") from exc
    await session.refresh(line_item)
    return line_item


@router.delete("/{line_item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a line item")
async def delete_line_item(line_item_id: int, session: AsyncSession = Depends(get_session)) -> None:
    line_item = await session.get(LineItem, line_item_id)
    if not line_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Line item with id {line_item_id} not found.")
    await session.delete(line_item)
    await session.commit()
