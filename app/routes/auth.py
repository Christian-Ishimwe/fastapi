from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas,database, utls, oath2
from ..database import engine, get_db
router=APIRouter(
    tags=['AUTHENTICATION']
)
@router.post('/login',status_code=status.HTTP_200_OK)
def login(user: OAuth2PasswordRequestForm=Depends() ,db: Session =Depends(get_db)):
   
    Luser=db.query(models.User).filter_by(email=user.username).first()
    if Luser and utls.verify(user.password, Luser.password):
        access_token=oath2.create_token(data={"user_id": Luser.id, "email": Luser.email})
        return {"access_token": access_token, "token_type":"bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unthothorised access")
        


