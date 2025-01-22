# This page represents all of the backend functions that power article functionality in this app.
# The routes include /articles/feed, /articles/headers, /articles/saved, /articles/save, /articles/view,
# /articles/reaction, /articles/article

import asyncio
import os
import random
import threading
from code import interact
from datetime import date, datetime

import bcrypt
import google.generativeai as genai
import pandas as pd
import pycountry
import reverse_geocode
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..db.controllers import articles_c, auth, users
from ..db.init import (
    articles_get_article_details_and_interactions,
    articles_get_article_from_article_id,
    articles_get_article_interaction_information,
    articles_get_articles_of_topic,
    articles_get_recent_articles,
    articles_get_saved_articles,
    articles_get_users_article_interactions,
    articles_get_x_user_article_interactions,
    articles_user_article_comment_create,
    articles_user_article_reaction_create,
    articles_user_article_scroll_complete,
    articles_user_article_view_create,
    articles_user_save_article,
    articles_user_set_age_and_gender,
    articles_user_unsave_article,
    auth_return_user_object_from_user_id,
)

# Loading environment variables to hash, use generative AI, and from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()

# Are all basemodels to help structure incoming data


class Feed(BaseModel):
    user_id: str | None = None
    topic: str | None = "For you"
    page: int | None = 1


class Article(BaseModel):
    article_id: str | None = None
    user_id: str | None = None


class ArticleView(BaseModel):
    article_id: str | None = None
    user_id: str | None = None
    view_seconds: int | None = None
    scroll_depth: float | None = None


class ArticleReaction(BaseModel):
    article_id: str | None = None
    user_id: str | None = None
    reaction_sentiment: float | None = None


class ArticleSaveReaction(BaseModel):
    article_id: str | None = None
    user_id: str | None = None
    save: bool | None = None


class Headers(BaseModel):
    user_id: str | None = None


# All articles pre-loaded
articles = []


# Implements a basic queue data structure with a fixed length
class Queue:
    def __init__(self, length):
        self.obj = []
        self.length = length

    # Adds item to the back of the queue
    def enqueue(self, item):
        if len(self.obj) == self.length:
            raise IndexError("Queue full")
        self.obj.append(item)

    # Removes and returns item from the front of the queue
    def dequeue(self):
        if len(self.obj) == 0:
            raise IndexError("Queue empty")
        return self.obj.pop(0)

    # Return the item at the front of the queue
    def front(self):
        if len(self.obj) == 0:
            raise IndexError("Queue empty")
        return self.obj[0]

    # Return the item at the back of the queue
    def rear(self):
        if len(self.obj) == 0:
            raise IndexError("Queue empty")
        return self.obj[-1]

    # If queue is empty
    def isEmpty(self):
        return len(self.obj) == 0

    # If queue is full
    def isFull(self):
        return len(self.obj) == self.length

    # Size of queue
    def size(self):
        return len(self.obj)

    # Returns the object
    def getObject(self):
        return self.obj


# Implements a basic stack data structure with a fixed length
class Stack:
    def __init__(self, length):
        self.obj = []
        self.length = length

    # Adds item to the top of the stack
    def push(self, item):
        if len(self.obj) == self.length:
            raise IndexError("Stack full")
        self.obj.append(item)

    # Removes and returns item at the top of the stack
    def pop(self):
        if len(self.obj) == 0:
            raise IndexError("Stack empty")
        return self.obj.pop()

    # Returns the item at the top of the stack
    def top(self):
        if len(self.obj) == 0:
            raise IndexError("Stack empty")
        return self.obj[-1]

    # If stack is empty
    def isEmpty(self):
        return len(self.obj) == 0

    # If stack is full
    def isFull(self):
        return len(self.obj) == self.length

    # Size of stack
    def size(self):
        return len(self.obj)

    # Returns the stack
    def getObject(self):
        return self.obj

    # shuffles stack according to Fisher-Yates shuffle Algorithm random
    def shuffle(self):
        for i in range(len(self.obj) - 1, 0, -1):
            j = random.randint(0, i)

            self.obj[i], self.obj[j] = self.obj[j], self.obj[i]


# Preloading articles
async def get_articles():
    global articles
    print("Getting articles")
    articles = await articles_c.get_all_articles()
    print("articles retrieved")


