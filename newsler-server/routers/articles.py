from code import interact
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
import pycountry
import bcrypt
from ..db.init import (
    articles_get_article_interaction_information,
    articles_get_articles_of_topic,
    articles_get_recent_articles,
    articles_get_users_article_interactions,
    articles_get_x_user_article_interactions,
    articles_user_article_comment_create,
    articles_user_save_article,
    auth_get_user_recommendation_index,
    auth_is_session_token_valid,
    auth_return_user_object_from_user_id,
    users_get_users_based_on_rec_criteria,
)
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()


class Feed(BaseModel):
    user_id: str | None = None
    topic: str | None = "Trending"
    page: int | None = 1


class Headers(BaseModel):
    user_id: str | None = None


router = APIRouter(prefix="/articles", tags=["articles"])


async def is_logged_in(req: Request) -> bool:
    try:
        session_token = req.headers["Authorization"]
    except KeyError:
        return False

    session_token = session_token.replace("Bearer ", "")
    auth_obj = auth_is_session_token_valid({"session_token": session_token})

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

    for interaction in interactions:
        recency_factor = 14  # number of days considered recent
        total_weighting = 0

        article_id = interaction[3]
        if article_id not in articles:
            articles[article_id] = 0
        if datetime.fromtimestamp(int(interaction[2])) >= (
            datetime.fromtimestamp(
                datetime.now().timestamp() - recency_factor * 24 * 60 * 60
            )
        ):
            # TODO: very inefficient retrieval that needs to be reworked
            interaction_info = articles_get_article_interaction_information(
                {"reaction_id": interaction[1]}
            )

            if interaction[4] == 1:
                # View
                total_weighting += view_weighting
            elif interaction[4] == 2:
                # full scroll, therefore scroll depth is 0.0-1.0
                total_weighting += full_scroll_weighting * float(interaction_info[5])

            elif interaction[4] == 3:
                # Comment
                total_weighting += comment_weighting
                total_weighting += 0.001 * len(interaction_info[5].split())
            elif interaction[4] == 4:
                # Reaction (emoji)
                if interaction_info[5] > 0:
                    total_weighting += reaction_weighting
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


async def user_article_ratings(users: list) -> list:
    reaction_weighting = 0.7
    view_weighting = 0.1
    full_scroll_weighting = 0.5
    comment_weighting = 0.7
    saved_weighting = 0.97

    interactions = articles_get_users_article_interactions({"users": users})

    for user in users:

        articles = {}

        for interaction in interactions:
            if interaction[0] != user:
                continue
            recency_factor = 14  # number of days considered recent
            total_weighting = 0

            article_id = interaction[3]
            if article_id not in articles:
                articles[article_id] = 0
            if datetime.fromtimestamp(int(interaction[2])) >= (
                datetime.fromtimestamp(
                    datetime.now().timestamp() - recency_factor * 24 * 60 * 60
                )
            ):
                # TODO: very inefficient retrieval that needs to be reworked
                interaction_info = articles_get_article_interaction_information(
                    {"reaction_id": interaction[1]}
                )

                if interaction[4] == 1:
                    # View
                    total_weighting += view_weighting
                elif interaction[4] == 2:
                    # full scroll, therefore scroll depth is 0.0-1.0
                    total_weighting += full_scroll_weighting * float(
                        interaction_info[5]
                    )

                elif interaction[4] == 3:
                    # Comment
                    total_weighting += comment_weighting
                    total_weighting += 0.001 * len(interaction_info[5].split())
                elif interaction[4] == 4:
                    # Reaction (emoji)
                    if interaction_info[5] > 0:
                        total_weighting += reaction_weighting
                    else:
                        total_weighting += reaction_weighting / 2
                elif interaction[4] == 5:
                    # Saved article
                    total_weighting += saved_weighting
                articles[article_id] += total_weighting
        print(articles)
    # This following line sorts articles by their value, in the {article_id: weighting}
    # it sorts by weighting where greatest weighting is at the front of the array with
    # the key-value pairs
    pass


@router.get("/feed")
async def feed(body: Feed, auth_headers: bool = Depends(is_logged_in)):
    user_id = body.user_id
    topic = body.topic

    if user_id == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # through genre find list of articles, then find people with similar tastes
    # preload 20 posts, then as they reach 15 load 10
    if topic == "Trending":
        # past 2 days trending articles

        recommendation_indexes = auth_get_user_recommendation_index(
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
        users = users_get_users_based_on_rec_criteria(
            {"user_id": user_id, "age": age, "gender": gender, "geolocation": location}
        )
        users.append(("60858c60-70cd-4d44-8496-4f2c518a169b",))
        print(await user_article_ratings([user[0] for user in users]))

        # highest rating users x the user article ratings add together to form total rating
        #  average the total rating and highest rating is top of feed, then scrolls down and 20-10-10-10...

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


@router.get("/headers")
async def headers(body: Headers, auth_headers: bool = Depends(is_logged_in)):
    user_id = body.user_id

    if user_id == None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

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

    return headers
