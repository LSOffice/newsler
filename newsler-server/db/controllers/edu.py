import json
import os
import random
import string
from datetime import datetime
from shlex import join
from uuid import uuid4

import aiomysql
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


async def user_edu_load(query: dict):
    # user_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        sql = "SELECT * FROM user_edu WHERE user_id = %s"
        await cur.execute(sql, (query["user_id"],))
        result = await cur.fetchall()
        if len(result) == 0:
            await cur.execute(
                "INSERT INTO user_edu (user_id, edu_type) VALUES (%s, %s)",
                (query["user_id"], "student"),
            )
            await conn.commit()
            return "student", []
        else:
            sql = """SELECT uc.user_id, uc.classroom_id, uc.type, c.name, c.education_level, c.subject_code, u.username FROM user_classrooms uc INNER JOIN classrooms c ON c.classroom_id = uc.classroom_id INNER JOIN users u ON u.user_id = uc.user_id"""
            await cur.execute(sql)
            user_type = result[0][1]
            results = [
                {
                    "user_id": row[0],
                    "classroom_id": row[1],
                    "type": row[2],
                    "name": row[3],
                    "education_level": row[4],
                    "subject_code": row[5],
                    "username": row[6],
                }
                for row in await cur.fetchall()
            ]
            user_classroom_ids = []
            classrooms = {}
            for result in results:
                if result["user_id"] == query["user_id"]:
                    user_classroom_ids.append(result["classroom_id"])
                if not result["classroom_id"] in classrooms:
                    classrooms[result["classroom_id"]] = {
                        "education_level": result["education_level"],
                        "subject_code": result["subject_code"],
                        "name": result["name"],
                        "teacher": "",
                    }
                if result["type"] == "teacher":
                    classrooms[result["classroom_id"]]["teacher"] = result["username"]

            await cur.execute(
                "SELECT username FROM users WHERE user_id = %s", (query["user_id"],)
            )
            username = await cur.fetchall()
            username = username[0][0]

            user_classrooms = []
            for classroom_id in user_classroom_ids:
                classroom = classrooms[classroom_id]
                classroom["classroom_id"] = classroom_id
                user_classrooms.append(classroom)

            return user_type, user_classrooms
    conn.close()


async def user_create_classroom(query: dict):
    # classroom_name, education_level, subject_code
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT * FROM classrooms WHERE name = %s", (query["classroom_name"],)
        )

        results = await cur.fetchall()
        if len(results) != 0:
            return [False]

        classroom_id = str(uuid4())
        join_code = (
            "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
            ),
        )
        await cur.execute(
            "INSERT INTO classrooms (classroom_id, name, education_level, subject_code, join_code) VALUES (%s, %s, %s, %s, %s)",
            (
                classroom_id,
                query["classroom_name"],
                query["educational_level"],
                query["subject_code"],
                join_code,
            ),
        )
        await conn.commit()
        return [True, classroom_id, join_code]
    conn.close()


