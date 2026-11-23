from pydantic import BaseModel,EmailStr
from datetime import datetime
class Post(BaseModel):
    title:str
    content:str
    published:bool=True


class Postcreate(Post):
    pass

class Postresponse(Post):
    id:int
    

    class Config:
        orm_mode=True

class Userscreate(BaseModel):
    email:EmailStr
    password:str

class Usersresponse(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime