# This file contains the db requests for the authentication sections

import os
import uuid
from datetime import datetime
from tracemalloc import start

import aiomysql
import bcrypt

salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()


# retrieves session from database given a user_id
def get_session_from_user_id(db, query: dict):
    cursor = db.cursor()
    user_id = query["user_id"]

    sql = "SELECT * FROM sessions WHERE user_id=%s "
    cursor.execute(
        sql,
        (user_id,),
    )
    results = cursor.fetchall()
    if len(results) == 0:
        return [False]

    return [True, results[0]]


# checks if session token is valid
async def is_session_token_valid(query: dict):
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        session_token = query["session_token"]

        sql = "SELECT user_id, sessionExpiresAt FROM sessions WHERE session_token=%s"
        await cur.execute(sql, (bcrypt.hashpw(session_token.encode(), salt).decode(),))
        results = await cur.fetchall()
        if len(results) > 0:
            return [
                True,
                datetime.fromtimestamp(results[0][1]) > datetime.now(),
                results[0][0],
            ]
        else:
            return [False]


# updates user session in database
def update_user_session(db, query: dict):
    cursor = db.cursor()

    sql = "UPDATE sessions SET refresh_token=%s, refreshExpiresAt=%s, session_token=%s, sessionExpiresAt=%s WHERE user_id=%s"
    cursor.execute(
        sql,
        (
            query["refresh_token"],
            query["refreshExpiresAt"],
            query["session_token"],
            query["sessionExpiresAt"],
            query["user_id"],
        ),
    )
    db.commit()

    return True


# updates only the session token of a user session
def update_user_session_token_only(db, query: dict):
    cursor = db.cursor()

    sql = "UPDATE sessions SET session_token=%s, sessionExpiresAt=%s WHERE user_id=%s"
    cursor.execute(
        sql,
        (
            query["session_token"],
            query["sessionExpiresAt"],
            query["user_id"],
        ),
    )
    db.commit()

    return True


# creates a new user in the database
def create_user(db, user: dict):
    cursor = db.cursor()
    sql = "INSERT INTO users (user_id, username, type, password, display_name, country) VALUES (%s, %s, %s, %s, %s, %s)"
    user_id = str(uuid.uuid4())

    display_name = user["email"][: user["email"].find("@")]
    # Create display name from email address, parse everything after and incl. @ symbol

    val = (
        user_id,
        user["email"],
        "free",
        user["password"],
        display_name,
        user["country"],
    )
    cursor.execute(sql, val)
    db.commit()

    return user_id


# returns user object from user id
def return_user_object_from_user_id(db, query: dict) -> list:
    if len(list(query.keys())) != 1:
        raise AttributeError("Should not be more than 1 query field")

    field = str(query["user_id"])

    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE user_id=%s "
    cursor.execute(
        sql,
        (field,),
    )
    results = cursor.fetchall()

    return results[0]


# gets user geolocation from database
async def get_user_geolocation(query: dict) -> str:
    if not "user_id" in query:
        raise AttributeError
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT * FROM user_recommendation_index WHERE user_id = %s",
            (query["user_id"],),
        )
        result = await cur.fetchall()
        if len(result) != 1:
            raise AttributeError

        return result[0][2]


# updates user recommendation index in database
def update_user_recommendation_index(db, query: dict):
    cursor = db.cursor()
    if not "user_id" in query:
        raise AttributeError
    sql = "SELECT * FROM user_recommendation_index WHERE user_id=%s"
    cursor.execute(sql, (query["user_id"],))

    results = cursor.fetchall()
    if len(results) != 1:
        raise ValueError

    user_recommendation_index = results[0]
    device_type = query.get("device_type", user_recommendation_index[1])
    geolocation = query.get("geolocation", user_recommendation_index[2])
    topical_interests = query.get("topical_interests", user_recommendation_index[3])
    age = query.get("age", user_recommendation_index[4])
    gender = query.get("gender", user_recommendation_index[5])
    preferred_format = query.get("preferred_format", user_recommendation_index[6])
    sql = "UPDATE user_recommendation_index SET device_type=%s, geolocation=%s, topical_interests=%s, age=%s, gender=%s, preferred_format=%s  WHERE (user_id = %s);"
    val = (
        device_type,
        geolocation,
        topical_interests,
        age,
        gender,
        preferred_format,
        query["user_id"],
    )
    cursor.execute(sql, val)
    db.commit()


# gets user recommendation index from database
async def get_user_recommendation_index(query: dict):
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        sql = "SELECT * FROM user_recommendation_index WHERE user_id=%s"
        await cur.execute(sql, (query["user_id"],))
        result = await cur.fetchone()
        return result


# creates a new user recommendation index in the database
def create_user_recommendation_index(db, query: dict):
    cursor = db.cursor()
    sql = "INSERT INTO user_recommendation_index (user_id, device_type, geolocation, topical_interests, age, gender, preferred_format) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (query["user_id"], query["device_type"], query["geolocation"], "", -1, "", "")
    cursor.execute(sql, val)
    db.commit()


# searches for a user by username
def search_user_by_username(db, query: dict) -> list:
    if len(list(query.keys())) != 1:
        raise AttributeError("Should not be more than 1 query field")

    field = str(query["username"])

    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE username=%s "
    cursor.execute(
        sql,
        (field,),
    )
    results = cursor.fetchall()

    return results


# creates a new session in the database
def create_session(db, session: dict):
    cursor = db.cursor()
    sql = "INSERT INTO sessions (user_id, refresh_token, refreshExpiresAt, session_token, sessionExpiresAt) VALUES (%s, %s, %s, %s, %s)"
    val = (
        session["user_id"],
        session["refresh_token"],
        session["refreshExpiresAt"],
        session["session_token"],
        session["sessionExpiresAt"],
    )
    cursor.execute(sql, val)
    db.commit()
