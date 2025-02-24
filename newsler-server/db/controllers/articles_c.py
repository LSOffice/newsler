# This file contains the db requests for the articles sections

import os
from datetime import datetime
from tracemalloc import start
from uuid import uuid4

import aiomysql
import bcrypt

salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()


# this function creates a new record for when a user views an article
async def user_article_view_create(db, query: dict):
    cursor = db.cursor()

    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        int(datetime.now().timestamp()),
        query["article_id"],
        1,
    )
    cursor.execute(sql, val)

    sql = "INSERT INTO article_view_information (reaction_id, view_seconds) VALUES (%s, %s)"
    val = (reaction_id, query["view_seconds"])
    cursor.execute(sql, val)

    db.commit()


# this function creates a new record for when a user scrolls through an article
async def user_article_scroll_complete(db, query: dict):
    cursor = db.cursor()

    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        int(datetime.now().timestamp()),
        query["article_id"],
        2,
    )
    cursor.execute(sql, val)

    sql = "INSERT INTO article_scroll_information (reaction_id, scroll_depth) VALUES (%s, %s)"
    val = (reaction_id, query["scroll_depth"])
    cursor.execute(sql, val)
    db.commit()


# this function creates a new record for when a user comments on an article
def user_article_comment_create(db, query: dict):
    cursor = db.cursor()

    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        int(datetime.now().timestamp()),
        query["article_id"],
        3,
    )
    cursor.execute(sql, val)

    sql = (
        "INSERT INTO article_comment_information (reaction_id, comment) VALUES (%s, %s)"
    )
    val = (reaction_id, query["comment"])
    cursor.execute(sql, val)
    db.commit()

    return True


# this function updates the age and gender of a user based on their article interactions
async def user_set_age_and_gender(db, query: dict):
    cursor = db.cursor()
    headers = query["headers"][2:]

    things = {
        "Architecture": {"age": 45, "gender": "M"},
        "Art": {"age": 38, "gender": "W"},
        "Business": {"age": 42, "gender": "M"},
        "Crime": {"age": 48, "gender": "M"},
        "Entertainment": {"age": 32, "gender": "W"},
        "Health": {"age": 45, "gender": "W"},
        "Law": {"age": 45, "gender": "M"},
        "Lifestyle": {"age": 35, "gender": "W"},
        "Politics": {"age": 50, "gender": "M"},
        "Sports": {"age": 38, "gender": "M"},
        "Technology": {"age": 30, "gender": "M"},
    }

    totalAge = 0
    genderCount = {"M": 0, "W": 0}

    for header in headers:
        totalAge += things[header]["age"]
        genderCount[things[header]["gender"]] += 1

    sql = """
        UPDATE user_recommendation_index SET age = %s, gender = %s WHERE (user_id = %s)
    """
    cursor.execute(
        sql,
        (totalAge / len(headers), sorted(genderCount.items())[0][0], query["user_id"]),
    )
    db.commit()


