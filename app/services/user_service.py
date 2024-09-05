from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.core.security import hash_password,verify_password
from fastapi import HTTPException
from app.auth import jwt
from app.schemas.schema import GetToken



async def create_user(db: AsyncSession, username: str, email: str, password: str):
    try:
        hashed_pwd = hash_password(password)
        user = User(username=username, email=email, hashed_password=hashed_pwd)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        print("error time",e)
        raise HTTPException(status_code=400,detail="Something went wrong")


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    return user


async def get_all_users(db: AsyncSession ):
    result = await db.execute(select(User))
    return result.scalars().all()


async def login(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        print("no usr")
        raise HTTPException(status_code=401,detail="Email is incorrect")
    isPassword = verify_password(password,user.hashed_password)
    if not isPassword:
        raise HTTPException(status_code=401,detail="Password is incorrect")
    token = jwt.create_access_token({"username": user.username,"id":user.id})
    return GetToken(access_token=token)
