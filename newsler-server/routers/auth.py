from datetime import datetime, timezone, timedelta
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request
import bcrypt
from pydantic import BaseModel
import asyncio
from ..db.init import (
    auth_create_session,
    auth_create_user,
    auth_search_user_by_username,
)
import re

salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


class Credentials(BaseModel):
    email: str | None = None
    password: str | None = None


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


async def is_email_used(email: str | None):
    users = auth_search_user_by_username({"username": email})

    if len(users) > 0:
        return {"result": True, "user_id": users[0][0]}
    else:
        return {"result": False}


@router.post("/login")
async def login(login: Credentials):
    print(auth_get_session({}))
    return {}
    if login.email == None or login.password == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    result = await is_email_used(login.email)
    if not result["result"]:
        raise HTTPException(status_code=401, detail="Not authorised")
    user_id = result["user_id"]
    if (
        not bcrypt.hashpw(login.password.encode(), salt).decode()
        == sample_users_db[str(user_id)]["password"]
    ):
        raise HTTPException(status_code=401, detail="Not authorised")

    session_token = str(uuid4())
    refresh_token = str(uuid4())

    time_now = datetime.now().timestamp()
    sample_sessions_db[str(user_id)] = {
        "refresh_token": bcrypt.hashpw(refresh_token.encode(), salt).decode(),
        "refreshExpiresAt": str(int(time_now) + 120 * 86400),
        "session_token": bcrypt.hashpw(session_token.encode(), salt).decode(),
        "sessionExpiresAt": str(int(time_now) + 15 * 60),
    }

    return {"refresh_token": refresh_token, "session_token": session_token}


@router.post("/signup")
async def signup(signupInfo: Credentials):
    if signupInfo.email == None or signupInfo.password == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    result = await is_email_used(signupInfo.email)

    if result["result"]:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not len(signupInfo.password) >= 8:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    password_hashed = bcrypt.hashpw(signupInfo.password.encode(), salt)

    if not re.fullmatch(
        re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"),
        signupInfo.email,
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user_id = auth_create_user({"email": signupInfo.email, "password": password_hashed})

    session_token = str(uuid4())
    refresh_token = str(uuid4())

    time_now = datetime.now().timestamp()
    refresh_token, session_token = auth_create_session(
        {
            "user_id": user_id,
            "refresh_token": bcrypt.hashpw(refresh_token.encode(), salt).decode(),
            "refreshExpiresAt": int(time_now) + 120 * 86400,
            "session_token": bcrypt.hashpw(session_token.encode(), salt).decode(),
            "sessionExpiresAt": int(time_now) + 15 * 60,
        }
    )

    return {
        "signup": True,
        "refresh_token": refresh_token,
        "session_token": session_token,
    }
