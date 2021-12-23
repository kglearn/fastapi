from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from appORM import models, schemas, oauth2
from appORM.database import get_db

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    postQuery = db.query(models.Post).filter(models.Post.id == vote.postId)
    post = postQuery.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.postId} not found")

    existingVoteQuery = db.query(models.Vote).filter(models.Vote.postId == vote.postId, models.Vote.userId == currentUser.id)
    existingVote = existingVoteQuery.first()

    if vote.direction == 1:
        if existingVote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {currentUser.id} has already voted on post {vote.postId}")
        newVote = models.Vote(userId=currentUser.id, postId=vote.postId)

        db.add(newVote)
        postQuery.update({'votes': post.votes + 1}, synchronize_session=False)
        db.commit()
        return {"message": "voted successfully"}
    else:
        if not existingVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {currentUser.id} has not yet voted on post {vote.postId}")
        existingVoteQuery.delete(synchronize_session=False)
        postQuery.update({'votes': post.votes - 1}, synchronize_session=False)
        db.commit()
        return {"message": "unvoted successfully"}