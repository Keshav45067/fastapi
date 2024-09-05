from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema import UserCreate, UserRead, GetToken,Login
from app.services.user_service import create_user, get_user_by_username, get_all_users,login
from app.db.session import get_db
from app.auth.jwt import verify_access_token,create_access_token
router = APIRouter()


@router.post("/users/", response_model=UserRead)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user(db, user.username, user.email, user.password)


@router.get("/users/", response_model=List[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)


@router.post("/users/login")
async def login_route(user: Login, db: AsyncSession = Depends(get_db)):
    return await login(db, user.email, user.password)