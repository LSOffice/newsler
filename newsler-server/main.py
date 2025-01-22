import asyncio
import os
from typing import Union

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .db import init
from .routers import articles, auth, edu

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(articles.router)
app.include_router(auth.router)
app.include_router(edu.router)
