"""Firm CRUD routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.firm import Firm, FirmCreate, FirmRead


router = APIRouter(prefix="/firms", tags=["firms"])


class FirmUpdate(FirmCreate):
    """Optional fields for full/partial firm updates."""

    name: str | None = None
    contact_email: str | None = None
    status: str | None = None


@router.get(
    "/",
    response_model=List[FirmRead],
    summary="List all firms",
)
async def list_firms(
    session: AsyncSession = Depends(get_session),
) -> List[Firm]:
    """Return every firm in the database."""
    result = await session.execute(select(Firm))
    return result.scalars().all()


@router.get(
    "/{firm_id}",
    response_model=FirmRead,
    summary="Get a single firm by ID",
)
async def get_firm(
    firm_id: int,
    session: AsyncSession = Depends(get_session),
) -> Firm:
    """Return the firm matching the supplied ID."""
    firm = await session.get(Firm, firm_id)
    if not firm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Firm with id {firm_id} not found.",
        )
    return firm


@router.post(
    "/",
    response_model=FirmRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new firm",
)
async def create_firm(
    firm_in: FirmCreate,
    session: AsyncSession = Depends(get_session),
) -> Firm:
    """Create and persist a new firm record."""
    firm = Firm.model_validate(firm_in)
    session.add(firm)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A firm with this information already exists.",
        ) from exc
    await session.refresh(firm)
    return firm


@router.put(
    "/{firm_id}",
    response_model=FirmRead,
    summary="Update an existing firm",
)
async def update_firm(
    firm_id: int,
    firm_in: FirmUpdate,
    session: AsyncSession = Depends(get_session),
) -> Firm:
    """Update a firm's fields. Only supplied fields are changed."""
    firm = await session.get(Firm, firm_id)
    if not firm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Firm with id {firm_id} not found.",
        )

    update_data = firm_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(firm, key, value)

    session.add(firm)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Update conflicts with an existing firm.",
        ) from exc
    await session.refresh(firm)
    return firm


@router.delete(
    "/{firm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a firm",
)
async def delete_firm(
    firm_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Remove the firm matching the supplied ID."""
    firm = await session.get(Firm, firm_id)
    if not firm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Firm with id {firm_id} not found.",
        )

    await session.delete(firm)
    await session.commit()
