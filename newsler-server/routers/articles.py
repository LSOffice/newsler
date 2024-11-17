from fastapi import APIRouter, Depends, Request
import bcrypt

salt = open("config.txt", "r").readlines()[0].replace("salt=", "").encode()


router = APIRouter(
    prefix="/articles",
    responses={404: {"description": "Not found"}},
)
