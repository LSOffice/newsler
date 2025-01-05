
from uuid import uuid4
import aiomysql
from dotenv import load_dotenv
import os
from datetime import datetime
import json

load_dotenv()

async def user_edu_load(query: dict):
    # user_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        sql = "SELECT * FROM user_edu WHERE user_id = %s"
        await cur.execute(sql, (query['user_id'],))
        result = await cur.fetchall()
        if len(result) == 0:
            await cur.execute("INSERT INTO user_edu (user_id, edu_type) VALUES (%s, %s)", (query['user_id'], "student"))
            await conn.commit()
            return "student", []
        else:
            sql = "SELECT * FROM user_classrooms WHERE user_id = %s"
            await cur.execute(sql, (query['user_id'],))
            results = await cur.fetchall()
            return result[0][1], results
    conn.close()

async def user_create_classroom(query: dict):
    # classroom_name, education_level, subject_code
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM classrooms WHERE name = %s", (query['classroom_name'],))

        results = await cur.fetchall()
        if len(results) != 0:
            return False
        
        classroom_id = str(uuid4())
        await cur.execute("INSERT INTO classrooms (classroom_id, name, education_level, subject_code) VALUES (%s, %s, %s, %s)", (classroom_id, query['classroom_name'], query['education_level'], query['subject_code']))
        return True
    conn.close()

async def user_load_classroom(query: dict) -> dict:
    # classroom_id, user_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM classrooms WHERE classroom_id = %s", (query['classroom_id'],))

        results = await cur.fetchall()
        if len(results) != 1:
            return {"success": False}
        
        classroom_detail = {
            "name": results[0][1],
            "education_level": results[0][2],
            "subject_code": results[0][3]
        }

        await cur.execute("SELECT * FROM user_classrooms WHERE user_id = %s AND classroom_id = %s", (query['user_id'], query['classroom_id']))
        results = await cur.fetchall()
        if len(results) != 1:
            return {"success": False}
        type = results[0][2]

        await cur.execute("SELECT * FROM assignments WHERE classroom_id = %s", (query['classroom_id'],))
        
        assignments = []
        results = await cur.fetchall()
        for assignment in results:
            assignment_id = assignment[0]
            assignment_type = assignment[5]

            await cur.execute("SELECT * FROM assignment_article WHERE assignment_id = %s", (assignment_id,))
            articles = await cur.fetchall()
            if assignment_type == "share":
                assignments.append({"assignment_id": assignment_id, "author_id": assignment[2], "title": assignment[3], "description": assignment[4], "timestamp": assignment[7], "type": assignment_type, "article": articles[0][1]})
            elif assignment_type == "task":
                assignments.append({"assignment_id": assignment_id, "author_id": assignment[2], "title": assignment[3], "description": assignment[4], "timestamp": assignment[7], "type": assignment_type, "articles": [article[1] for article in articles]})
        
        return {"success": True, "details": classroom_detail, "user_type": type, "assignments": sorted(assignments, key=lambda x: x['timestamp'], reverse=True)}
    conn.close()

async def user_join_classroom(query: dict):
    # user_id, classroom_id, type
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM user_classrooms WHERE user_id = %s AND classroom_id = %s", (query['user_id'], query['classroom_id']))

        results = await cur.fetchall()
        if len(results) == 1:
            return False
        
        await cur.execute("INSERT INTO user_classrooms (user_id, classroom_id, type) VALUES (%s, %s, %s)", (query['user_id'], query['classroom_id'], query['type']))
        return True
    conn.close()

async def user_leave_classroom(query: dict):
    # user_id, classroom_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM user_classrooms WHERE user_id = %s AND classroom_id = %s", (query['user_id'], query['classroom_id']))

        results = await cur.fetchall()
        if len(results) == 0:
            return False
        if results[0][2] == "teacher":
            return False

        await cur.execute("DELETE FROM user_classrooms WHERE user_id = %s AND classroom_id = %s", (query['user_id'], query['classroom_id']))
        return True
    conn.close()

