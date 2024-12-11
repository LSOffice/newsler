from dotenv import load_dotenv
import mysql.connector as mysql
import os
from .controllers import auth, articles, users

load_dotenv()
mydb = mysql.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


def articles_user_article_view_create(query: dict):
    return articles.user_article_view_create(mydb, query=query)


def articles_get_articles_of_topic(query: dict):
    return articles.get_articles_of_topic(mydb, query=query)


def articles_user_article_scroll_complete(query: dict):
    return articles.user_article_scroll_complete(mydb, query=query)


def articles_user_article_comment_create(query: dict):
    return articles.user_article_comment_create(mydb, query=query)


def articles_user_article_reaction_create(query: dict):
    return articles.user_article_reaction_create(mydb, query=query)


def articles_user_save_article(query: dict):
    return articles.user_save_article(mydb, query=query)


def articles_get_article_interaction_information(query: dict):
    return articles.get_article_interaction_information(mydb, query=query)


def articles_get_recent_articles():
    return articles.get_recent_articles(mydb)


def articles_get_x_user_article_interactions(query: dict):
    return articles.get_x_user_article_interactions(mydb, query=query)


def articles_get_users_article_interactions(query: dict):
    return articles.get_users_article_interactions(mydb, query)


def auth_update_user_session(query: dict):
    return auth.update_user_session(mydb, query=query)


def auth_is_session_token_valid(query: dict):
    return auth.is_session_token_valid(mydb, query=query)


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


def auth_create_user_recommendation_index(query: dict):
    return auth.create_user_recommendation_index(mydb, query=query)


def auth_update_user_recommendation_index(query: dict):
    return auth.update_user_recommendation_index(mydb, query=query)


def auth_get_user_recommendation_index(query: dict):
    return auth.get_user_recommendation_index(mydb, query=query)


def users_get_users_based_on_rec_criteria(query: dict):
    return users.get_users_based_on_rec_criteria(mydb, query=query)
