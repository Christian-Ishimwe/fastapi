from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oath2

router= APIRouter(
    tags=['POSTS']
)

@router.get("/")
def get_user():
    return {"name": "Ishimwe christian!"}


@router.get('/sqlalech', response_model=List[schemas.ResultPost])
def test_set(db: Session= Depends(get_db), current_user=Depends(oath2.get_current_user),
             limit: int=10, skip: int =1, search: Optional[str]=""):
    
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all() #.filter_by(owner_id=current_user.id)
    if posts:
        return posts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No content ")

@router.get('/post/{id}', response_model=schemas.ResultPost, status_code=status.HTTP_200_OK)
def get_sql_post(id, db: Session=Depends(get_db), current_user= Depends(oath2.get_current_user)):

    post= db.query(models.Post).filter_by(id=id).first()
    if post:
        if post.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorsed to perform this action")
        else:
            return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    

@router.post('/post',  status_code=status.HTTP_201_CREATED)
def post_sql(post : schemas.Post ,db: Session=Depends(get_db), current_user: int =Depends(oath2.get_current_user)):
    print(current_user.email)
    new_post=models.Post(owner_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResultUpdate)
def update_post(id: str, updates: schemas.UpdatedPost, db: Session=Depends(get_db),user_id: int =Depends(oath2.get_current_user)):
    try:
        post=db.query(models.Post).filter_by(id=id).first()
        post.title=updates.title
        post.content=updates.content    
        post.published=updates.published
        db.commit()
        return {"Updated data": updates}
    except Exception as e:
        print(e)
        return {'error': e}
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (change.title, change.content, change.published, id))
    # post= cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The Post With that id does't Exist")
    # conn.commit()
    # return {"post": post}
        

@router.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str ,db: Session=Depends(get_db), current_user: int =Depends(oath2.get_current_user)):
    post= db.query(models.Post).filter_by(id=int(id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no post with such id')
    else:
        if post.owner_id!=current_user.id:
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unothorised access")
        else:
            return post

