from fastapi import FastAPI , Response , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import models
from database import engine , get_db
from sqlalchemy.orm import Session
import schemas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

conn = psycopg.connect(
    host="localhost",
    dbname="fastapi",
    user="postgres",
    password="new_password"
)




print("posts table created")

    




my_posts=[{'title':"title of post 1","content":"content of post 1","id":1},{'title':"beaches", "content":"top 10 beaches","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
          return p 


def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p['id'] == id:
          return i

@app.get("/")
def root():
    return {"message":"welcome to my api"}


@app.get("/posts",response_model=list[schemas.Post])
def get_post(db: Session= Depends(get_db)):
    #cursor = conn.cursor()
    #cursor.execute(""" SELECT * FROM posts""")
     posts=db.query (models.Posts).all()
     return  posts

@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Postresponse)
def createpost(post: schemas.Postcreate,db: Session= Depends(get_db) ):
    #   cursor = conn.cursor()
    # cursor.execute(""" INSERT INTO POSTS (title,content,published) VALUES (%s ,%s ,%s) RETURNING *""",(post.title,post.content,post.published))  
    #   new_post = cursor.fetchall()  
    #   conn.commit()

      new_post=  models.Posts(**post.dict())
      db.add(new_post)
      db.commit()
      db.refresh(new_post)
      return  new_post

@app.get("/posts/{id}",response_model=schemas.Postresponse)
def get_post (id: int,db: Session= Depends(get_db)):
    # cursor=conn.cursor()
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(id,))
    # one_post=cursor.fetchone()
    
    one_post= db.query(models.Posts).filter(models.Posts.id == id).first()
    
    


    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return (one_post)
   
@app.delete("/posts/{id}",status_code=status.HTTP_200_OK)
def delete_post(id : int,db: Session= Depends(get_db)):
    # cursor=conn.cursor()
    # cursor.execute("""DELETE FROM posts WHERE id =%s returning *""",(id,))
    # print("hello")
    # print(cursor.execute("""DELETE FROM posts WHERE id =%s returning *""",(id,)))
    # deleted_post= cursor.fetchone()
   
    # conn.commit()
    
    deleted_post= db.query(models.Posts).filter(models.Posts.id == id)

    if deleted_post.first()== None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not found")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    



@app.put("/posts/{id}",response_model=schemas.Postresponse)
def update_post(id:int , post:schemas.Postcreate,db: Session= Depends(get_db) ):

    # cursor=conn.cursor()
    # cursor.execute("""UPDATE posts SET title = %s,content=%s,published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query= deleted_post= db.query(models.Posts).filter(models.Posts.id == id)

    updated_post=post_query.first()

    if updated_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not found")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
     
    return post_query.first()



@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.Usersresponse)
def create_post(user:schemas.Userscreate,db: Session= Depends(get_db)):
    new_user=  models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user