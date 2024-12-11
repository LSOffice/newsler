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

    db.commit()

    return True


def get_article_interaction_information(db, query: dict):
    cursor = db.cursor()
    reaction_id = query["reaction_id"]

    sql = "SELECT * FROM user_article_interactions WHERE reaction_id=%s"
    cursor.execute(sql, (reaction_id,))
    results = cursor.fetchall()
    if len(results) != 1:
        return ()
    result = results[0]

    interaction = result[4]
    if interaction == 1:
        table_name = "article_view_information"
        field_name = "view_seconds"
    elif interaction == 2:
        table_name = "article_scroll_information"
        field_name = "scroll_depth"
    elif interaction == 3:
        table_name = "article_comment_information"
        field_name = "comment"
    elif interaction == 4:
        table_name = "article_reaction_information"
        field_name = "reaction_sentiment"
    elif interaction == 5:
        return result
    sql = f"""
        SELECT user_article_interactions.user_id, user_article_interactions.reaction_id, user_article_interactions.timestamp, user_article_interactions.article_id, user_article_interactions.interaction, {table_name}.{field_name}
        FROM {table_name}
        INNER JOIN user_article_interactions ON user_article_interactions.reaction_id={table_name}.reaction_id
        WHERE user_article_interactions.reaction_id=%s;
    """
    cursor.execute(
        sql,
        (reaction_id,),
    )
    return cursor.fetchone()


def get_articles_of_topic(db, query: dict):
    cursor = db.cursor()
    bar = "%" + query["topic"] + "%"
    sql = "SELECT * FROM articles WHERE topic LIKE %s"
    cursor.execute(sql, (bar,))
    return cursor.fetchall()


def get_x_global_most_interacted_articles(db, query: dict):
    cursor = db.cursor()
    sql = "SELECT * FROM user_recommendation_index "


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
    print(users)
    if len(users) == 0:
        raise IndexError

    users = str(users)
    if users[-2] == ",":
        users = users[:-2] + users[-1:]
    sql = f"SELECT * FROM user_article_interactions WHERE user_id IN {users}"
    cursor.execute(sql)

    results = cursor.fetchall()

    return results
