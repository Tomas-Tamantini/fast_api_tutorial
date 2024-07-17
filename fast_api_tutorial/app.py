from fastapi import FastAPI
from fast_api_tutorial.api.routers import (
    user_router,
    auth_router,
    exercises_router,
    todo_router,
)

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(exercises_router)
app.include_router(todo_router)
