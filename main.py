from fastapi import FastAPI, Request ,HTTPException,status
#from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException




app= FastAPI()

templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

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

# @app.get("/post",response_class=HTMLResponse,include_in_schema=False) 
# def get_first_post():
#     return f"<h1>{posts[0]['author']}</h1>"

@app.get("/",include_in_schema=False,name="home")
@app.get("/posts",include_in_schema=False,name="posts")
def home(request:Request):
    return templates.TemplateResponse(request,"home.html",{
        "posts":posts,
        "count":len(posts)
        })

@app.get("/api/get/posts/{post_id}",include_in_schema=False)
@app.get("/get/posts/{post_id}",include_in_schema=False)
def get_all_posts(request:Request,post_id:int):
    for post in posts:
        if post.get("id")==post_id:
            title=post["title"[:50]]
            return templates.TemplateResponse(request,"post.html",{"post":post,"title":title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
# @app.get("/api/posts", response_class=PlainTextResponse)
# def get_posts():
#     return str(posts)

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request:Request,exception:StarletteHTTPException):
    message=(
        exception.detail
        if exception.detail
        else "An error occured.Please check your request and try again."
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail":message},
        )
    return templates.TemplateResponse(request,"error.html",
                                      {
                                          "status_code":exception.status_code,
                                          "title":exception.status_code,
                                          "message":message,
                                      },
                                      status_code=exception.status_code,
                                      )