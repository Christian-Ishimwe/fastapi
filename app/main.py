from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

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

@app.get("/")
def get_user():
    return {"name": "Ishimwe christian!"}

@app.get('/posts')
def get_posts():
    return {"data": myposts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    post_dict=post.dict()
    post_dict['id']=randrange(1,100000)
    myposts.append(post_dict)
    return {'data': myposts}

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
