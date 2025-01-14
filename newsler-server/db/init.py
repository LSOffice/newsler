import os

import mysql.connector as mysql
from dotenv import load_dotenv

from .controllers import articles_c as articles
from .controllers import auth, users

load_dotenv()


async def articles_user_article_view_create(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return await articles.user_article_view_create(mydb, query=query)


def articles_get_article_details_and_interactions(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_article_details_and_interactions(mydb, query=query)


def articles_get_articles_of_topic(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_articles_of_topic(mydb, query=query)


async def articles_user_article_scroll_complete(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return await articles.user_article_scroll_complete(mydb, query=query)


def articles_user_article_comment_create(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.user_article_comment_create(mydb, query=query)


def articles_user_article_reaction_create(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.user_article_reaction_create(mydb, query=query)


async def articles_user_save_article(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return await articles.user_save_article(mydb, query=query)


async def articles_user_unsave_article(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return await articles.user_unsave_article(mydb, query=query)


def articles_get_saved_articles(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_saved_articles(mydb, query=query)


def articles_get_article_interaction_information(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_article_interaction_information(mydb, query=query)


async def articles_user_set_age_and_gender(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return await articles.user_set_age_and_gender(mydb, query=query)


def articles_get_recent_articles():
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_recent_articles(mydb)


def articles_get_article_from_article_id(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_article_from_article_id(mydb, query=query)


def articles_get_x_user_article_interactions(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_x_user_article_interactions(mydb, query=query)


def articles_get_users_article_interactions(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return articles.get_users_article_interactions(mydb, query)


def auth_update_user_session(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.update_user_session(mydb, query=query)


def auth_update_user_session_token_only(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.update_user_session_token_only(mydb, query=query)


def auth_return_user_object_from_user_id(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.return_user_object_from_user_id(mydb, query=query)


def auth_get_session_from_user_id(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.get_session_from_user_id(mydb, query=query)


def auth_search_user_by_username(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.search_user_by_username(mydb, query=query)


def auth_create_session(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.create_session(mydb, session=query)


def auth_create_user(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.create_user(mydb, user=query)


def auth_create_user_recommendation_index(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.create_user_recommendation_index(mydb, query=query)


def auth_update_user_recommendation_index(query: dict):
    mydb = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return auth.update_user_recommendation_index(mydb, query=query)
