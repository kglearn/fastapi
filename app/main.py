from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                            password='passwordone', cursor_factory=RealDictCursor)
    print("DB connected successfully")
except Exception as err:
    print(f"DB connection failed with - {err}")

myPosts = [{"title": "Post 1", "content": "post 1 content", "id": 1},
            {"title": "Post 2", "content": "po st 2 content", "id": 2}]


def getPostFromArr(id):
    for idx, post in enumerate(myPosts):
        if post['id'] == id:
            return idx, post       
    return None, None       

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/posts")
def getPosts():
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    cursor.close()
    return {"posts": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    newPost = cursor.fetchone()
    conn.commit()
    cursor.close()
    return {"data" : newPost}

@app.get("/posts/latest")
def getPostLatest():
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM posts where id = (SELECT max(id) FROM posts) """)
    post = cursor.fetchone()
    cursor.close()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": post}

@app.get("/posts/{id}")
def getPostById(id: int):
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
    post = cursor.fetchone()
    cursor.close()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM posts where id = %s RETURNING * """, (str(id)))
    deletedPost = cursor.fetchone()
    conn.commit()

    if not deletedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post {id} not found")
    
    cursor.close()
    # return {"data" : deletedPost}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    idx, _ = getPostFromArr(id)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post {id} not found")

    postDict = post.dict()
    postDict['id'] = id
    myPosts[idx] = postDict

    return {"data": postDict}