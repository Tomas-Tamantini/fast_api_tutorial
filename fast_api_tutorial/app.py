from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fast_api_tutorial.api.routers import user_router, auth_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/html", response_class=HTMLResponse)
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