# this function creates a new record for when a user reacts to an article
def user_article_reaction_create(db, query: dict):
    cursor = db.cursor(buffered=True)
    reaction_id = str(uuid4())
    # Check for existing interaction (one query with JOIN)
    check_sql = """
        SELECT *
        FROM user_article_interactions uai
        JOIN article_reaction_information ari ON uai.reaction_id = ari.reaction_id
        WHERE uai.user_id = %s AND uai.article_id = %s AND interaction = 4
    """
    cursor.execute(check_sql, (query["user_id"], query["article_id"]))
    exists = cursor.fetchone() is not None

    if exists:
        delete_sql = """
            DELETE FROM article_reaction_information
            WHERE reaction_id IN (
                SELECT reaction_id
                FROM user_article_interactions
                WHERE user_id = %s AND article_id = %s AND interaction = 4
            )
        """
        cursor.execute(delete_sql, (query["user_id"], query["article_id"]))

        delete_sql = """
            DELETE FROM user_article_interactions
            WHERE user_id = %s AND article_id = %s AND interaction = %s
        """
        cursor.execute(
            delete_sql,
            (
                query["user_id"],
                query["article_id"],
                4,
            ),
        )

    # Insert new interaction (using prepared statement)
    insert_sql = """
        INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(
        insert_sql,
        (
            query["user_id"],
            reaction_id,
            int(datetime.now().timestamp()),
            query["article_id"],
            4,
        ),
    )

    insert_sql = """
        INSERT INTO article_reaction_information (reaction_id, reaction_sentiment)
        VALUES (%s, %s)
    """
    cursor.execute(insert_sql, (reaction_id, query["reaction_sentiment"]))

    db.commit()
    cursor.execute(
        """
    SELECT reaction_sentiment, COUNT(*) AS count
    FROM user_article_interactions uai
    JOIN article_reaction_information ari ON uai.reaction_id = ari.reaction_id
    WHERE uai.article_id = %s
    GROUP BY reaction_sentiment
  """,
        (query["article_id"],),
    )

    reactions = {"love": 0, "smile": 0, "pensive": 0, "surprised": 0, "angry": 0}
    for row in cursor.fetchall():
        sentiment = row[0]
        count = row[1]
        if sentiment == 1.0:
            reactions["love"] += 1
        elif sentiment == 0.75:
            reactions["smile"] += 1
        elif sentiment == 0.3:
            reactions["pensive"] += 1
        elif sentiment == 0.5:
            reactions["surprised"] += 1
        elif sentiment == 0.0:
            reactions["angry"] += 1
    return reactions


# this function creates a new record for when a user saves an article
async def user_save_article(db, query: dict):
    cursor = db.cursor()
    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        int(datetime.now().timestamp()),
        query["article_id"],
        5,
    )
    cursor.execute(sql, val)

    db.commit()

    return True


# this function creates a new record for when a user unsave an article
async def user_unsave_article(db, query: dict):
    cursor = db.cursor()
    cursor = db.cursor()

    sql = "DELETE FROM user_article_interactions WHERE user_id = %s AND article_id = %s AND interaction = %s"
    val = (
        query["user_id"],
        query["article_id"],
        5,
    )
    cursor.execute(sql, val)

    db.commit()

    return True


# this function posts reaction information to the database
def post_reaction_information(db, query: dict):
    cursor = db.cursor()
    cursor = db.cursor()

    sql = (
        "SELECT * FROM user_article_interactions WHERE user_id = %s AND article_id = %s"
    )
    val = (
        query["user_id"],
        query["article_id"],
    )
    cursor.execute(sql, val)
    # TODO: this

    db.commit()

    return True


# this function gets article interaction information from the database
def get_article_interaction_information(db, query: dict):
    # cursor = db.cursor()
    # article_id = query["article_id"]
    # user_id = query["user_id"]

    # sql = "SELECT * FROM user_article_interactions WHERE article_id=%s"
    # cursor.execute(
    #     sql,
    #     (article_id,),
    # )
    # results = cursor.fetchall()
    # saved = []
    # for result in results:
    #     if result[4] == 5 and result[0] == user_id:
    #         saved.append(result)

    # reaction_dbs = []

    # for interaction in range(1, 5):
    #     if interaction == 1:
    #         table_name = "article_view_information"
    #         field_name = "view_seconds"
    #     elif interaction == 2:
    #         table_name = "article_scroll_information"
    #         field_name = "scroll_depth"
    #     elif interaction == 3:
    #         table_name = "article_comment_information"
    #         field_name = "comment"
    #     elif interaction == 4:
    #         table_name = "article_reaction_information"
    #         field_name = "reaction_sentiment"
    #     sql = f"""
    #         SELECT user_article_interactions.user_id, user_article_interactions.reaction_id, user_article_interactions.timestamp, user_article_interactions.article_id, user_article_interactions.interaction, {table_name}.{field_name}
    #         FROM {table_name}
    #         INNER JOIN user_article_interactions ON user_article_interactions.reaction_id={table_name}.reaction_id
    #     """
    #     cursor.execute(sql)
    #     reaction_dbs.append(cursor.fetchall())
    # reaction_dbs.append(saved)
    # return reaction_dbs

    # optimised version underneath

    cursor = db.cursor()
    article_id = query["article_id"]
    user_id = query["user_id"]

    # Optimized single query with UNION ALL
    sql = """
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            avi.view_seconds
        FROM 
            user_article_interactions uai
        JOIN 
            article_view_information avi ON uai.reaction_id = avi.reaction_id
        WHERE 
            uai.article_id = %s
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            asi.scroll_depth
        FROM 
            user_article_interactions uai
        JOIN 
            article_scroll_information asi ON uai.reaction_id = asi.reaction_id
        WHERE 
            uai.article_id = %s
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            aci.comment
        FROM 
            user_article_interactions uai
        JOIN 
            article_comment_information aci ON uai.reaction_id = aci.reaction_id
        WHERE 
            uai.article_id = %s
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            ari.reaction_sentiment
        FROM 
            user_article_interactions uai
        JOIN 
            article_reaction_information ari ON uai.reaction_id = ari.reaction_id
        WHERE 
            uai.article_id = %s
        UNION ALL 
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            NULL 
        FROM 
            user_article_interactions uai
        WHERE 
            uai.article_id = %s AND uai.interaction = 5;
    """

    cursor.execute(sql, (article_id, article_id, article_id, article_id, article_id))
    results = cursor.fetchall()

    # Group results by interaction type
    reaction_dbs = {}
    for row in results:
        interaction = row[4]
        if interaction not in reaction_dbs:
            reaction_dbs[interaction] = []
        reaction_dbs[interaction].append(row)

    # Handle saved articles
    saved_articles = [row for row in results if row[4] == 5 and row[0] == user_id]
    reaction_dbs[5] = saved_articles

    return list(reaction_dbs.values())


