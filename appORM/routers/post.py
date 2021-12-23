from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from appORM import models, schemas, oauth2
from appORM.database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def getPosts(db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found")

    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def getPostById(id: int, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    newPost = models.Post(ownerId=currentUser.id, **post.dict())

    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost

@router.put("/{id}", response_model=schemas.PostResponse)
def updatePost(id: int, postUpdate: schemas.PostCreate, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    postQuery = db.query(models.Post).filter(models.Post.id == id, models.Post.ownerId == currentUser.id)
    post = postQuery.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorised to update this post")

    postQuery.update(postUpdate.dict(), synchronize_session=False)

    db.commit()
    
    return postQuery.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    postQuery = db.query(models.Post).filter(models.Post.id == id, models.Post.ownerId == currentUser.id)
    post = postQuery.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorised to delete this post")        

    postQuery.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)