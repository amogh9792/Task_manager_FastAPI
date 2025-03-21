from pydantic import BaseModel, EmailStr
from typing import Optional

# ✅ Task Schemas
class TaskBase(BaseModel):
    title: str
    description: str
    completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str

# ✅ User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str

# ✅ Login Schema
class LoginSchema(BaseModel):
    username: str
    password: str
