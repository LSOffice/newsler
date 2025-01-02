import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
import google.generativeai as genai
from pydantic import BaseModel
from ..db.init import auth_is_session_token_valid
from ..db.controllers.edu import *

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()

class Load(BaseModel):
    user_id: str | None = None

class LoadAssignment(BaseModel):
    assignment_id: str | None = None
    user_id: str | None = None

class JoinClassroom(BaseModel):
    user_id: str | None = None
    classroom_id: str | None = None
    type: str | None = None

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

router = APIRouter(prefix="/edu", tags=["education"])

async def is_logged_in(req: Request) -> list:
    try:
        session_token = req.headers["authorization"]
    except KeyError:
        return [False]
    session_token = session_token.replace("Bearer ", "")
    auth_obj = auth_is_session_token_valid({"session_token": session_token})

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
async def join_classroom(body: JoinClassroom, auth_headers: bool = Depends(is_logged_in)) -> dict:
    user_id = body.user_id
    classroom_id = body.classroom_id
    type = body.type
    
    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    success = await user_join_classroom({"user_id": user_id, "classroom_id": classroom_id, "type": type})
    return {"success": success}

@router.post("/classroom/leave")
async def leave_classroom(body: LeaveClassroom, auth_headers: bool = Depends(is_logged_in)) -> dict:
    user_id = body.user_id
    classroom_id = body.classroom_id

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_leave_classroom({"user_id": user_id, "classroom_id": classroom_id})
    if not result:
        raise HTTPException(status_code=400, detail="Bad request")
    return {"success": result}


@router.post("/classroom/create")
async def create_classroom(body: CreateClassroom, auth_headers: list = Depends(is_logged_in)) -> bool:
    user_id = body.user_id
    classroom_name = body.classroom_name
    educational_level = body.educational_level
    subject_code = body.subject_code

    if (not auth_headers[0]) and (user_id == auth_headers[1]):
        raise HTTPException(status_code=401, detail="Unauthorised")

    
    result = await user_create_classroom({"classroom_name": classroom_name, "educational_level": educational_level, "subject_code": subject_code})
    if not result:
        raise HTTPException(status_code=400, detail="Bad request")
    return result

@router.post("/classroom/load")
async def load_classroom(body: LeaveClassroom, auth_headers: bool = Depends(is_logged_in)) -> dict:
    user_id = body.user_id
    classroom_id = body.classroom_id

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_load_classroom({"user_id": user_id, "classroom_id": classroom_id})
    if not result['success']: raise HTTPException(status_code=400, detail="Failed")
    del result['success']
    return result

@router.post("/assignment/load")
async def load_assignment(body: LoadAssignment, auth_headers: bool = Depends(is_logged_in)) -> dict:
    user_id = body.user_id
    assignment_id = body.assignment_id

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")
    
    result = await user_load_assignment({"user_id": user_id, "assignment_id": assignment_id})
    if not result['success']:
        raise HTTPException(status_code=400, detail="Bad request")
    
    del result['success']
    return result

@router.post("/quiz/load")
async def load_quiz(body: Load, auth_headers: bool = Depends(is_logged_in)) -> dict:
    user_id = body.user_id

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    return {}

@router.post("/quiz/finish")
async def finish_quiz(body: Load, auth_headers: bool = Depends(is_logged_in)) -> dict:
    user_id = body.user_id

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    return {}

@router.post("/assignment/create")
async def create_assignment(body: CreateAssignment, auth_headers: bool = Depends(is_logged_in)) -> dict:
    # classroom_id, author_id, title, description, assignment_type, graded, articles
    author_id = body.user_id
    assignment_type = body.assignment_type
    articles = body.articles
    classroom_id = body.classroom_id
    description = body.description
    graded = body.graded
    title = body.title

    if not auth_headers:
        raise HTTPException(status_code=401, detail="Unauthorised")

    result = await user_create_assignment({
        "author_id": author_id,
        "classroom_id": classroom_id,
        "title": title,
        "description": description,
        "assignment_type": assignment_type,
        "articles": articles,
        "graded": graded
    })

    if not result:
        raise HTTPException(status_code=400, detail="Bad request")
    
    return {"success": result}