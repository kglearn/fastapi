from jose import jwt, JWTError
from datetime import datetime, timedelta
from appORM import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, oauth2
from sqlalchemy.orm import Session
from appORM.config import settings

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_toke_expire_minutes

def createAccessToken(data: dict):
    dataCopy = data.copy()  
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dataCopy.update({"exp": expire})

    encodedJWT = jwt.encode(dataCopy, SECRET_KEY, algorithm=ALGORITHM)

    return encodedJWT

def verifyAccessToken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("userId")

        if id is None:
            raise credentials_exception

        tokenData = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return tokenData

def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verifyAccessToken(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user