asyncio.run(get_articles())

router = APIRouter(prefix="/articles", tags=["articles"])
feeds = {}


# Function to determine if user is logged in
async def is_logged_in(req: Request) -> bool:
    try:
        # get Authorisation from headers of request
        session_token = req.headers["authorization"]
    except KeyError:
        return False

    # Remove "Bearer" from session_token
    session_token = session_token.replace("Bearer ", "")

    # Get validity of session_token
    auth_obj = await auth.is_session_token_valid({"session_token": session_token})
    if not auth_obj[0]:
        # if no refresh_token or expired refresh_token
        raise HTTPException(status_code=308, detail="Redirect /login")
    if not auth_obj[1]:
        # if no session_token or expired session_token
        raise HTTPException(status_code=308, detail="Redirect /refreshsession")

    return True


# to determine the recent topics that the user enjoys (tags/genre)
async def recent_x_user_article_interactions_ranked(user_id: str, x: int) -> list:
    reaction_weighting = 0.7
    view_weighting = 0.1
    full_scroll_weighting = 0.5
    comment_weighting = 0.7
    saved_weighting = 0.97

    interactions = articles_get_x_user_article_interactions(
        {"x": x, "user_id": user_id}
    )
    articles = {}
    for interaction in interactions:  # type: ignore
        recency_factor = 14  # number of days considered recent
        total_weighting = 0

        article_id = interaction[3]
        if article_id not in articles:
            articles[article_id] = 0
        elif datetime.fromtimestamp(int(interaction[2])) >= (
            datetime.fromtimestamp(
                datetime.now().timestamp() - recency_factor * 24 * 60 * 60
            )
        ):
            if interaction[4] == 1:
                # View
                total_weighting += view_weighting  # + int(interaction[5] * 0.001)
            elif interaction[4] == 2:
                # full scroll, therefore scroll depth is 0.0-1.0
                total_weighting += full_scroll_weighting * float(interaction[5])

            elif interaction[4] == 3:
                # Comment
                total_weighting += comment_weighting
                total_weighting += 0.001 * len(interaction[5].split())
            elif interaction[4] == 4:
                # Reaction (emoji)
                if float(interaction[5]) > 0.5:
                    total_weighting += reaction_weighting
                elif float(interaction[5]) == 0.5:
                    total_weighting += reaction_weighting / 1.5
                else:
                    total_weighting += reaction_weighting / 2
            elif interaction[4] == 5:
                # Saved article
                total_weighting += saved_weighting
            articles[article_id] += total_weighting

    # This following line sorts articles by their value, in the {article_id: weighting}
    # it sorts by weighting where greatest weighting is at the front of the array with
    # the key-value pairs
    return sorted(articles.items(), key=lambda item: item[1], reverse=True)


# to get the ratings of users by article_ids
async def user_article_ratings(users: list) -> dict:
    reaction_weighting = 0.7
    view_weighting = 0.1
    full_scroll_weighting = 0.5
    comment_weighting = 0.7
    saved_weighting = 0.97

    interactions = articles_get_users_article_interactions({"users": users})

    user_dict = {}
    for user in users:
        articles = {}

        for interaction in interactions:  # type: ignore
            if interaction[0] != user:
                continue
            recency_factor = 14  # number of days considered recent
            total_weighting = 0

            article_id = interaction[3]
            if article_id not in articles:
                articles[article_id] = {"rating": 0, "viewed": False}

            if interaction[4] == 1:
                # View
                total_weighting += view_weighting  # + int(interaction[5] * 0.001)
                if int(interaction[5]) > 10:
                    articles[article_id]["viewed"] = True
            elif interaction[4] == 2:
                # full scroll, therefore scroll depth is 0.0-1.0
                total_weighting += full_scroll_weighting * float(interaction[5])

            elif interaction[4] == 3:
                # Comment
                total_weighting += comment_weighting
                total_weighting += 0.001 * len(interaction[5].split())
            elif interaction[4] == 4:
                # Reaction (emoji)
                if float(interaction[5]) > 0.5:
                    total_weighting += reaction_weighting
                elif float(interaction[5]) == 0.5:
                    total_weighting += reaction_weighting / 1.5
                else:
                    total_weighting += reaction_weighting / 2
            elif interaction[4] == 5:
                # Saved article
                total_weighting += saved_weighting

            articles[article_id]["rating"] += total_weighting
        user_dict[user] = articles

    return user_dict


