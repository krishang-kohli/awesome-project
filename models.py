
from sqlalchemy import String, Boolean, Integer,TIMESTAMP,func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean,server_default='True',nullable=False)
    created_at: Mapped[datetime] = mapped_column( TIMESTAMP(timezone=True),nullable=False, server_default=func.now())


class user(Base):
    __tablename__="Users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email:Mapped[str]=mapped_column(String,nullable=False,unique=True)
    password:Mapped[str]=mapped_column(String,nullable=False)
    created_at: Mapped[datetime] = mapped_column( TIMESTAMP(timezone=True),nullable=False, server_default=func.now())
    
    
