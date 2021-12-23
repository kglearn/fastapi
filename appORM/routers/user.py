from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from appORM import models, schemas, utils
from appORM.database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.get("/", response_model=List[schemas.UserReponse])
def getUsers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user found")

    return users

@router.get("/{id}", response_model=schemas.UserReponse)
def getUserById(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReponse)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hashPasswd(user.password)

    newUser = models.User(**user.dict())

    db.add(newUser)
    try:
        db.commit()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"Email {user.email} already exists") 

    
    db.refresh(newUser)

    return newUser

@router.put("/{id}", response_model=schemas.UserReponse)
def updateUser(id: int, userUpdate: schemas.UserCreate, db: Session = Depends(get_db)):
    userQuery = db.query(models.User).filter(models.User.id == id)

    print(id, userQuery.first())

    if not userQuery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User {id} not found")

    try:
        userQuery.update(userUpdate.dict(), synchronize_session=False)
        db.commit()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"Email - {userUpdate.email} - already exists") 
    
    return userQuery.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int, db: Session = Depends(get_db)):
    userQuery = db.query(models.User).filter(models.User.id == id)

    if not userQuery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User {id} not found")

    userQuery.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)