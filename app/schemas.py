from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    created_at: datetime=datetime.now()
    
    class Config:
        from_attributes=True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes=True
        
class UpdatedPost(BaseModel):
    title: str
    content: str
    published: bool=True
    class Config:
        from_attributes=True

class ResultPost(BaseModel):
    id: int
    content: str
    title: str
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        from_attributes= True
        
class ResultUpdate(BaseModel):
    title: str
    content: str
    class Config:
        from_attributes=True
    
class RegisterUser(BaseModel):
    email: EmailStr
    password: str

        
class Login(BaseModel):
    email: EmailStr
    password: str
    
class ResultLogin(BaseModel):
    email: EmailStr
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Votes(BaseModel):
    user_id: int
    post_id: int
    user: UserOut
    post: ResultPost
    
    class Config:
        from_attributes= True
    
class VoteInput(BaseModel):
    post_id: int
    dir: conint(le=1)