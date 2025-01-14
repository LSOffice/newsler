import os
from ast import Delete

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..db.controllers import auth
from ..db.controllers.edu import *

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()


class Load(BaseModel):
    user_id: str | None = None


class LoadQuiz(BaseModel):
    user_id: str | None = None
    article_id: str | None = None
    assignment_id: str | None = None


class FinishQuiz(BaseModel):
    user_id: str | None = None
    article_id: str | None = None
    assignment_id: str | None = None
    answers: str | None = None


class LoadAssignment(BaseModel):
    assignment_id: str | None = None
    user_id: str | None = None


class JoinClassroom(BaseModel):
    user_id: str | None = None
    join_code: str | None = None


class CreateClassroom(BaseModel):
    user_id: str | None = None
    classroom_name: str | None = None
    subject_code: str | None = None
    educational_level: str | None = None


class CreateAssignment(BaseModel):
    user_id: str | None = None
    classroom_id: str | None = None
    title: str | None = None
    description: str | None = None
    assignment_type: str | None = None
    graded: bool | None = None
    articles: list | None = None


class LeaveClassroom(BaseModel):
    user_id: str | None = None
    classroom_id: str | None = None


class DeleteAssignment(BaseModel):
    user_id: str | None = None
    assignment_id: str | None = None


class FinishQuiz(BaseModel):
    user_id: str | None = None
    article_id: str | None = None
    assignment_id: str | None = None
    answers: str | None = None


router = APIRouter(prefix="/edu", tags=["education"])


async def is_logged_in(req: Request) -> list:
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

    return [True, auth_obj[2]]


@router.post("/load")
async def load_edu(body: Load, auth_headers: list = Depends(is_logged_in)) -> dict:
    user_id = body.user_id
    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    edu_type, classrooms = await user_edu_load({"user_id": user_id})

    return {"edu_type": edu_type, "classrooms": classrooms}


@router.post("/classroom/join")
async def join_classroom(
    body: JoinClassroom, auth_headers: list = Depends(is_logged_in)
) -> dict:
    user_id = body.user_id
    join_code = body.join_code

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    success = await user_join_classroom({"user_id": user_id, "join_code": join_code})
    return {"success": success}


@router.post("/classroom/leave")
async def leave_classroom(
    body: LeaveClassroom, auth_headers: list = Depends(is_logged_in)
) -> dict:
    user_id = body.user_id
    classroom_id = body.classroom_id

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_leave_classroom(
        {"user_id": user_id, "classroom_id": classroom_id}
    )
    if not result:
        raise HTTPException(status_code=400, detail="Bad request")
    return {"success": result}


@router.post("/classroom/create")
async def create_classroom(
    body: CreateClassroom, auth_headers: list = Depends(is_logged_in)
) -> bool:
    user_id = body.user_id
    classroom_name = body.classroom_name
    educational_level = body.educational_level
    subject_code = body.subject_code

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_create_classroom(
        {
            "classroom_name": classroom_name,
            "educational_level": educational_level,
            "subject_code": subject_code,
        }
    )
    if not result[0]:
        raise HTTPException(status_code=400, detail="Bad request")
    success = await user_join_classroom(
        {"user_id": user_id, "classroom_id": result[1], "type": "teacher"}
    )
    if not success:
        raise HTTPException(status_code=400, detail="Bad request")

    return True


@router.post("/classroom/load")
async def load_classroom(
    body: LeaveClassroom, auth_headers: list = Depends(is_logged_in)
) -> dict:
    user_id = body.user_id
    classroom_id = body.classroom_id

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_load_classroom(
        {"user_id": user_id, "classroom_id": classroom_id}
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail="Failed")
    del result["success"]
    return result


@router.post("/assignment/load")
async def load_assignment(
    body: LoadAssignment, auth_headers: list = Depends(is_logged_in)
) -> dict:
    user_id = body.user_id
    assignment_id = body.assignment_id

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_load_assignment(
        {"user_id": user_id, "assignment_id": assignment_id}
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail="Bad request")

    del result["success"]
    return result


@router.post("/quiz/load")
async def load_quiz(body: LoadQuiz, auth_headers: list = Depends(is_logged_in)) -> dict:
    user_id = body.user_id
    assignment_id = body.assignment_id
    article_id = body.article_id
    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")
    result = await user_load_quiz(
        {"assignment_id": assignment_id, "user_id": user_id, "article_id": article_id}
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail="Bad request")

    del result["success"]
    return result


@router.post("/quiz/finish")
async def finish_quiz(
    body: FinishQuiz, auth_headers: list = Depends(is_logged_in)
) -> dict:
    user_id = body.user_id
    assignment_id = body.assignment_id
    article_id = body.article_id
    answers = body.answers

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_finish_quiz(
        {
            "user_id": user_id,
            "assignment_id": assignment_id,
            "article_id": article_id,
            "answers": answers,
        }
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail="Bad request")

    del result["success"]
    return result


@router.post("/assignment/5mrv")
async def fivemostrecentlyviewed(
    body: Load, auth_headers: list = Depends(is_logged_in)
) -> list:
    # user_id
    user_id = body.user_id

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_5_recently_viewed_articles({"user_id": user_id})

    if not result:
        raise HTTPException(status_code=400, detail="Bad request")

    return result


@router.post("/assignment/delete")
async def delete_assignment(
    body: DeleteAssignment, auth_headers: list = Depends(is_logged_in)
) -> dict:
    # user_id, assignment_id
    user_id = body.user_id
    assignment_id = body.assignment_id

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_delete_assignment({"assignment_id": assignment_id})

    if not result:
        raise HTTPException(status_code=400, detail="Bad request")

    return {"success": result}


@router.post("/assignment/create")
async def create_assignment(
    body: CreateAssignment, auth_headers: list = Depends(is_logged_in)
) -> dict:
    # classroom_id, author_id, title, description, assignment_type, graded, articles
    author_id = body.user_id
    assignment_type = body.assignment_type
    articles = body.articles
    classroom_id = body.classroom_id
    description = body.description
    graded = body.graded
    title = body.title

    if (not auth_headers[0]) and (author_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_create_assignment(
        {
            "author_id": author_id,
            "classroom_id": classroom_id,
            "title": title,
            "description": description,
            "assignment_type": assignment_type,
            "articles": articles,
            "graded": graded,
        }
    )

    if not result:
        raise HTTPException(status_code=400, detail="Bad request")

    return {"success": result}
