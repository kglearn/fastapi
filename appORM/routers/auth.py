from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from appORM import schemas, models, utils, oauth2
from appORM.database import get_db

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(userCreds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == userCreds.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials u")
    
    if not utils.verifyPasswd(userCreds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials p")

    token = oauth2.createAccessToken(data = {"userId": user.id})

    return {"token": token, "tokenType": "bearer"}