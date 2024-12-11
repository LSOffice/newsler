from datetime import datetime, timezone, timedelta
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request
import bcrypt
from pydantic import BaseModel
import asyncio

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)


class Feed(BaseModel):
    user_id: str | None = None


class Credentials(BaseModel):
    email: str | None = None
    password: str | None = None


pw = b"Luciano#1977"
salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()
hashed = bcrypt.hashpw(pw, salt)
print(hashed)

sample_users_db = {
    "56754323456": {
        "email": "luciano.suen@gmail.com",
        "password": "$2b$12$FEkXT67TEFPCA9p5tAuQRun0BXWvgWet.R4bNdyaMnFi6ar49fUA6",
    }
}

sample_sessions_db = {}

sample_interactions_db = {
    # user id
    "56754323456": {
        # article id
        "12345": [
            {"type": "view", "timestamp": int(datetime.now().timestamp())},
            {
                "type": "reaction",
                "reaction_sentiment": 1.0,
                "timestamp": int(datetime.now().timestamp()),
            },
        ],
        "1234": [
            {"type": "save", "timestamp": int(datetime.now().timestamp())},
        ],
    }
}


async def rank_interactions(interactions: list):
    for interaction in interactions:
        pass


async def is_logged_in(req: Request) -> list:
    try:
        session_token = req.headers["Authorization"]
    except KeyError:
        return [False, False]

    session_token = session_token.replace("Bearer ", "")
    hashed_session_token = bcrypt.hashpw(session_token.encode(), salt)
    for user_id in sample_sessions_db:
        if (
            sample_sessions_db[user_id]["session_token"]
            == hashed_session_token.decode()
        ):
            if datetime.now().timestamp() >= int(
                sample_sessions_db[user_id]["sessionExpiresAt"]
            ):
                return [True, False]
            return [True, True]
    # Has account, invalid credentials
    return [True, False]


@router.post("/")
async def get():
    b = await recent_x_articles_interacted_with_ranked("56754323456", 10)
    print(b)


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