async def search_articles(query: dict):
    # title
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
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
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        assignment_id = str(uuid4())
        await cur.execute("INSERT INTO assignments (assignment_id, classroom_id, author_id, title, description, assignment_type, graded, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (assignment_id, query['classroom_id'], query['author_id'], query['title'], query['description'], query['assignment_type'], query['graded'], int(datetime.now().timestamp())))

        data = []
        for article_id in query['articles']:
            data.append((assignment_id, article_id))
        
        await cur.executemany("INSERT INTO assignment_article (assignment_id, article_id) VALUES (%s, %s)", data)

        return True
    conn.close()

async def user_load_assignment(query: dict):
    # assignment_id, user_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        assignment_id = query['assignment_id']
        user_id = query['user_id']

        await cur.execute("SELECT * FROM user_edu WHERE user_id = %s", (user_id,))
        result = await cur.fetchall()
        if len(result) != 1:
            return {
                "success": False
            }
        user_type = result[0][1]
        
        await cur.execute("SELECT * FROM assignments WHERE assignment_id = %s", (assignment_id,))
        result = await cur.fetchall()
        if len(result) != 1:
            return {
                "success": False
            }
        
        assignment = result[0]
        assignment_details = {
            "assignment_id": assignment[0],
            "classroom_id": assignment[1],
            "author_id": assignment[2],
            "title": assignment[3],
            "description": assignment[4],
            "assignment_type": assignment[5],
            "graded": assignment[6],
            "timestamp": assignment[7]
        }

        await cur.execute("SELECT * FROM assignment_article WHERE assignment_id = %s", (assignment_id,))
        result = await cur.fetchall()

        data = []
        for article_id in result:
            data.append((article_id,))
        await cur.executemany("SELECT * FROM articles WHERE article_id = %s", data)
        result = await cur.fetchall()

        articles = [
            {
                "article_id": article[0],
                "title": article[1]
            }
            for article in result
        ]

        return {"success": False, "detail": assignment_details, "articles": articles}


    conn.close()

    # TODO: ^^ load quiz results too

async def user_load_quiz(query: dict):
    # assignment_id, user_id, article_id
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        assignment_id = query['assignment_id']
        user_id = query['user_id']
        article_id = query['article_id']

        await cur.execute("SELECT * FROM article_quiz WHERE article_id = %s", (article_id,))
        result = await cur.fetchall()
        if len(result) != 1:
            return {"success": False}

        quiz = json.load(result[0][1])

        await cur.execute("SELECT * FROM user_quiz_progress WHERE article_id = %s AND user_id = %s AND assignment_id = %s", (article_id, user_id, assignment_id))
        result = await cur.fetchall()
        if len(result) == 1:
            pass
        else:
            await cur.execute("INSERT INTO user_quiz_progress (user_id, article_id, assignment_id, score) VALUES (%s, %s, %s, %s)", (user_id, article_id, assignment_id, -1))

        return {"success": True, "quiz": quiz}

async def user_finish_quiz(query: dict):
    # assignment_id, user_id, article_id, answers
    conn = await aiomysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db=os.getenv("DB_DATABASE")) # type: ignore
    async with conn.cursor() as cur:
        assignment_id = query['assignment_id']
        user_id = query['user_id']
        article_id = query['article_id']
        answers = json.load(query['answers'])

        await cur.execute("SELECT * FROM article_quiz WHERE article_id = %s", (article_id,))
        result = await cur.fetchall()
        if len(result) != 1:
            return {"success": False}

        quiz = json.load(result[0][1])
        if len(answers) != len(quiz):
            return {"success": False}

        correct = 0
        for question in quiz:
            # question1: {question: "", answer: ""}, question2: ...
            if answers[question]['answer'] == quiz[question]['answer']: correct += 1
        
        await cur.execute("UPDATE user_quiz_progress SET score = %s WHERE article_id = %s AND user_id = %s AND assignment_id = %s", (correct, article_id, user_id, assignment_id))
        
        return {"success": True, "score": correct}
    