# ratings of articles by users all around the world (trending)
async def global_article_ratings() -> dict:
    reaction_weighting = 0.7
    view_weighting = 0.1
    full_scroll_weighting = 0.5
    comment_weighting = 0.7
    saved_weighting = 0.97

    interactions = await articles_c.get_global_users_article_interactions()
    users = []
    for interaction in interactions:
        if interaction[0] not in users:
            users.append(interaction[0])

    user_dict = {}
    for user in users:
        articles = {}

        for interaction in interactions:  # type: ignore
            if interaction[0] != user:
                continue
            total_weighting = 0

            article_id = interaction[3]
            if article_id not in articles:
                articles[article_id] = {"rating": 0, "viewed": False}

            if interaction[4] == 1:
                # View
                total_weighting += view_weighting  # + int(interaction[5] * 0.001)
                if int(interaction[5]) > 10:
                    articles[article_id]["viewed"] = True
            elif interaction[4] == 2:
                # full scroll, therefore scroll depth is 0.0-1.0
                total_weighting += full_scroll_weighting * float(interaction[5])

            elif interaction[4] == 3:
                # Comment
                total_weighting += comment_weighting
                total_weighting += 0.001 * len(interaction[5].split())
            elif interaction[4] == 4:
                # Reaction (emoji)
                if float(interaction[5]) > 0.5:
                    total_weighting += reaction_weighting
                elif float(interaction[5]) == 0.5:
                    total_weighting += reaction_weighting / 1.5
                else:
                    total_weighting += reaction_weighting / 2
            elif interaction[4] == 5:
                # Saved article
                total_weighting += saved_weighting

            if abs(datetime.now().timestamp() - interaction[2]) < 86400:
                articles[article_id]["rating"] += total_weighting
        user_dict[user] = articles

    return user_dict


