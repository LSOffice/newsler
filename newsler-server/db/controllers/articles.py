from uuid import uuid4
from datetime import datetime

import bcrypt

salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()


def user_article_view_create(db, query: dict):
    cursor = db.cursor()

    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        datetime.now().timestamp(),
        query["article_id"],
        1,
    )
    cursor.execute(sql, val)

    sql = "INSERT INTO article_view_information (reaction_id, view_seconds) VALUES (%s, %s)"
    val = (reaction_id, query["view_seconds"])
    cursor.execute(sql, val)
    db.commit()

    return True


def user_article_scroll_complete(db, query: dict):
    cursor = db.cursor()

    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        datetime.now().timestamp(),
        query["article_id"],
        2,
    )
    cursor.execute(sql, val)

    sql = "INSERT INTO article_scroll_information (reaction_id, scroll_depth) VALUES (%s, %s)"
    val = (reaction_id, query["scroll_depth"])
    cursor.execute(sql, val)
    db.commit()

    return True


def user_article_comment_create(db, query: dict):
    cursor = db.cursor()

    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        datetime.now().timestamp(),
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


def user_article_reaction_create(db, query: dict):
    cursor = db.cursor()

    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        datetime.now().timestamp(),
        query["article_id"],
        4,
    )
    cursor.execute(sql, val)

    sql = "INSERT INTO article_reaction_information (reaction_id, reaction_sentiment) VALUES (%s, %s)"
    val = (reaction_id, query["reaction_sentiment"])
    cursor.execute(sql, val)
    db.commit()

    return True


def user_save_article(db, query: dict):
    cursor = db.cursor()
    print("received1")
    reaction_id = str(uuid4())
    sql = "INSERT INTO user_article_interactions (user_id, reaction_id, timestamp, article_id, interaction) VALUES (%s, %s, %s, %s, %s)"
    val = (
        query["user_id"],
        reaction_id,  # create new reaction id
        datetime.now().timestamp(),
        query["article_id"],
        5,
    )
    cursor.execute(sql, val)
    print("done")

    db.commit()

    return True


def user_unsave_article(db, query: dict):
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


def get_articles_of_topic(db, query: dict):
    cursor = db.cursor()
    bar = "%" + query["topic"] + "%"
    sql = "SELECT * FROM articles WHERE topic LIKE %s"
    cursor.execute(sql, (bar,))
    return cursor.fetchall()


def get_all_articles(db):
    cursor = db.cursor()
    sql = "SELECT * FROM articles"
    cursor.execute(sql)
    articles = cursor.fetchall()
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
    articles = [
        {
            "article_id": article_id,
            "title": title.replace("\n", ""),
            "author": authors[author_id]["author_name"],
            "company": agencies[authors[author_id]["agency_id"]],
            "created_at": created_at,
            "verified": True,
            "live": False,
            "image_uri": image_uri,
        }
        for article_id, title, body, author_id, created_at, topic, country, content_form, image_uri in articles
    ]
    return articles


def get_x_global_most_interacted_articles(db, query: dict):
    cursor = db.cursor()
    sql = "SELECT * FROM user_recommendation_index "


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
    print(articles)
    return articles


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


def get_recent_articles(db):
    cursor = db.cursor()
    # hard coded to be 14 days
    sql = "SELECT * FROM articles WHERE created_at>=%s"
    cursor.execute(sql, (int(datetime.now().timestamp() - 14 * 24 * 60 * 60),))
    return cursor.fetchall()


def get_x_user_article_interactions(db, query: dict):
    cursor = db.cursor()
    x = query["x"]  # number of articles
    user_id = query["user_id"]

    sql = "SELECT * FROM user_article_interactions WHERE user_id=%s ORDER BY ABS(timestamp) DESC LIMIT 0, %s"
    cursor.execute(
        sql,
        (
            user_id,
            x,
        ),
    )

    results = cursor.fetchall()

    return results


def get_users_article_interactions(db, query: dict):
    cursor = db.cursor()
    users = tuple(query["users"])
    if len(users) == 0:
        raise IndexError

    users = str(users)
    if users[-2] == ",":
        users = users[:-2] + users[-1:]
    sql = f"SELECT * FROM user_article_interactions WHERE user_id IN {users}"
    cursor.execute(sql)

    results = cursor.fetchall()

    return results
