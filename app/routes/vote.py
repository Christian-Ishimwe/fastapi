from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from app import oath2
from .. import schemas, database, models
from sqlalchemy.orm import Session


router= APIRouter(
    tags=['votes']
)

@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.VoteInput, db: Session=Depends(database.get_db),
         current_user=Depends(oath2.get_current_user)):
    post_id=vote.post_id
    post= db.query(models.Post).filter( models.Post.id==post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such post with that {post_id}")
    post_query=db.query(models.Votes).filter( models.Votes.post_id==post_id, models.Votes.user_id==current_user.id).first()
    if(vote.dir == 1):
        if post_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {current_user.id} have already votted for {vote.post_id}')
        new_vote=models.Votes(
            post_id=vote.post_id, 
            user_id=current_user.id
        )
        db.add(new_vote)
        db.commit()
        return {'reponse': "succeful added a vote"}
    else:
        if not post_query:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete such a post")
        
        else:
            db.delete(post_query)
            db.commit()
            
