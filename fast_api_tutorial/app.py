from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


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
