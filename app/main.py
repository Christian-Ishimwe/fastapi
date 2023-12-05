from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body


from pydantic import BaseModel
from random import randrange

from app.routes import vote


from .database import engine
from .  import models
from .config import settings
from .routes import posts, user, auth

models.Base.metadata.create_all(bind=engine)


app =FastAPI()




    

        
app.include_router(posts.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)



# @app.get('/posts')
# def get_posts():
#     cursor.execute("""
#                        SELECT * FROM posts
#                        ORDER BY id DESC
#                        """)
#     data=cursor.fetchall()
#     print()
#     return {"data": data}

# @app.post('/posts', status_code=status.HTTP_201_CREATED) 
# def create_post(post : Post):
#     cursor.execute("""
#                    INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
#                    """,
#                     (post.title, post.content, post.published)
#                    )
#     new_entry=cursor.fetchone()
#     conn.commit()
#     return {"New post": new_entry}


# @app.get('/post/{id}')
# def get_post(id: str):
#     cursor.execute(""" SELECT * FROM posts WHERE id= %s""", (id))
#     post=cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found!")
#     else:
#         return {'data': post}


# @app.put('/update/{id}')
# def update_post(id: str, change: Update):
#     cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (change.title, change.content, change.published, id))
#     post= cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The Post With that id does't Exist")
#     conn.commit()
#     return {"post": post}

# @app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(f""" DELETE FROM posts WHERE id = {id} RETURNING *""", )
#     post= cursor.fetchone()
#     if not post :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The requested post does't exist")
#     else:
#         conn.commit()
#         return {'deleted': post}

# def find_post(id):
#     for p in myposts:
#         if p['id']==id:
#             return p


# # title, str and content, str