# Code that powers the main feed algorithm (trending "for you", specific topic, country-based)
@router.post("/feed")
async def feed(body: Feed, auth_headers: bool = Depends(is_logged_in)):
    global articles
    user_id = body.user_id
    topic = body.topic
    page = body.page

    if not auth_headers:
        # if authentication headers not valid (session_token invalid)
        raise HTTPException(status_code=401, detail="Unauthorised")

    if user_id == None:
        # if required information not provided in body
        raise HTTPException(status_code=400, detail="Invalid credentials")
    requester_id = user_id
    if str(user_id) not in feeds:
        feeds[str(user_id)] = []

    # through genre find list of articles, then find people with similar tastes
    # preload 20 posts, then as they reach 15 load 10
    if topic == "For you":
        uar = await global_article_ratings()
        rows = []
        for user_id, ratings in uar.items():
            for article_id, rating in ratings.items():
                ratingd = rating["rating"]

                if not (rating["viewed"]):
                    rows.append(
                        {
                            "user_id": user_id,
                            "article_id": article_id,
                            "rating": ratingd,
                        }
                    )

        df = pd.DataFrame(rows)
        article_ratings = df.groupby("article_id")["rating"].mean()
        article_ids = article_ratings.sort_values(ascending=False)

        article_id_to_article = {article["article_id"]: article for article in articles}

        if page == 1:
            articles_a = article_ids.iloc[0:20]
        else:
            articles_a = article_ids.iloc[20 + int(page - 2) * 30 : 20 + int(page - 2) * 30 + 30]  # type: ignore

        article_id_list = []
        filtered_articles = articles.copy()
        for article_id in articles_a.index:
            if article_id not in feeds[str(requester_id)]:
                article_id_list.append(article_id)

        if page == 1:
            if len(article_id_list) < 20:
                random.shuffle(filtered_articles)
                for i in range(20 - len(article_id_list)):
                    locked = True
                    while locked:
                        if filtered_articles[0]["article_id"] not in article_id_list:
                            article_id_list.append(filtered_articles[0]["article_id"])
                            locked = False
                        else:
                            filtered_articles.pop(0)
        else:
            if len(article_id_list) < 30:
                random.shuffle(filtered_articles)
                for i in range(30 - len(article_id_list)):
                    locked = True
                    while locked:
                        if filtered_articles[0]["article_id"] not in article_id_list:
                            article_id_list.append(filtered_articles[0]["article_id"])
                            locked = False
                        else:
                            filtered_articles.pop(0)
        article_list = []

        for article_id in article_id_list:
            article_list.append(article_id_to_article[article_id])

        feeds[str(requester_id)].extend(article_id_list)
        return article_list

    elif pycountry.countries.get(name=topic):
        # geolocation rating ONLY in rec_criteria and articles tagged with country
        # highest rating users x the user article ratings add together to form total rating
        #  average the total rating and highest rating is top of feed, then scrolls down and 20-10-10-10...
        country_code = pycountry.countries.get(name=topic).alpha_2
        article_list = [
            article for article in articles if article["country"] == country_code
        ]
        recommendation_indexes = await auth.get_user_recommendation_index(
            {"user_id": user_id}
        )
        # query parameters:
        # ignore device_type for now

        location = (
            float(recommendation_indexes[2][: recommendation_indexes[2].index(", ")]),
            float(
                recommendation_indexes[2][(recommendation_indexes[2].index(", ") + 2) :]
            ),
        )
        # if latitude and longitude +- 15

        topical_interests = [i.strip() for i in recommendation_indexes[3].split(",")]
        # shares at least 1 item on topical_interests
        if topical_interests == []:
            pass
        age = recommendation_indexes[4]
        # +- 8 years
        gender = recommendation_indexes[5]
        # same gender but low weighting
        # ignore preferred_format for now
        us = await users.get_users_based_on_rec_criteria(
            {"user_id": user_id, "age": age, "gender": gender, "geolocation": location}
        )

        try:
            uar = await user_article_ratings([user[0] for user in us])
        except IndexError:
            random.shuffle(article_list)
            article_id_list = []

            if page == 1:
                articles_result = article_list[0:20]
            else:
                articles_result = article_list[20 + int(page - 2) * 30 : 20 + int(page - 2) * 30 + 30]  # type: ignore

            for article_id in articles_result:
                article_id_list.append(article_id)
            feeds[str(requester_id)].extend(article_id_list)
            return articles_result

        rows = []
        for user_id, ratings in uar.items():
            for article_id, rating in ratings.items():
                ratingd = rating["rating"]

                if article_id in feeds[str(requester_id)]:
                    ratingd *= 0.29

                if not rating["viewed"]:
                    rows.append(
                        {
                            "user_id": user_id,
                            "article_id": article_id,
                            "rating": ratingd,
                        }
                    )

        filtered_articles = article_list.copy()
        article_id_to_article = {
            article["article_id"]: article for article in article_list
        }

        for row in rows:
            try:
                filtered_articles.remove(article_id_to_article[row["article_id"]])
            except:
                pass
        for article_id in article_id_to_article:
            if article_id in feeds[str(requester_id)]:
                try:
                    filtered_articles.remove(article_id_to_article[article_id])
                except:
                    pass

        df = pd.DataFrame(rows)
        article_ratings = df.groupby("article_id")["rating"].mean()
        article_ids = article_ratings.sort_values(ascending=False)

        if page == 1:
            articles_a = article_ids.iloc[0:20]
        else:
            articles_a = article_ids.iloc[20 + int(page - 2) * 30 : 20 + int(page - 2) * 30 + 30]  # type: ignore
        # past 2 days trending articles

        # highest rating users x the user article ratings add together to form total rating
        #  average the total rating and highest rating is top of feed, then scrolls down and 20-10-10-10...

        article_id_list = []

        for article_id in articles_a.index:
            article_id_list.append(article_id)

        if page == 1:
            if len(article_id_list) < 20:
                random.shuffle(filtered_articles)
                for i in range(20 - len(article_id_list)):
                    locked = True
                    while locked:
                        if filtered_articles[0]["article_id"] not in article_id_list:
                            article_id_list.append(filtered_articles[0]["article_id"])
                            locked = False
                        else:
                            filtered_articles.pop(0)
        else:
            if len(article_id_list) < 30:
                random.shuffle(filtered_articles)
                for i in range(30 - len(article_id_list)):
                    locked = True
                    while locked:
                        if filtered_articles[0]["article_id"] not in article_id_list:
                            article_id_list.append(filtered_articles[0]["article_id"])
                            locked = False
                        else:
                            filtered_articles.pop(0)
        article_list = []

        for article_id in article_id_list:
            try:
                article_list.append(article_id_to_article[article_id])
            except KeyError:
                pass

        feeds[str(requester_id)].extend(article_id_list)

        return article_list

    else:
        article_list = [article for article in articles if article["topic"] == topic]
        recommendation_indexes = await auth.get_user_recommendation_index(
            {"user_id": user_id}
        )
        # query parameters:
        # ignore device_type for now

        location = (
            float(recommendation_indexes[2][: recommendation_indexes[2].index(", ")]),
            float(
                recommendation_indexes[2][(recommendation_indexes[2].index(", ") + 2) :]
            ),
        )
        # if latitude and longitude +- 15

        topical_interests = [i.strip() for i in recommendation_indexes[3].split(",")]
        # shares at least 1 item on topical_interests
        if topical_interests == []:
            pass
        age = recommendation_indexes[4]
        # +- 8 years
        gender = recommendation_indexes[5]
        # same gender but low weighting
        # ignore preferred_format for now
        us = await users.get_users_based_on_rec_criteria(
            {"user_id": user_id, "age": age, "gender": gender, "geolocation": location}
        )

        try:
            uar = await user_article_ratings([user[0] for user in us])
        except IndexError:
            random.shuffle(article_list)
            article_id_list = []

            if page == 1:
                articles_result = article_list[0:20]
            else:
                articles_result = article_list[20 + int(page - 2) * 30 : 20 + int(page - 2) * 30 + 30]  # type: ignore

            for article_id in articles_result:
                article_id_list.append(article_id)
            feeds[str(requester_id)].extend(article_id_list)
            return articles_result

        rows = []
        for user_id, ratings in uar.items():
            for article_id, rating in ratings.items():
                ratingd = rating["rating"]

                if article_id in feeds[str(requester_id)]:
                    ratingd *= 0.29

                if not rating["viewed"]:
                    rows.append(
                        {
                            "user_id": user_id,
                            "article_id": article_id,
                            "rating": ratingd,
                        }
                    )

        filtered_articles = article_list.copy()

        article_id_to_article = {
            article["article_id"]: article for article in article_list
        }

        for row in rows:
            try:
                filtered_articles.remove(article_id_to_article[row["article_id"]])
            # trunk-ignore(bandit/B110)
            except:
                pass
        for article_id in article_id_to_article:
            if article_id in feeds[str(requester_id)]:
                try:
                    filtered_articles.remove(article_id_to_article[article_id])
                # trunk-ignore(bandit/B110)
                except:
                    pass

        df = pd.DataFrame(rows)
        article_ratings = df.groupby("article_id")["rating"].mean()
        article_ids = article_ratings.sort_values(ascending=False)

        if page == 1:
            articles_a = article_ids.iloc[0:20]
        else:
            articles_a = article_ids.iloc[20 + int(page - 2) * 30 : 20 + int(page - 2) * 30 + 30]  # type: ignore
        # past 2 days trending articles

        # highest rating users x the user article ratings add together to form total rating
        #  average the total rating and highest rating is top of feed, then scrolls down and 20-10-10-10...

        article_id_list = []

        for article_id in articles_a.index:
            article_id_list.append(article_id)
        if page == 1:
            if len(article_id_list) < 20:
                random.shuffle(filtered_articles)
                for i in range(20 - len(article_id_list)):
                    locked = True

                    while locked:
                        try:
                            if (
                                filtered_articles[0]["article_id"]
                                not in article_id_list
                            ):
                                article_id_list.append(
                                    filtered_articles[0]["article_id"]
                                )
                                locked = False
                            else:
                                filtered_articles.pop(0)
                        except IndexError:
                            locked = False

        else:
            if len(article_id_list) < 30:
                random.shuffle(filtered_articles)
                for i in range(30 - len(article_id_list)):
                    locked = True
                    while locked:
                        if filtered_articles[0]["article_id"] not in article_id_list:
                            article_id_list.append(filtered_articles[0]["article_id"])
                            locked = False
                        else:
                            filtered_articles.pop(0)
        article_list = []
        for article_id in article_id_list:
            try:
                article_list.append(article_id_to_article[article_id])
            except KeyError:
                pass

        feeds[str(requester_id)].extend(article_id_list)
        return article_list


