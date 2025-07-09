from pydantic import BaseModel, EmailStr
from app import models
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    otp: int

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class JournalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: int

class EntryCreate(BaseModel):
    book_id: int
    mood: Optional[str] = None
    description: str

class EmailSchema(BaseModel):
    email: str