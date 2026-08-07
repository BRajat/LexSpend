"""Alert CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.alert import Alert, AlertCreate, AlertRead


router = APIRouter(prefix="/alerts", tags=["alerts"])


class AlertUpdate(AlertCreate):
    budget_id: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[str] = None


@router.get("/", response_model=List[AlertRead], summary="List all alerts")
async def list_alerts(session: AsyncSession = Depends(get_session)) -> List[Alert]:
    result = await session.execute(select(Alert))
    return result.scalars().all()


@router.get("/{alert_id}", response_model=AlertRead, summary="Get a single alert by ID")
async def get_alert(alert_id: int, session: AsyncSession = Depends(get_session)) -> Alert:
    alert = await session.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert with id {alert_id} not found.")
    return alert


@router.post("/", response_model=AlertRead, status_code=status.HTTP_201_CREATED, summary="Create a new alert")
async def create_alert(alert_in: AlertCreate, session: AsyncSession = Depends(get_session)) -> Alert:
    alert = Alert.model_validate(alert_in)
    session.add(alert)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create alert.") from exc
    await session.refresh(alert)
    return alert


@router.put("/{alert_id}", response_model=AlertRead, summary="Update an existing alert")
async def update_alert(alert_id: int, alert_in: AlertUpdate, session: AsyncSession = Depends(get_session)) -> Alert:
    alert = await session.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert with id {alert_id} not found.")

    update_data = alert_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(alert, key, value)

    session.add(alert)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update alert.") from exc
    await session.refresh(alert)
    return alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an alert")
async def delete_alert(alert_id: int, session: AsyncSession = Depends(get_session)) -> None:
    alert = await session.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert with id {alert_id} not found.")
    await session.delete(alert)
    await session.commit()