# this function gets article details and interactions from the database
def get_article_details_and_interactions(db, query: dict):
    # really optimised single query to search for articles and interactions! (7s -> 3s)
    article_id = query["article_id"]
    user_id = query["user_id"]

    sql = """
    SELECT 
        a.article_id, 
        a.title, 
        a.body, 
        a.author_id, 
        a.created_at, 
        a.topic, 
        a.country, 
        a.content_form, 
        a.image_uri,
        au.author_name,
        ag.agency_name,
        uai.user_id, 
        uai.reaction_id, 
        uai.timestamp, 
        uai.interaction, 
        avi.view_seconds,
        asi.scroll_depth,
        aci.comment,
        ari.reaction_sentiment
    FROM 
        articles a
    JOIN 
        authors au ON a.author_id = au.author_id
    JOIN 
        agencies ag ON au.agency_id = ag.agency_id
    LEFT JOIN 
        user_article_interactions uai ON uai.article_id = a.article_id
    LEFT JOIN 
        article_view_information avi ON uai.reaction_id = avi.reaction_id
    LEFT JOIN 
        article_scroll_information asi ON uai.reaction_id = asi.reaction_id
    LEFT JOIN 
        article_comment_information aci ON uai.reaction_id = aci.reaction_id
    LEFT JOIN
        article_reaction_information ari ON uai.reaction_id = ari.reaction_id
    WHERE 
        a.article_id = %s
    """

    cursor = db.cursor()
    cursor.execute(sql, (article_id,))

    results = cursor.fetchall()

    article = None
    interactions = {
        "post_saved": False,
        "reactions": {"love": 0, "smile": 0, "pensive": 0, "surprised": 0, "angry": 0},
        "current_reaction": "",
    }

    for row in results:
        # Extract article details
        if not article:
            article = {
                "article_id": row[0],
                "title": row[1].replace("\n", ""),
                "author": row[9],
                "body": row[2],
                "company": row[10],
                "created_at": row[4],
                "verified": True,
                "live": False,
                "image_uri": row[8],
            }

        # Extract interaction details
        if row[11] is not None:  # Check if interaction data exists
            if row[14] == 5 and row[11] == user_id:
                interactions["post_saved"] = True

            if row[14] == 4:
                if row[18] == 1.0:
                    if row[11] == user_id:
                        interactions["current_reaction"] = "love"

                    interactions["reactions"]["love"] += 1
                elif row[18] == 0.75:
                    if row[11] == user_id:
                        interactions["current_reaction"] = "smile"
                    interactions["reactions"]["smile"] += 1
                elif row[18] == 0.3:
                    if row[11] == user_id:
                        interactions["current_reaction"] = "pensive"
                    interactions["reactions"]["pensive"] += 1
                elif row[18] == 0.5:
                    if row[11] == user_id:
                        interactions["current_reaction"] = "suprised"
                    interactions["reactions"]["surprised"] += 1
                elif row[18] == 0.0:
                    if row[11] == user_id:
                        interactions["current_reaction"] = "angry"
                    interactions["reactions"]["angry"] += 1

    return {"article_info": article, "reaction_info": interactions}