# Loads article information when viewing article
@router.post("/article")
async def article_information(
    body: Article, auth_headers: bool = Depends(is_logged_in)
):
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")
    return articles_get_article_details_and_interactions(
        {"article_id": body.article_id, "user_id": body.user_id}
    )


# Records an article view after article has been read
@router.post("/view")
async def article_view(body: ArticleView, auth_headers: bool = Depends(is_logged_in)):
    article_id = body.article_id
    user_id = body.user_id
    vs = body.view_seconds
    sd = body.scroll_depth
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    asyncio.create_task(
        articles_user_article_view_create(
            {"user_id": user_id, "article_id": article_id, "view_seconds": vs}
        )
    )

    asyncio.create_task(
        articles_user_article_scroll_complete(
            {"user_id": user_id, "article_id": article_id, "scroll_depth": sd}
        )
    )
    return True


# Record article reaction by user on article
@router.post("/reaction")
async def article_reaction(
    body: ArticleReaction, auth_headers: bool = Depends(is_logged_in)
):
    article_id = body.article_id
    user_id = body.user_id
    reaction_sentiment = body.reaction_sentiment
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")
    return articles_user_article_reaction_create(
        {
            "user_id": user_id,
            "article_id": article_id,
            "reaction_sentiment": reaction_sentiment,
        }
    )


