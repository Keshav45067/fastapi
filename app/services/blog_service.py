from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.blog import Blog
from fastapi import HTTPException, status
from app.schemas.schema import BlogRead, BlogCreate
from sqlalchemy.orm import selectinload
from app.auth.jwt import verify_access_token


async def create_blog(db: AsyncSession, title: str, content: str, authorization):
    try:
        if authorization is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token = authorization.split(" ")[1]
        payload = verify_access_token(token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        owner_id = payload["id"]
        blog = Blog(title=title, content=content, owner_id=owner_id)
        db.add(blog)
        await db.commit()
        await db.refresh(blog)
        return blog
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create blog")


async def get_blog(db: AsyncSession, blog_id: int, authorization):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    result = await db.execute(select(Blog).options(selectinload(Blog.owner)).filter(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


async def update_blog(db : AsyncSession, new_blog: BlogRead, id:int, authorization):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_blog = await db.execute(select(Blog).filter(Blog.id == id))
    blog = db_blog.scalar_one_or_none()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db_blog.title = new_blog.title
    db_blog.content = new_blog.content
    await db.commit()
    return new_blog


async def delete_blog(db:AsyncSession,id:int, authorization):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_blog = await db.execute(select(Blog).filter(Blog.id == id))
    blog = db_blog.scalar_one_or_none()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    await db.delete(blog)
    await db.commit()
    return {"data": "Deleted successfully"}