# this function gets articles of a specific topic from the database
def get_articles_of_topic(db, query: dict):
    cursor = db.cursor()
    bar = "%" + query["topic"] + "%"
    sql = """SELECT
        a.article_id,
        a.title,
        a.body,
        a.author_id,
        a.created_at,
        a.topic,
        a.country,
        a.content_form,
        a.image_uri,
        au.author_name,
        ag.agency_name
        FROM articles a
        INNER JOIN authors au ON a.author_id = au.author_id
        LEFT JOIN agencies ag ON au.agency_id = ag.agency_id
        WHERE topic LIKE %s;"""
    cursor.execute(sql, (bar,))

    results = cursor.fetchall()
    articles = [
        {
            "article_id": row[0],
            "title": row[1].replace("\n", ""),
            "author": row[9],
            "company": row[10],
            "created_at": row[4],
            "verified": True,
            "live": False,
            "image_uri": row[8],
        }
        for row in results
    ]
    return articles


# this function gets all articles from the database
async def get_all_articles():
    # cursor = db.cursor()
    # sql = "SELECT * FROM articles"
    # cursor.execute(sql)
    # articles = cursor.fetchall()
    # sql = "SELECT * FROM authors"
    # cursor.execute(sql)
    # authors = cursor.fetchall()
    # sql = "SELECT * FROM agencies"
    # cursor.execute(sql)
    # agencies = cursor.fetchall()
    # authors = {
    #     author_id: {"agency_id": agency_id, "author_name": author_name}
    #     for author_id, agency_id, author_name in authors
    # }
    # agencies = {agency_id: agency_name for agency_id, agency_name in agencies}
    # articles = [
    #     {
    #         "article_id": article_id,
    #         "title": title.replace("\n", ""),
    #         "author": authors[author_id]["author_name"],
    #         "company": agencies[authors[author_id]["agency_id"]],
    #         "created_at": created_at,
    #         "verified": True,
    #         "live": False,
    #         "image_uri": image_uri,
    #     }
    #     for article_id, title, body, author_id, created_at, topic, country, content_form, image_uri in articles
    # ]
    # return articles

    # optimised version underneath
    starttime = datetime.now()
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        sql = """
        SELECT
        a.article_id,
        a.title,
        a.body,
        a.author_id,
        a.created_at,
        a.topic,
        a.country,
        a.content_form,
        a.image_uri,
        au.author_name,
        ag.agency_name
        FROM articles a
        INNER JOIN authors au ON a.author_id = au.author_id
        LEFT JOIN agencies ag ON au.agency_id = ag.agency_id;
        """
        await cur.execute(sql)
        results = await cur.fetchall()

        articles = [
            {
                "article_id": row[0],
                "title": row[1].replace("\n", ""),
                "author": row[9],
                "company": row[10],
                "created_at": row[4],
                "verified": True,
                "live": False,
                "image_uri": row[8],
                "topic": row[5],
                "country": row[6],
            }
            for row in results
        ]
        return articles


