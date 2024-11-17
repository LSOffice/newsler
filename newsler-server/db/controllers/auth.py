import uuid
from datetime import datetime


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


def create_user(db, user: dict):
    cursor = db.cursor()
    sql = "INSERT INTO users (user_id, username, type, password, display_name) VALUES (%s, %s, %s, %s, %s)"
    user_id = str(uuid.uuid4())

    display_name = user["email"][: user["email"].find("@")]
    # Create display name from email address, parse everything after and incl. @ symbol

    val = (
        user_id,
        user["email"],
        "free",
        user["password"],
        display_name,
    )
    cursor.execute(sql, val)
    db.commit()

    return user_id


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


def create_session(db, session: dict):
    cursor = db.cursor()
    sessions = get_session_from_user_id(db, {"user_id": session["user_id"]})
    if sessions[0]:
        # if a current session already exists, check session_token valid, and if valid refresh token provided update session_token
        pass

    if session["refresh_token"]:
        query = "SELECT * FROM sessions WHERE refresh_token = %s"
        cursor.execute(query, (session["refresh_token"],))
        results = cursor.fetchall()
        if len(results) == 1:
            print(results[0])

    sql = "INSERT INTO sessions (user_id, refresh_token, refreshExpiresAt, session_token, sessionExpiresAt) VALUES (%s, %s, %s, %s, %s)"
    refresh_token = str(uuid.uuid4())
    session_token = str(uuid.uuid4())
    val = (
        session["user_id"],
        session["refresh_token"],
        session["refreshExpiresAt"],
        session["session_token"],
        session["sessionExpiresAt"],
    )
    cursor.execute(sql, val)
    db.commit()

    return refresh_token, session_token
