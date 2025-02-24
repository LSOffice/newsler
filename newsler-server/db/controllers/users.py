# This file contains the db requests for the users sections

import os

import aiomysql
from dotenv import load_dotenv

load_dotenv()


# this function takes a dictionary containing user's preferences as input and returns a list of users
# that match the criteria, ranked by a rating score
# the rating score is calculated based on the
# similarity between the user's preferences and the preferences of other users in the database
async def get_users_based_on_rec_criteria(query: dict):
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        sql = "SELECT * FROM user_recommendation_index WHERE user_id!=%s"
        await cur.execute(sql, (query["user_id"],))
        users = await cur.fetchall()

    if "age" in query:
        condition = lambda x: (abs(x[4] - query["age"]) > 7) or x[4] == -1
        users = list(filter(lambda x: not condition(x), users))

    if "device_type" in query:
        # condition = lambda x: x[2] != query["device_type"]

        # users = list(filter(lambda x: not condition(x), users))
        pass

    if "gender" in query:
        # condition = lambda x: x[5] != query["gender"]

        # gender same is +0.15, gender different is +0.05

        # users = list(filter(lambda x: not condition(x), users))

        pass
    if "geolocation" in query:
        condition = lambda x: (
            abs(float(x[2][: x[2].index(", ")]) - query["geolocation"][0]) > 25
        ) or (abs(float(x[2][x[2].index(", ") + 2 :]) - query["geolocation"][1]) > 25)

        # geolocation within 5 is +0.5, geolocation within 10 is +0.3, geolocation within 15 is +0.24, geolocation within 20 +0.15, geolocation within 25 is +0.09

        users = list(filter(lambda x: not condition(x), users))

    user_dict = []

    for user in users:
        rating = 0
        if "age" in query:
            if user[4] > query["age"]:
                rating += 0.12 + (0.14 - 0.02 * user[4])
            elif user[4] < query["age"]:
                rating += 0.08 + (0.07 - 0.01 * user[4])

        if "device_type" in query:
            if user[2] == query["device_type"]:
                rating += 0.25
            else:
                rating += 0.10

        if "gender" in query:
            if user[5] == query["gender"]:
                rating += 0.15
            else:
                rating += 0.05

        if "geolocation" in query:
            if abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0]) < 5:
                rating += 0.5 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 10
            ):
                rating += 0.3 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 15
            ):
                rating += 0.24 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 20
            ):
                rating += 0.15 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 25
            ):
                rating += 0.09 / 2

            if abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0]) < 5:
                rating += 0.5 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 10
            ):
                rating += 0.3 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 15
            ):
                rating += 0.24 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 20
            ):
                rating += 0.15 / 2
            elif (
                abs(float(user[2][: user[2].index(", ")]) - query["geolocation"][0])
                < 25
            ):
                rating += 0.09 / 2

        user_dict.append((user[0], rating))

    return user_dict
