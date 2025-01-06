import asyncio
import os
import random
from code import interact
from datetime import date, datetime
import threading

import bcrypt
import google.generativeai as genai
import pandas as pd
import pycountry
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..db.controllers import auth, users, articles_c
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

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()


class Feed(BaseModel):
    user_id: str | None = None
    topic: str | None = "Trending"
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


router = APIRouter(prefix="/articles", tags=["articles"])
feeds = {}
valid_token_cache = {}
# "token": {expiresAt}

async def is_logged_in(req: Request) -> bool:
    try:
        session_token = req.headers["authorization"]
    except KeyError:
        return False

    session_token = session_token.replace("Bearer ", "")

    auth_obj = await auth.is_session_token_valid({"session_token": session_token})
    if not auth_obj[0]:
        raise HTTPException(status_code=308, detail="Redirect /login")
    if not auth_obj[1]:
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
    for interaction in interactions: # type: ignore
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

        for interaction in interactions: # type: ignore
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


@router.post("/feed")
async def feed(body: Feed, auth_headers: bool = Depends(is_logged_in)):

    user_id = body.user_id
    topic = body.topic
    page = body.page

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    if user_id == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    starttime = datetime.now()

    # through genre find list of articles, then find people with similar tastes
    # preload 20 posts, then as they reach 15 load 10
    if topic == "Trending":
        # loop = asyncio.get_running_loop()
        # thread = threading.Thread(target=loop.run_until_complete, args=(worker(query),))

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
            articles = await articles_c.get_all_articles()
            random.shuffle(articles)

            if page == 1:
                return articles[0:20]
            else:
                return articles[20 + int(page - 2) * 30 : 20 + int(page - 2) * 30 + 30]  # type: ignore

        if str(user_id) not in feeds:
            feeds[str(user_id)] = []

        requester_id = user_id
        rows = []
        for user_id, ratings in uar.items():
            for article_id, rating in ratings.items():
                ratingd = rating["rating"]
                if rating["viewed"]:
                    ratingd *= 0.10
                if article_id in feeds[str(requester_id)]:
                    ratingd *= 0.29
                rows.append(
                    {"user_id": user_id, "article_id": article_id, "rating": ratingd}
                )

        df = pd.DataFrame(rows)
        article_ratings = df.groupby("article_id")["rating"].mean()
        article_ids = article_ratings.sort_values(ascending=False)
        articles = await articles_c.get_all_articles()
        filtered_articles = articles.copy()
        article_id_to_article = {article["article_id"]: article for article in articles}

        for row in article_ids.index:
            for article in articles:
                if (
                    article["article_id"] == row
                    or article["article_id"] in feeds[str(requester_id)]
                ):
                    try:
                        filtered_articles.remove(article)
                    except:
                        pass

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
                        if articles[0]["article_id"] not in article_id_list:
                            article_id_list.append(articles[0]["article_id"])
                            articles.pop(0)
                            locked = False
        else:
            if len(article_id_list) < 30:
                random.shuffle(filtered_articles)
                for i in range(30 - len(article_id_list)):
                    locked = True
                    while locked:
                        if articles[0]["article_id"] not in article_id_list:
                            article_id_list.append(articles[0]["article_id"])
                            articles.pop(0)
                            locked = False
        article_list = []

        for article_id in article_id_list:
            article_list.append(article_id_to_article[article_id])

        feeds[str(requester_id)].extend(article_id_list)
        
        return article_list

    elif pycountry.countries.get(name=topic):

        # geolocation rating ONLY in rec_criteria and articles tagged with country
        # highest rating users x the user article ratings add together to form total rating
        #  average the total rating and highest rating is top of feed, then scrolls down and 20-10-10-10...
        pass

    else:
        article_list = articles_get_articles_of_topic({"topic": topic})
        topics_of_interest = []

        return article_list


@router.get("/aitest")
async def aitest():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("The opposite of hot is")
    return response.text


@router.post("/article")
async def article_information(
    body: Article, auth_headers: bool = Depends(is_logged_in)
):
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")
    return articles_get_article_details_and_interactions(
        {"article_id": body.article_id, "user_id": body.user_id}
    )


@router.post("/view")
async def article_view(body: ArticleView, auth_headers: bool = Depends(is_logged_in)):
    article_id = body.article_id
    user_id = body.user_id
    vs = body.view_seconds
    sd = body.scroll_depth
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    # TODO: potentially unsafe point, any token can use any user id)
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


@router.post("/saved")
async def saved(body: Headers, auth_headers: bool = Depends(is_logged_in)):
    user_id = body.user_id
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    return articles_get_saved_articles({"user_id": user_id})


@router.post("/headers")
async def headers(body: Headers, auth_headers: bool = Depends(is_logged_in)):
    user_id = body.user_id

    if user_id == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    interactions = await recent_x_user_article_interactions_ranked(
        user_id=user_id, x=100
    )

    topics_of_interest = {}
    starter_topics = ["Politics", "Business", "Health", "Technology", "Entertainment"]

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
        for header in headers:
            if header in starter_topics:
                starter_topics.remove(header)
        headers += starter_topics
    country_code = auth_return_user_object_from_user_id({"user_id": user_id})[5]

    headers = [pycountry.countries.get(alpha_2=country_code).name, "Trending"] + headers
    asyncio.create_task(
        articles_user_set_age_and_gender({"headers": headers, "user_id": user_id})
    )
    return headers
