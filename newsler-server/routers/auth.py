import asyncio
import re
from datetime import datetime, timedelta, timezone
from http import client
from uuid import uuid4

import bcrypt
import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..db.init import (
    auth_create_session,
    auth_create_user,
    auth_create_user_recommendation_index,
    auth_get_session_from_user_id,
    auth_return_user_object_from_user_id,
    auth_search_user_by_username,
    auth_update_user_recommendation_index,
    auth_update_user_session,
    auth_update_user_session_token_only,
)

salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # responses={404: {"description": "Not found"}},
)


class Credentials(BaseModel):
    email: str | None = None
    password: str | None = None


class SessionRefresh(BaseModel):
    refresh_token: str | None = None
    user_id: str | None = None


"""
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
    return [True, False]"""


async def is_email_used(email: str | None):
    users = auth_search_user_by_username({"username": email})

    if len(users) > 0:
        return {"result": True, "user_id": users[0][0]}
    else:
        return {"result": False}


@router.post("/refreshsession")
async def refresh_session(refreshCredentials: SessionRefresh):
    if refreshCredentials.refresh_token == None or refreshCredentials.user_id == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    cur_session = auth_get_session_from_user_id({"user_id": refreshCredentials.user_id})
    if not cur_session[0]:
        # if session doesn't exist with user
        raise HTTPException(status_code=308, detail="Redirect /login")

    session_info = cur_session[1]
    if (
        not bcrypt.hashpw(refreshCredentials.refresh_token.encode(), salt).decode()
        == session_info[1]
    ):
        # Incorrect refresh token
        raise HTTPException(status_code=308, detail="Redirect /login")

    if datetime.now() >= datetime.fromtimestamp(session_info[2]):
        # if past refresh expire deadline
        raise HTTPException(status_code=308, detail="Redirect /login")

    session_token = str(uuid4())
    auth_update_user_session_token_only(
        {
            "session_token": bcrypt.hashpw(session_token.encode(), salt).decode(),
            "sessionExpiresAt": int(datetime.now().timestamp()) + 15 * 60,
            "user_id": refreshCredentials.user_id,
        }
    )

    return {
        "session_token": session_token,
        "email": auth_return_user_object_from_user_id(
            {"user_id": refreshCredentials.user_id}
        )[1],
    }


# TODO: Can add inner join here (session and user data, if necessary)
@router.post("/login")
async def login(login: Credentials, request: Request):
    if login.email == None or login.password == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    result = await is_email_used(login.email)
    if not result["result"]:
        raise HTTPException(status_code=401, detail="Not authorised")
    user_id = result["user_id"]
    user_obj = auth_return_user_object_from_user_id({"user_id": user_id})
    # 5 object array returned (in key order)
    if (
        not bcrypt.hashpw(login.password.encode(), salt).decode()
        == user_obj[3]  # password
    ):
        raise HTTPException(status_code=401, detail="Not authorised")

    cur_session = auth_get_session_from_user_id({"user_id": user_id})
    time_now = datetime.now().timestamp()
    if cur_session[0]:
        # if current session exists
        session_token = str(uuid4())
        refresh_token = str(uuid4())

        auth_update_user_session(
            {
                "refresh_token": bcrypt.hashpw(refresh_token.encode(), salt).decode(),
                "refreshExpiresAt": int(time_now) + 120 * 86400,
                "session_token": bcrypt.hashpw(session_token.encode(), salt).decode(),
                "sessionExpiresAt": int(time_now) + 15 * 60,
                "user_id": user_id,
            }
        )
    else:
        # if session doesn't exist already, it goes here
        session_token = str(uuid4())
        refresh_token = str(uuid4())
        auth_create_session(
            {
                "user_id": user_id,
                "refresh_token": bcrypt.hashpw(refresh_token.encode(), salt).decode(),
                "refreshExpiresAt": int(time_now) + 120 * 86400,
                "session_token": bcrypt.hashpw(session_token.encode(), salt).decode(),
                "sessionExpiresAt": int(time_now) + 15 * 60,
            }
        )

    # client_host = request.client.host
    client_host = "170.171.1.12"
    response = requests.get(
        "https://geolocation-db.com/json/" + client_host + "&position=true"
    ).json()
    auth_update_user_recommendation_index(
        {
            "user_id": user_id,
            "device_type": "iOS",
            "geolocation": str(response["latitude"])
            + ", "
            + str(response["longitude"]),
        }
    )

    return {
        "refresh_token": refresh_token,
        "session_token": session_token,
        "user_id": user_id,
        "email": login.email,
    }


@router.post("/signup")
async def signup(signupInfo: Credentials, request: Request):
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

    # client_host = request.client.host
    client_host = "170.171.1.12"

    response = requests.get(
        "https://geolocation-db.com/json/" + client_host + "&position=true"
    ).json()
    country_code = response["country_code"]

    user_id = auth_create_user(
        {
            "email": signupInfo.email,
            "password": password_hashed,
            "country": country_code,
        }
    )

    latitude = (
        response["latitude"] if response["latitude"] != "Not found" else "22.3193"
    )

    longitude = (
        response["longitude"] if response["longitude"] != "Not found" else "114.1694"
    )

    auth_create_user_recommendation_index(
        # hard coded to iOS because it is an iOS exclusive app
        {
            "user_id": user_id,
            "device_type": "iOS",
            "geolocation": str(latitude) + ", " + str(longitude),
        }
    )

    return {"signup": True, "user_id": user_id}