async def user_load_classroom(query: dict) -> dict:
    # classroom_id, user_id, type
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT * FROM classrooms WHERE classroom_id = %s", (query["classroom_id"],)
        )

        results = await cur.fetchall()
        if len(results) != 1:
            return {"success": False}

        classroom_detail = {
            "name": results[0][1],
            "education_level": results[0][2],
            "subject_code": results[0][3],
            "join_code": results[0][4],
        }

        await cur.execute(
            "SELECT uc.user_id, uc.classroom_id, uc.type, u.username FROM user_classrooms uc INNER JOIN users u ON u.user_id = uc.user_id WHERE classroom_id = %s",
            (query["classroom_id"],),
        )
        results = await cur.fetchall()
        if len(results) == 0:
            return {"success": False}
        user_type = ""
        teacher = ""
        for result in results:
            if result[0] == query["user_id"]:
                user_type = result[2]
            if result[2] == "teacher":
                teacher = result[3]
        if user_type == "" or teacher == "":
            return {"success": False}
        classroom_detail["teacher"] = teacher

        await cur.execute(
            "SELECT * FROM assignments WHERE classroom_id = %s",
            (query["classroom_id"],),
        )

        assignments = []
        results = await cur.fetchall()
        await cur.execute(
            "SELECT aa.assignment_id, a.body, a.title, a.image_uri, aa.article_id FROM assignment_article aa INNER JOIN articles a ON aa.article_id = a.article_id",
        )
        articles = await cur.fetchall()

        for assignment in results:
            assignment_id = assignment[0]
            assignment_type = assignment[5]

            if assignment_type == "share":
                assignments.append(
                    {
                        "assignment_id": assignment_id,
                        "author_id": assignment[2],
                        "title": assignment[3],
                        "description": assignment[4],
                        "timestamp": assignment[7],
                        "type": assignment_type,
                        "article": [
                            {
                                "title": article[2],
                                "image_uri": article[3],
                                "length": round(len(str(article[1]).split()) / 200),
                                "article_id": article[4],
                            }
                            for article in articles
                            if article[0] == assignment_id
                        ],
                    }
                )
            elif assignment_type == "task":
                assignments.append(
                    {
                        "assignment_id": assignment_id,
                        "author_id": assignment[2],
                        "title": assignment[3],
                        "description": assignment[4],
                        "timestamp": assignment[7],
                        "type": assignment_type,
                        "graded": assignment[6],
                        "article": [
                            {
                                "title": article[2],
                                "image_uri": article[3],
                                "length": round(len(str(article[1]).split()) / 200),
                                "article_id": article[4],
                            }
                            for article in articles
                            if article[0] == assignment_id
                        ],
                    }
                )

        return {
            "success": True,
            "details": classroom_detail,
            "user_type": user_type,
            "assignments": sorted(
                assignments, key=lambda x: x["timestamp"], reverse=True
            ),
        }
    conn.close()


async def user_join_classroom(query: dict):
    # user_id, join_code, type
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT * FROM classrooms WHERE join_code = %s", (query["join_code"],)
        )
        results = await cur.fetchall()
        if len(results) != 1:
            return False

        classroom_id = results[0][0]

        await cur.execute(
            "SELECT * FROM user_classrooms WHERE user_id = %s AND classroom_id = %s",
            (query["user_id"], classroom_id),
        )

        results = await cur.fetchall()
        if len(results) == 1:
            return False

        await cur.execute(
            "INSERT INTO user_classrooms (user_id, classroom_id, type) VALUES (%s, %s, %s)",
            (query["user_id"], classroom_id, query["type"]),
        )
        await conn.commit()
        return True
    conn.close()


async def user_leave_classroom(query: dict):
    # user_id, classroom_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT * FROM user_classrooms WHERE user_id = %s AND classroom_id = %s",
            (query["user_id"], query["classroom_id"]),
        )

        results = await cur.fetchall()
        if len(results) == 0:
            return False
        if results[0][2] == "teacher":
            return False

        await cur.execute(
            "DELETE FROM user_classrooms WHERE user_id = %s AND classroom_id = %s",
            (query["user_id"], query["classroom_id"]),
        )
        return True
    conn.close()


async def search_articles(query: dict):
    # title
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        bar = "%" + query["title"] + "%"
        await cur.execute("SELECT * FROM articles WHERE title LIKE %s", (bar,))
        results = await cur.fetchall()
        return [
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


async def user_create_assignment(query: dict):
    # classroom_id, author_id, title, description, assignment_type, graded, articles
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        assignment_id = str(uuid4())
        await cur.execute(
            "INSERT INTO assignments (assignment_id, classroom_id, author_id, title, description, assignment_type, graded, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                assignment_id,
                query["classroom_id"],
                query["author_id"],
                query["title"],
                query["description"],
                query["assignment_type"],
                query["graded"],
                int(datetime.now().timestamp()),
            ),
        )

        data = []
        for article_id in query["articles"]:
            data.append(
                (
                    assignment_id,
                    article_id,
                )
            )

        await cur.executemany(
            "INSERT INTO assignment_article (assignment_id, article_id) VALUES (%s, %s)",
            data,
        )
        await conn.commit()

        return True
    conn.close()


