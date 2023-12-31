from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(blog_router, prefix="/api/blog", tags=["blog"])
app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
