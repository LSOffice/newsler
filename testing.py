import mysql.connector as mysql

HOST = "lesterhk.com"
DATABASE = "kevin_lucy"
USER = "kevin_lucy"
PASSWORD = "island2024"
mydb = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
mycursor = mydb.cursor()
import uuid
import random
from datetime import datetime
# import pandas as pd
# import google.generativeai as genai
import time
from googleapiclient.discovery import build

"""service = build(
    "customsearch", "v1", developerKey=""
)"""

# mycursor.execute("""CREATE TABLE assignments (
#     assignment_id VARCHAR(36) PRIMARY KEY,
#     classroom_id VARCHAR(36),
#     author_id VARCHAR(36),
#     title VARCHAR(1000),
#     description VARCHAR(1000),
#     assignment_type VARCHAR(10),
#     graded BOOLEAN,
#     FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id) ON DELETE CASCADE
# )""")

# mycursor.execute("""CREATE TABLE assignment_article (
#     assignment_id VARCHAR(36),
#     article_id VARCHAR(36),
#     FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE
# )""")

# mycursor.execute("""
#     CREATE TABLE user_quiz_progress (
#         user_id VARCHAR(36),
#         article_id VARCHAR(36),
#         assignment_id VARCHAR(36),
#         completed BOOLEAN,
#         FOREIGN KEY (user_id) REFERENCES users(user_id),
#         FOREIGN KEY (article_id) REFERENCES articles(article_id),
#         FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE
#     )
# """)

# mycursor.execute("""
#     CREATE TABLE article_quiz (
#         article_id VARCHAR(36),
#         questions VARCHAR(5000),
#         FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE
#     )
# """)


"""failed = []
for article in mycursor.fetchall():
    if article[8] != None:
        continue
    res = (
        service.cse()
        .list(
            q=str(article[2][:30]),
            cx="a5fbdd3f7d6464c06",
        )
        .execute()
    )
    
    try:
        if "cse_image" in res['items'][0]['pagemap']:
            image_uri = res['items'][0]['pagemap']['cse_image'][0]['src']
        else:
            image_uri = res['items'][0]['pagemap']['metatags'][0]['og:image']
        mycursor.execute("UPDATE articles SET image_uri = %s WHERE article_id = %s", (image_uri, article[0],))
        print(article[0])
        mydb.commit()
    except KeyError:
        failed.append(article[0])
print(failed)"""

# authors = {}
# agencies = {}

# genai.configure(api_key="AIzaSyD5c4aa27UDljFlpLfCIjUp-gvv8TKbxeI")
# df = pd.read_csv("dataset.csv")
# count = 0
# for index, row in df.iterrows():
#     if count == 6:
#         time.sleep(60)
#         count = 0
#     publication = row["publication"]
#     author = row["author"]
#     if random.randint(0, 1) == 0:
#         dt = datetime.today().timestamp() + random.randint(0, 604800)
#     else:
#         dt = datetime.today().timestamp() - random.randint(0, 604800)
#     created_at = int(dt)
#     topic = str(row["theme"]).capitalize()

#     body = row["content"]

#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content("In one line, tell me what the name of this article should be, just write the headline only, don't say anything else: " + body[:200])

#     title = response.text

#     response = model.generate_content("In one line, tell me which country this article is from (2-letter country code), don't say anything else: " + body[:200])

#     country = response.text

#     if publication not in agencies:
#         sql = "INSERT INTO agencies (agency_id, agency_name) VALUES (%s, %s)"
#         agency_id = str(uuid.uuid4())
#         val = (agency_id, publication,)
#         mycursor.execute(sql, val)
#         mydb.commit()
#         agencies[publication] = agency_id

#     if author not in authors:
#         sql = "INSERT INTO authors (author_id, agency_id, author_name) VALUES (%s, %s, %s)"
#         author_id = str(uuid.uuid4())
#         agency_id = agencies[publication]
#         val = (author_id, agency_id, author,)
#         mycursor.execute(sql, val)
#         mydb.commit()
#         authors[author] = author_id

#     sql = "INSERT INTO articles (article_id, title, body, author_id, created_at, topic, country, content_form) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#     val = (str(uuid.uuid4()), title, body, authors[author], created_at, topic, country, 0,)
#     mycursor.execute(sql, val)
#     mydb.commit()
#     print(row)
#     count += 1

# mycursor.execute(
#     """CREATE TABLE users (
#     user_id VARCHAR(36) NOT NULL PRIMARY KEY,
#     username VARCHAR(32) NOT NULL,
#     type ENUM('free', 'premium', 'admin') NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     display_name VARCHAR(32),
#     country VARCHAR(2),
# )"""
# )

# mycursor.execute(
#     """
# CREATE TABLE user_recommended (
#     user_id VARCHAR(36),
#     article_id VARCHAR(36),
#     timestamp INTEGER,
#     FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
#     FOREIGN KEY (article_id) REFERENCES articles(article_id)
# )
# """
# )