# this function gets saved articles for a specific user from the database
def get_saved_articles(db, query: dict):
    cursor = db.cursor()
    user_id = query["user_id"]
    sql = "SELECT * FROM authors"
    cursor.execute(sql)
    authors = cursor.fetchall()
    sql = "SELECT * FROM agencies"
    cursor.execute(sql)
    agencies = cursor.fetchall()
    authors = {
        author_id: {"agency_id": agency_id, "author_name": author_name}
        for author_id, agency_id, author_name in authors
    }
    agencies = {agency_id: agency_name for agency_id, agency_name in agencies}
    sql = "SELECT * FROM user_article_interactions WHERE user_id=%s AND interaction=%s"
    cursor.execute(
        sql,
        (
            user_id,
            5,
        ),
    )
    results = cursor.fetchall()
    article_ids = []
    for result in results:
        article_ids.append(result[3])
    if len(article_ids) == 0:
        return []
    placeholders = ",".join(["%s"] * len(article_ids))
    sql = f"SELECT * FROM articles WHERE article_id IN ({placeholders})"

    cursor.execute(sql, article_ids)

    articles = [
        {
            "article_id": article_id,
            "title": title.replace("\n", ""),
            "author": authors[author_id]["author_name"],
            "body": body,
            "company": agencies[authors[author_id]["agency_id"]],
            "created_at": created_at,
            "verified": True,
            "live": False,
            "image_uri": image_uri,
        }
        for article_id, title, body, author_id, created_at, topic, country, content_form, image_uri in cursor.fetchall()
    ]
    return articles


# this function gets article details from article id
def get_article_from_article_id(db, query: dict):
    # cursor = db.cursor()
    # sql = "SELECT * FROM articles WHERE article_id = %s"
    # cursor.execute(sql, (query["article_id"],))
    # articles = cursor.fetchall()
    # sql = "SELECT * FROM authors"
    # cursor.execute(sql)
    # authors = cursor.fetchall()
    # sql = "SELECT * FROM agencies"
    # cursor.execute(sql)
    # agencies = cursor.fetchall()
    # authors = {
    #     author_id: {"agency_id": agency_id, "author_name": author_name}
    #     for author_id, agency_id, author_name in authors
    # }
    # agencies = {agency_id: agency_name for agency_id, agency_name in agencies}
    # articles = [
    #     {
    #         "article_id": article_id,
    #         "title": title.replace("\n", ""),
    #         "author": authors[author_id]["author_name"],
    #         "body": body,
    #         "company": agencies[authors[author_id]["agency_id"]],
    #         "created_at": created_at,
    #         "verified": True,
    #         "live": False,
    #         "image_uri": image_uri,
    #     }
    #     for article_id, title, body, author_id, created_at, topic, country, content_form, image_uri in articles
    # ]
    # return articles[0]

    # optimised version underneath

    cursor = db.cursor()

    # Optimized single query with JOINs
    sql = """
        SELECT 
            a.article_id, 
            a.title, 
            a.body, 
            a.author_id, 
            a.created_at, 
            a.topic, 
            a.country, 
            a.content_form, 
            a.image_uri,
            au.author_name,
            ag.agency_name
        FROM 
            articles a
        JOIN 
            authors au ON a.author_id = au.author_id
        JOIN 
            agencies ag ON au.agency_id = ag.agency_id
        WHERE 
            a.article_id = %s
    """

    cursor.execute(sql, (query["article_id"],))
    article = cursor.fetchone()

    if article:
        return {
            "article_id": article[0],
            "title": article[1].replace("\n", ""),
            "author": article[9],
            "body": article[2],
            "company": article[10],
            "created_at": article[4],
            "verified": True,
            "live": False,
            "image_uri": article[8],
        }
    else:
        return None


# this function gets recent articles from the database
def get_recent_articles(db):
    cursor = db.cursor()
    sql = "SELECT * FROM articles"
    cursor.execute(sql)


# gets x number of user article interactions from the database


def get_x_user_article_interactions(db, query: dict):
    cursor = db.cursor()
    x = query["x"]  # number of articles
    user_id = query["user_id"]

    sql = """
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            avi.view_seconds AS engagement_data 
        FROM 
            user_article_interactions uai
        JOIN 
            article_view_information avi ON uai.reaction_id = avi.reaction_id
        WHERE 
            uai.user_id = %s
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            asi.scroll_depth AS engagement_data
        FROM 
            user_article_interactions uai
        JOIN 
            article_scroll_information asi ON uai.reaction_id = asi.reaction_id
        WHERE 
            uai.user_id = %s
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            aci.comment AS engagement_data
        FROM 
            user_article_interactions uai
        JOIN 
            article_comment_information aci ON uai.reaction_id = aci.reaction_id
        WHERE 
            uai.user_id = %s
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            ari.reaction_sentiment AS engagement_data
        FROM 
            user_article_interactions uai
        JOIN 
            article_reaction_information ari ON uai.reaction_id = ari.reaction_id
        WHERE 
            uai.user_id = %s
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            NULL AS engagement_data 
        FROM 
            user_article_interactions uai
        WHERE 
            uai.user_id = %s AND uai.interaction = 5
        ORDER BY timestamp DESC
        LIMIT 0, %s;
        """

    cursor.execute(sql, (user_id, user_id, user_id, user_id, user_id, x))

    results = cursor.fetchall()

    return results


