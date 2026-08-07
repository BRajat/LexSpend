"""User CRUD routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.user import User, UserCreate, UserRead


router = APIRouter(prefix="/users", tags=["users"])


class UserUpdate(UserCreate):
    name: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    firm_id: Optional[int] = None


@router.get("/", response_model=List[UserRead], summary="List all users")
async def list_users(session: AsyncSession = Depends(get_session)) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserRead, summary="Get a single user by ID")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> User:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Create a new user")
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    user = User.model_validate(user_in)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create user.") from exc
    await session.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserRead, summary="Update an existing user")
async def update_user(user_id: int, user_in: UserUpdate, session: AsyncSession = Depends(get_session)) -> User:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update user.") from exc
    await session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)) -> None:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
    await session.delete(user)
    await session.commit()