# mycursor.execute(
#     """CREATE TABLE classrooms (
#     classroom_id VARCHAR(36) NOT NULL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     description VARCHAR(1000)
# )"""
# )

# mycursor.execute(
#     """
# CREATE TABLE user_classrooms (
#     user_id VARCHAR(36) NOT NULL,
#     classroom_id VARCHAR(36) NOT NULL,
#     type ENUM('teacher', 'student') NOT NULL,
#     PRIMARY KEY (user_id, classroom_id),
#     FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
#     FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id) ON DELETE CASCADE
# );
#     """
# )

# mycursor.execute(
#     """CREATE TABLE user_search (
#     user_id VARCHAR(36) NOT NULL,
#     search_query VARCHAR(100) NOT NULL,
#     PRIMARY KEY (user_id, search_query),
#     FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
# )"""
# )

# mycursor.execute(
#     """CREATE TABLE authors (
#     author_id VARCHAR(36) NOT NULL PRIMARY KEY,
#     agency_id VARCHAR(36) NOT NULL,
#     author_name VARCHAR(255) NOT NULL
# )"""
# )

# mycursor.execute(
#     """CREATE TABLE agencies (
#     agency_id VARCHAR(36) NOT NULL PRIMARY KEY,
#     agency_name VARCHAR(255)
# )"""
# )

# mycursor.execute(
#     """
# CREATE TABLE articles (
#   article_id VARCHAR(36) PRIMARY KEY,
#   title VARCHAR(255),
#   body VARCHAR(65535),
#   author_id VARCHAR(36),
#   created_at INTEGER,
#   topic VARCHAR(30),
#   country VARCHAR(2),
#   content_form INTEGER(1),
#   FOREIGN KEY (author_id) REFERENCES authors(author_id)
# );"""
# )

# mycursor.execute(
#     """
# CREATE TABLE user_article_interactions (
#   user_id VARCHAR(36),
#   reaction_id VARCHAR(36) PRIMARY KEY,
#   timestamp INTEGER,
#   article_id VARCHAR(36),
#   interaction TINYINT NOT NULL,
#   FOREIGN KEY (user_id) REFERENCES users(user_id),
#   FOREIGN KEY (article_id) REFERENCES articles(article_id)
# )
# """
# )

# mycursor.execute(
#     """
# CREATE TABLE article_view_information (
#     reaction_id VARCHAR(36),
#     view_seconds INTEGER(255) NOT NULL,
#     FOREIGN KEY (reaction_id) REFERENCES user_article_interactions(reaction_id)
# )
# """
# )

# mycursor.execute(
#     """
# CREATE TABLE article_scroll_information (
#     reaction_id VARCHAR(36),
#     scroll_depth DOUBLE NOT NULL,
#     FOREIGN KEY (reaction_id) REFERENCES user_article_interactions(reaction_id)
# )
# """
# )

# mycursor.execute(
#     """
# CREATE TABLE article_comment_information (
#     reaction_id VARCHAR(36),
#     comment VARCHAR(255) NOT NULL,
#     FOREIGN KEY (reaction_id) REFERENCES user_article_interactions(reaction_id)
# )
# """
# )

# mycursor.execute(
#     """
# CREATE TABLE article_reaction_information (
#     reaction_id VARCHAR(36),
#     reaction_sentiment DOUBLE NOT NULL,
#     FOREIGN KEY (reaction_id) REFERENCES user_article_interactions(reaction_id)
# )
# """
# )


# mycursor.execute(
#     """
#   CREATE TABLE user_recommendation_index (
#     user_id VARCHAR(36),
#     device_type VARCHAR(50),
#     geolocation VARCHAR(100),
#     topical_interests VARCHAR(1000),
#     age INTEGER,
#     gender CHAR(1),
#     preferred_format VARCHAR(20),
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
#   )
# """
# )

# mycursor.execute(
#     """
#   CREATE TABLE user_recommendation_index (
#     user_id VARCHAR(36),
#     device_type VARCHAR(50),
#     geolocation VARCHAR(100),
#     topical_interests VARCHAR(1000),
#     age INTEGER,
#     gender CHAR(1),
#     preferred_format VARCHAR(20),
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
#   )
# """
# )

# mycursor.execute(
#     """
#     CREATE TABLE sessions (
#         user_id VARCHAR(36),
#         refresh_token VARCHAR(100),
#         refreshExpiresAt INTEGER,
#         session_token VARCHAR(100),
#         sessionExpiresAt INTEGER,
#         FOREIGN KEY (user_id) REFERENCES users(user_id)
#     )
# """
# )


# mycursor.execute("Show tables;")

# myresult = mycursor.fetchall()

# for x in myresult:
#     print(x)