# Record article save by user into saved articles
@router.post("/save")
async def article_save(
    body: ArticleSaveReaction, auth_headers: bool = Depends(is_logged_in)
):
    article_id = body.article_id
    user_id = body.user_id
    save = body.save
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    # TODO: potentially unsafe point, any token can use any user id)
    if save:
        asyncio.create_task(
            articles_user_save_article({"user_id": user_id, "article_id": article_id})
        )
    else:
        asyncio.create_task(
            articles_user_unsave_article({"user_id": user_id, "article_id": article_id})
        )

    return True


# Checks all articles that a user has saved
@router.post("/saved")
async def saved(body: Headers, auth_headers: bool = Depends(is_logged_in)):
    user_id = body.user_id
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = articles_get_saved_articles({"user_id": user_id})

    # Sorting the saved articles randomly

    stack = Stack(len(result))
    for _ in result:
        stack.push(_)

    stack.shuffle()
    return stack.getObject()


# Get the headers "For you", country, topics of interest on top of feed page
@router.post("/headers")
async def headers(body: Headers, auth_headers: bool = Depends(is_logged_in)):
    user_id = body.user_id

    if user_id == None:
        # If user_id not provided
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not auth_headers:
        # If
        raise HTTPException(status_code=401, detail="Unauthorised")

    interactions = await recent_x_user_article_interactions_ranked(
        user_id=user_id, x=100
    )

    topics_of_interest = {}
    st = ["Politics", "Business", "Health", "Technology", "Entertainment"]
    starter_topics = Queue(5)
    for _ in st:
        starter_topics.enqueue(_)

    # Condenses into dictionary with {article_id: genre}
    articles = {article[0]: article[5] for article in articles_get_recent_articles()}
    for interaction in interactions:
        if articles[interaction[0]] not in topics_of_interest:
            topics_of_interest[articles[interaction[0]]] = 0
        topics_of_interest[articles[interaction[0]]] += interaction[1]

    headers_in_order = {
        k: v
        for k, v in sorted(
            topics_of_interest.items(), key=lambda item: item[1], reverse=True
        )
    }

    headers = list(headers_in_order.keys())[:6]
    if len(headers) != 6:
        while len(headers) < 6 and not starter_topics.isEmpty():
            header = starter_topics.dequeue()
            if header not in headers:
                headers.append(header)
    geolocation = await auth.get_user_geolocation({"user_id": user_id})
    coordinates = (
        (
            float(geolocation[: geolocation.find(",")]),
            float(geolocation[2 + geolocation.find(",") :]),
        ),
    )
    country_code = reverse_geocode.search(coordinates)[0]["country_code"]

    headers = [pycountry.countries.get(alpha_2=country_code).name, "For you"] + headers
    asyncio.create_task(
        articles_user_set_age_and_gender({"headers": headers, "user_id": user_id})
    )
    return headers
