
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, utls, schemas
from ..schemas import RegisterUser
from sqlalchemy.orm import Session
from ..database import engine, get_db

router= APIRouter(
    tags=['Users']
)

@router.post('/create/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : RegisterUser, db: Session=Depends(get_db)):
    hashed_password=utls.hashed_pass(user.password)
    user.password=hashed_password
    try:  
        new_User=models.User(**user.dict())
        db.add(new_User)
        db.commit()
        return new_User
    except Exception as err:
        print(err)
        return {'Error': err}
 
@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id :  str, db: Session=Depends(get_db)):
    user=db.query(models.User).filter_by(id=id).first()
    if user:
        return user
    else:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found')
    

    
    
    


