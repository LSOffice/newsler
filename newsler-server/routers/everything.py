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


async def recent_x_articles_interacted_with_ranked(user_id: str, x: int) -> list:
    if not str(user_id) in sample_interactions_db:
        return []
    reaction_weighting = 0.7
    view_weighting = 0.1
    full_scroll_weighting = 0.5
    comment_weighting = 0.7
    saved_weighting = 0.97

    user_interaction_db = sample_interactions_db[str(user_id)]
    articles = []
    for article_id in user_interaction_db:
        recency_factor = 14  # days, how many days is considered recent
        total_weighting = 0

        for interaction in user_interaction_db[str(article_id)]:

            if interaction["timestamp"] >= datetime.now().timestamp() - 1209600:
                if interaction["type"] == "view":
                    total_weighting += view_weighting
                elif interaction["type"] == "full_scroll":
                    total_weighting += full_scroll_weighting
                elif interaction["type"] == "comment":
                    total_weighting += comment_weighting
                elif interaction["type"] == "reaction":
                    if interaction["reaction_sentiment"] > 0:
                        total_weighting += reaction_weighting
                elif interaction["type"] == "save":
                    total_weighting += saved_weighting
        if total_weighting != 0:
            articles.append(
                {"articleId": str(article_id), "weighting": total_weighting}
            )

    return sorted(articles, key=lambda d: d["weighting"], reverse=True)


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


@router.get("/feed")
async def feed(body: Feed, auth_headers: list = Depends(is_logged_in)):
    user_id = body.user_id
    if not auth_headers[1]:
        raise HTTPException(status_code=401, detail="Redirect /login")
    if not auth_headers[0]:
        raise HTTPException(status_code=401, detail="Redirect /signup")
    if user_id == None:
        raise HTTPException(status_code=400, detail="Invalid user id")


@router.get("/headers")
async def headers(body: Feed, auth_headers: list = Depends(is_logged_in)):
    user_id = body.user_id
    if not auth_headers[1]:
        raise HTTPException(status_code=401, detail="Redirect /login")
    if not auth_headers[0]:
        raise HTTPException(status_code=401, detail="Redirect /signup")
    if user_id == None:
        raise HTTPException(status_code=400, detail="Invalid user id")


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
