from fastapi import APIRouter
from fastapi.responses import HTMLResponse


exercises_router = APIRouter(prefix="/exercises", tags=["exercises"])


@exercises_router.get("/")
def read_root():
    return {"message": "Hello World"}


@exercises_router.get("/html", response_class=HTMLResponse)
def get_html():
    return """
    <html>
        <head>
            <title>hello world</title>
        </head>
        <body>
            <h1>Hello world!</h1>
            <p>In HTML format :)</p>
        </body>
    </html>
    """
