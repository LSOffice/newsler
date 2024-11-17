from dotenv import load_dotenv
import mysql.connector as mysql
import os
from .controllers import auth

load_dotenv()
mydb = mysql.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


def auth_update_user_session(query: dict):
    return auth.update_user_session(mydb, query=query)


def auth_update_user_session_token_only(query: dict):
    return auth.update_user_session_token_only(mydb, query=query)


def auth_return_user_object_from_user_id(query: dict):
    return auth.return_user_object_from_user_id(mydb, query=query)


def auth_get_session_from_user_id(query: dict):
    return auth.get_session_from_user_id(mydb, query=query)


def auth_search_user_by_username(query: dict):
    return auth.search_user_by_username(mydb, query=query)


def auth_create_session(query: dict):
    return auth.create_session(mydb, session=query)


def auth_create_user(query: dict):
    return auth.create_user(mydb, user=query)
