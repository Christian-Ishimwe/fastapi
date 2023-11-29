from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app =FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
    rating: Optional[int]=None

@app.get("/")
def get_user():
    return {"name": "Ishimwe christian!"}

@app.get('/posts')
def get_posts():
    return {"data": "this is your post"}

@app.post('/createpost')
def create_post(post : Post):
    print(post)
    if post.published:
        return {'data': f"Title: {post.title} \nContent: {post.content} Rating: {post.rating}"}
    else:
        return {'data': "Data stored for future use"}

# title, str and content, str