# this function gets global users article interactions from the database
async def get_global_users_article_interactions():
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        sql = """
            SELECT 
                uai.user_id, 
                uai.reaction_id, 
                uai.timestamp, 
                uai.article_id, 
                uai.interaction, 
                avi.view_seconds AS engagement_data 
            FROM 
                user_article_interactions uai
            JOIN 
                article_view_information avi ON uai.reaction_id = avi.reaction_id
            UNION ALL
            SELECT 
                uai.user_id, 
                uai.reaction_id, 
                uai.timestamp, 
                uai.article_id, 
                uai.interaction, 
                asi.scroll_depth AS engagement_data
            FROM 
                user_article_interactions uai
            JOIN 
                article_scroll_information asi ON uai.reaction_id = asi.reaction_id
            UNION ALL
            SELECT 
                uai.user_id, 
                uai.reaction_id, 
                uai.timestamp, 
                uai.article_id, 
                uai.interaction, 
                aci.comment AS engagement_data
            FROM 
                user_article_interactions uai
            JOIN 
                article_comment_information aci ON uai.reaction_id = aci.reaction_id
            UNION ALL
            SELECT 
                uai.user_id, 
                uai.reaction_id, 
                uai.timestamp, 
                uai.article_id, 
                uai.interaction, 
                ari.reaction_sentiment AS engagement_data
            FROM 
                user_article_interactions uai
            JOIN 
                article_reaction_information ari ON uai.reaction_id = ari.reaction_id
            UNION ALL
            SELECT 
                uai.user_id, 
                uai.reaction_id, 
                uai.timestamp, 
                uai.article_id, 
                uai.interaction, 
                NULL AS engagement_data 
            FROM 
                user_article_interactions uai
            WHERE 
                uai.interaction = 5
            """
        await cur.execute(sql)

        results = await cur.fetchall()
        return results


# this function gets users article interactions from the database
def get_users_article_interactions(db, query: dict):
    cursor = db.cursor()
    users = tuple(query["users"])
    if len(users) == 0:
        raise IndexError

    users = str(users)
    if users[-2] == ",":
        users = users[:-2] + users[-1:]

    sql = f"""
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            avi.view_seconds AS engagement_data 
        FROM 
            user_article_interactions uai
        JOIN 
            article_view_information avi ON uai.reaction_id = avi.reaction_id
        WHERE 
            uai.user_id IN {users}
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            asi.scroll_depth AS engagement_data
        FROM 
            user_article_interactions uai
        JOIN 
            article_scroll_information asi ON uai.reaction_id = asi.reaction_id
        WHERE 
            uai.user_id IN {users}
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            aci.comment AS engagement_data
        FROM 
            user_article_interactions uai
        JOIN 
            article_comment_information aci ON uai.reaction_id = aci.reaction_id
        WHERE 
            uai.user_id IN {users}
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            ari.reaction_sentiment AS engagement_data
        FROM 
            user_article_interactions uai
        JOIN 
            article_reaction_information ari ON uai.reaction_id = ari.reaction_id
        WHERE 
            uai.user_id IN {users}
        UNION ALL
        SELECT 
            uai.user_id, 
            uai.reaction_id, 
            uai.timestamp, 
            uai.article_id, 
            uai.interaction, 
            NULL AS engagement_data 
        FROM 
            user_article_interactions uai
        WHERE 
            uai.user_id IN {users} AND uai.interaction = 5
        """
    cursor.execute(sql)

    results = cursor.fetchall()

    return results
