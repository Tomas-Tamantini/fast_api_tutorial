from http import HTTPStatus
from fastapi import APIRouter


todo_router = APIRouter(prefix="/todos", tags=["todos"])
