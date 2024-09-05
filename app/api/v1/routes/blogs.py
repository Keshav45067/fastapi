
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.schemas.schema import BlogCreate, BlogRead
from app.services.blog_service import create_blog, get_blog,update_blog, delete_blog
from app.db.session import get_db

router = APIRouter()


@router.post('/blogs', response_model=BlogCreate)
async def create_blog_route( blog: BlogCreate, db: AsyncSession = Depends(get_db),authorization:Optional[str] = Header(None)):
    return await create_blog(db, blog.title,blog.content, authorization)


@router.get("/blogs/{id}", response_model=BlogRead)
async def get_blog_route(id:int, db : AsyncSession = Depends(get_db),authorization:Optional[str] = Header(None)):
    return await get_blog(db, id,authorization)

@router.put("/blogs/{id}", response_model=BlogRead)
async def update_blog_route( id:int, request: BlogRead, db: AsyncSession = Depends(get_db),authorization:Optional[str] = Header(None)):
    return await update_blog(db , request, id,authorization)

@router.delete("/blogs/{id}")
async def delete_blog_route( id:int, db: AsyncSession = Depends(get_db),authorization:Optional[str] = Header(None)):
    return await delete_blog(db,id,authorization)