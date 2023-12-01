from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from random import randrange
import time

app =FastAPI()

myposts=[
        {
            "title": "test 1",
            "content": "content for test 1",
            "id": 1
        },
        {
            "title": "test 2",
            "content": "content for test 2",
            "id": 2
        },
        {
            "title": "test 3",
            "content": "content for test 3",
            "id": 3
        }
    ]
class Post(BaseModel):
    
    title: str
    content: str 
    published: bool = True
    rating: Optional[int]=None

class Update(BaseModel):
    title: str
    content: str
    published: bool  = True
    
    
while True:
    try:
        cunn=psycopg2.connect(host='localhost', password='christian', user='postgres',database='fastapi', cursor_factory=RealDictCursor)
        cursor=cunn.cursor()
        print('successful connected')
        break
    except Exception as error:
        
        print('failed to auntantivate')
        print('error is', error)
        time.sleep(2)
        


@app.get("/")
def get_user():
    return {"name": "Ishimwe christian!"}

@app.get('/posts')
def get_posts():
    cursor.execute("""
                       SELECT * FROM posts
                       ORDER BY id DESC
                       """)
    data=cursor.fetchall()
    print()
    return {"data": data}

@app.post('/posts', status_code=status.HTTP_201_CREATED) 
def create_post(post : Post):
    
    cursor.execute("""
                   INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
                   """,
                    (post.title, post.content, post.published)
                   )
    new_entry=cursor.fetchone()
    return {"New post": new_entry}


@app.get('/post/{id}')
def get_post(id: int, response: Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found!")
    else:
        return {'data': post}


@app.put('/update/{id}')
def update_post(id: int, change: Update):
    change_post=change.dict()
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The Post With that id does't Exist")
    post['title']=change_post['title']
    post['content']=change_post['content']  
    return {"post": change_post}

@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The requested post does't exist")
    myposts.remove(post)
    return {'deleted': post}

def find_post(id):
    for p in myposts:
        if p['id']==id:
            return p


# title, str and content, str
