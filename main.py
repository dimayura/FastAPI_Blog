from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app= FastAPI()

posts:list[dict]=[
    {
        "id":1,
        "author":"mayura",
        "title":"FastAPI is really good",
        "content":"FastAPI provides inbuilt documentation,data validation",
        "date_posted":"March 25,2026"
    },
    {
            "id":2,
        "author":"pankaj tanwar",
        "title":"Rasperberry PI is really good",
        "content":"i use it to create cool stuffs!",
        "date_posted":"March 20,2026"
    }
]

@app.get("/post",response_class=HTMLResponse,include_in_schema=False)
def get_first_post():
    return f"<h1>{posts[0]['author']}</h1>"

@app.get("/")
def home():
    return {"message": "Hello world!"}

@app.get("/api/posts")
def get_posts():
    return posts