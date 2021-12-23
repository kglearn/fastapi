from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint
from sqlalchemy_utils import EmailType

from appORM.database import Base
#----------------------------------------------------------------------------------------------------
#----------------------- USERS ----------------------------
#----------------------------------------------------------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str 

class UserReponse(UserBase):
    id: int
    createdAt: datetime

    class Config:
        orm_mode = True

#----------------------------------------------------------------------------------------------------
#----------------------- POST ----------------------------
#----------------------------------------------------------------------------------------------------
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    createdAt: datetime
    ownerId: int
    owner: UserReponse
    votes: int
    
    class Config:
        orm_mode = True

#----------------------------------------------------------------------------------------------------
#----------------------- TOKEN ----------------------------
#----------------------------------------------------------------------------------------------------

class Token(BaseModel):
    token: str
    tokenType: str

class TokenData(BaseModel):
    id: Optional[str] = None

#----------------------------------------------------------------------------------------------------
#----------------------- VOTE ----------------------------
#----------------------------------------------------------------------------------------------------
class Vote(BaseModel):
    postId: int 
    direction: bool
