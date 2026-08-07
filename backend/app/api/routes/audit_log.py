"""Audit log CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.audit_log import AuditLog, AuditLogCreate, AuditLogRead


router = APIRouter(prefix="/audit-logs", tags=["audit_logs"])


class AuditLogUpdate(AuditLogCreate):
    invoice_id: Optional[int] = None
    user_id: Optional[int] = None
    action: Optional[str] = None
    notes: Optional[str] = None
    timestamp: Optional[str] = None


@router.get("/", response_model=List[AuditLogRead], summary="List all audit logs")
async def list_audit_logs(session: AsyncSession = Depends(get_session)) -> List[AuditLog]:
    result = await session.execute(select(AuditLog))
    return result.scalars().all()


@router.get("/{log_id}", response_model=AuditLogRead, summary="Get a single audit log by ID")
async def get_audit_log(log_id: int, session: AsyncSession = Depends(get_session)) -> AuditLog:
    audit_log = await session.get(AuditLog, log_id)
    if not audit_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Audit log with id {log_id} not found.")
    return audit_log


@router.post("/", response_model=AuditLogRead, status_code=status.HTTP_201_CREATED, summary="Create a new audit log")
async def create_audit_log(audit_log_in: AuditLogCreate, session: AsyncSession = Depends(get_session)) -> AuditLog:
    audit_log = AuditLog.model_validate(audit_log_in)
    session.add(audit_log)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create audit log.") from exc
    await session.refresh(audit_log)
    return audit_log


@router.put("/{log_id}", response_model=AuditLogRead, summary="Update an existing audit log")
async def update_audit_log(log_id: int, audit_log_in: AuditLogUpdate, session: AsyncSession = Depends(get_session)) -> AuditLog:
    audit_log = await session.get(AuditLog, log_id)
    if not audit_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Audit log with id {log_id} not found.")

    update_data = audit_log_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(audit_log, key, value)

    session.add(audit_log)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update audit log.") from exc
    await session.refresh(audit_log)
    return audit_log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an audit log")
async def delete_audit_log(log_id: int, session: AsyncSession = Depends(get_session)) -> None:
    audit_log = await session.get(AuditLog, log_id)
    if not audit_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Audit log with id {log_id} not found.")
    await session.delete(audit_log)
    await session.commit()
