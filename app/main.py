from fastapi import FastAPI
from app.api.v1.routes import users, blogs
from app import models
from app.db.session import engine

app = FastAPI()

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(blogs.router, prefix="/api/v1", tags=["blogs"])