async def user_5_recently_viewed_articles(query: dict):
    # user_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        assignment_id = str(uuid4())
        await cur.execute(
            """SELECT uai.article_id, a.title, a.image_uri 
FROM user_article_interactions uai 
INNER JOIN articles a ON a.article_id = uai.article_id 
WHERE uai.interaction = %s 
  AND uai.user_id = %s 
ORDER BY uai.timestamp DESC;""",
            (1, query["user_id"]),
        )
        result = await cur.fetchall()
        article_ids = set()
        articles = []

        for row in result:
            if len(articles) == 5:
                break
            article_id = row[0]
            if article_id not in article_ids:
                articles.append(
                    {"article_id": article_id, "title": row[1], "image_uri": row[2]}
                )
                article_ids.add(article_id)

        return articles
    conn.close()


async def user_load_assignment(query: dict):
    # assignment_id, user_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        assignment_id = query["assignment_id"]
        user_id = query["user_id"]

        await cur.execute("SELECT * FROM user_edu ue WHERE user_id = %s", (user_id,))
        result = await cur.fetchall()
        if len(result) != 1:
            return {"success": False}
        user_type = result[0][1]

        if user_type == "student":

            await cur.execute(
                "SELECT a.author_id, a.title, a.description, a.assignment_type, a.graded, a.timestamp, u.username, a.assignment_id FROM assignments a INNER JOIN users u ON u.user_id = a.author_id WHERE a.assignment_id = %s",
                (assignment_id,),
            )
            result = await cur.fetchall()
            if len(result) != 1:
                print("abcd")
                return {"success": False}

            await cur.execute(
                "SELECT * FROM user_quiz_progress WHERE user_id = %s AND assignment_id = %s",
                (
                    user_id,
                    assignment_id,
                ),
            )
            result1 = await cur.fetchall()
            if len(result1) != 1:
                completed = False
            else:
                if result1[0][3] == -1:
                    completed = False
                else:
                    completed = True

            assignment = result[0]
            assignment_details = {
                "author": assignment[6],
                "title": assignment[1],
                "description": assignment[2],
                "assignment_type": assignment[3],
                "graded": assignment[4],
                "timestamp": assignment[5],
                "completed": completed,
                "user_type": user_type,
            }

            await cur.execute(
                "SELECT * FROM assignment_article WHERE assignment_id = %s",
                (assignment_id,),
            )
            result = await cur.fetchall()
            article_id_list = ""
            for article_id in result:
                article_id_list += "'" + article_id[1] + "'" + ", "
            article_id_list = article_id_list[:-2]
            await cur.execute(
                "SELECT aa.assignment_id, a.body, a.title, a.image_uri, aa.article_id FROM assignment_article aa INNER JOIN articles a ON aa.article_id = a.article_id WHERE a.article_id IN ("
                + article_id_list
                + ")",
            )
            result = await cur.fetchall()
            article_ids = []
            articles = []
            for article in result:
                if article[4] in article_ids:
                    continue
                articles.append(
                    {
                        "title": article[2],
                        "image_uri": article[3],
                        "length": round(len(str(article[1]).split()) / 200),
                        "article_id": article[4],
                        "body": article[1],
                    }
                )
                article_ids.append(article[4])
            return {"success": True, "detail": assignment_details, "articles": articles}
        else:
            await cur.execute(
                "SELECT a.author_id, a.title, a.description, a.assignment_type, a.graded, a.timestamp, u.username, a.assignment_id FROM assignments a INNER JOIN users u ON u.user_id = a.author_id WHERE a.assignment_id = %s",
                (assignment_id,),
            )
            result = await cur.fetchall()
            if len(result) != 1:
                return {"success": False}

            assignment = result[0]
            assignment_details = {
                "author": assignment[6],
                "title": assignment[1],
                "description": assignment[2],
                "assignment_type": assignment[3],
                "graded": assignment[4],
                "timestamp": assignment[5],
                "user_type": user_type,
            }

            await cur.execute(
                "SELECT * FROM assignments WHERE assignment_id = %s", (assignment_id,)
            )
            result = await cur.fetchall()
            classroom_id = result[0][1]

            await cur.execute(
                "SELECT uc.user_id, u.username FROM user_classrooms uc INNER JOIN users u ON u.user_id = uc.user_id WHERE uc.classroom_id = %s AND uc.type = %s",
                (classroom_id, "student"),
            )
            result = await cur.fetchall()

            student = {}
            for username in result:
                student[username[0]] = {
                    "username": username[1],
                    "started": False,
                    "completed": False,
                    "score": -1,
                }

            await cur.execute(
                "SELECT * FROM user_quiz_progress WHERE assignment_id = %s",
                (assignment_id,),
            )
            result = await cur.fetchall()

            for quiz_attempt in result:
                student[quiz_attempt[0]]["started"] = True
                if quiz_attempt[3] != 1:
                    student[quiz_attempt[0]]["completed"] = True
                    student[quiz_attempt[0]]["score"] = quiz_attempt[3]

            students = []
            for stud in student:
                students.append(
                    {
                        "student_id": stud,
                        "started": student[stud]["started"],
                        "completed": student[stud]["completed"],
                        "score": student[stud]["score"],
                        "username": student[stud]["username"],
                    }
                )

            return {"success": True, "detail": assignment_details, "students": students}

    conn.close()


