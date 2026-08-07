"""Matter CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.matter import Matter, MatterCreate, MatterRead


router = APIRouter(prefix="/matters", tags=["matters"])


class MatterUpdate(MatterCreate):
    firm_id: Optional[int] = None
    name: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None


@router.get("/", response_model=List[MatterRead], summary="List all matters")
async def list_matters(session: AsyncSession = Depends(get_session)) -> List[Matter]:
    result = await session.execute(select(Matter))
    return result.scalars().all()


@router.get("/{matter_id}", response_model=MatterRead, summary="Get a single matter by ID")
async def get_matter(matter_id: int, session: AsyncSession = Depends(get_session)) -> Matter:
    matter = await session.get(Matter, matter_id)
    if not matter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Matter with id {matter_id} not found.")
    return matter


@router.post("/", response_model=MatterRead, status_code=status.HTTP_201_CREATED, summary="Create a new matter")
async def create_matter(matter_in: MatterCreate, session: AsyncSession = Depends(get_session)) -> Matter:
    matter = Matter.model_validate(matter_in)
    session.add(matter)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create matter.") from exc
    await session.refresh(matter)
    return matter


@router.put("/{matter_id}", response_model=MatterRead, summary="Update an existing matter")
async def update_matter(matter_id: int, matter_in: MatterUpdate, session: AsyncSession = Depends(get_session)) -> Matter:
    matter = await session.get(Matter, matter_id)
    if not matter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Matter with id {matter_id} not found.")

    update_data = matter_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(matter, key, value)

    session.add(matter)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update matter.") from exc
    await session.refresh(matter)
    return matter


@router.delete("/{matter_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a matter")
async def delete_matter(matter_id: int, session: AsyncSession = Depends(get_session)) -> None:
    matter = await session.get(Matter, matter_id)
    if not matter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Matter with id {matter_id} not found.")
    await session.delete(matter)
    await session.commit()
