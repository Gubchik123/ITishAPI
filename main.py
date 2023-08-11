from fastapi import FastAPI

from db import Base, engine
from blog.router import blog_router
from user.router import user_router
from auth.router import auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ITish API",
    description="API for ITish blog site",
    version="1.0.0",
)

app.include_router(blog_router, prefix="/api/blog", tags=["blog"])
app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