async def user_load_quiz(query: dict):
    # assignment_id, user_id, article_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        assignment_id = query["assignment_id"]
        user_id = query["user_id"]
        article_id = query["article_id"]

        await cur.execute(
            "SELECT * FROM article_quiz WHERE article_id = %s", (article_id,)
        )
        result = await cur.fetchall()
        if len(result) != 1:
            await cur.execute(
                "SELECT * FROM articles WHERE article_id = %s", (article_id,)
            )
            result = await cur.fetchall()

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                "Generate a five question quiz in an array of JSON format of question, answer in a 4-choice multiple choice format for a news article with content (the fields should be 'question': string, 'choices': array, 'answer': string of the actual answer): "
                + result[0][2]
            )
            response_text = response.text.replace("```", "")
            response_text = response_text.replace("json", "")
            response_text = json.loads(response_text)
            await cur.execute(
                "INSERT INTO article_quiz (article_id, questions) VALUES (%s, %s)",
                (
                    article_id,
                    json.dumps(response_text),
                ),
            )
            quiz = response_text
        else:
            quiz = json.loads(result[0][1])

        await cur.execute(
            "SELECT * FROM user_quiz_progress WHERE article_id = %s AND user_id = %s AND assignment_id = %s",
            (article_id, user_id, assignment_id),
        )
        result = await cur.fetchall()
        if len(result) == 1:
            pass
        else:
            await cur.execute(
                "INSERT INTO user_quiz_progress (user_id, article_id, assignment_id, score) VALUES (%s, %s, %s, %s)",
                (user_id, article_id, assignment_id, -1),
            )

        await conn.commit()
        for question in quiz:
            del question["answer"]
        return {"success": True, "quiz": quiz}


async def user_delete_assignment(query: dict):
    # assignment_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        assignment_id = query["assignment_id"]

        await cur.execute(
            "DELETE FROM assignments WHERE assignment_id = %s", (assignment_id,)
        )
        await cur.execute(
            "DELETE FROM assignment_article WHERE assignment_id = %s", (assignment_id,)
        )
        await conn.commit()
        return True


async def user_finish_quiz(query: dict):
    # assignment_id, user_id, article_id, answers
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE"))  # type: ignore
    async with conn.cursor() as cur:
        assignment_id = query["assignment_id"]
        user_id = query["user_id"]
        article_id = query["article_id"]
        answers = json.loads(query["answers"])

        await cur.execute(
            "SELECT * FROM article_quiz WHERE article_id = %s", (article_id,)
        )
        result = await cur.fetchall()
        if len(result) != 1:
            return {"success": False}

        quiz = json.loads(result[0][1])
        if len(answers) != len(quiz):
            return {"success": False}

        letter_to_number = {"a": 0, "b": 1, "c": 2, "d": 3}

        correct = 0
        for i in range(len(answers)):
            if quiz[i]["choices"][letter_to_number[answers[i]]] == quiz[i]["answer"]:
                correct += 1
        await cur.execute(
            "UPDATE user_quiz_progress SET score = %s WHERE article_id = %s AND user_id = %s AND assignment_id = %s",
            (correct, article_id, user_id, assignment_id),
        )
        await conn.commit()

        return {"success": True, "score": correct}
