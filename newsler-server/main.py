from typing import Union
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI
from .routers import everything, articles, auth, edu
import os
import asyncio
from .db import init

app = FastAPI()
app.include_router(everything.router)
app.include_router(articles.router)
app.include_router(auth.router)
app.include_router(edu.router)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
