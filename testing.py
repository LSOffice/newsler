import mysql.connector as mysql

HOST = "lesterhk.com"
DATABASE = "kevin_lucy"
USER = "kevin_lucy"
PASSWORD = "island2024"
mydb = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
mycursor = mydb.cursor()
import uuid
from datetime import datetime

# mycursor.execute(
#     """CREATE TABLE users (
#     user_id VARCHAR(36) NOT NULL PRIMARY KEY,
#     username VARCHAR(32) NOT NULL,
#     type ENUM('free', 'premium', 'admin') NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     display_name VARCHAR(32)
# )"""
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
#   created_at TIMESTAMP,
#   FOREIGN KEY (author_id) REFERENCES authors(author_id)
# );"""
# )

# mycursor.execute(
#     """
# CREATE TABLE user_article_interactions (
#   user_id VARCHAR(36),
#   article_id VARCHAR(36),
#   reaction TINYINT NOT NULL,
#   comment VARCHAR(255),
#   view_seconds INTEGER(255) NOT NULL,
#   scroll_depth DOUBLE NOT NULL,
#   FOREIGN KEY (user_id) REFERENCES users(user_id),
#   FOREIGN KEY (article_id) REFERENCES articles(article_id)
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

sql = "INSERT INTO sessions (user_id, refresh_token, refreshExpiresAt, session_token, sessionExpiresAt) VALUES (%s, %s, %s, %s, %s)"
val = (
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    datetime.now().timestamp(),
    str(uuid.uuid4()),
    datetime.now().timestamp(),
)
mycursor.execute(sql, val)
mycursor.execute("Show tables;")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
