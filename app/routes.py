from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, crud, auth, dependencies
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import os
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_user(db, user)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/tasks/")
def create_task(task: schemas.TaskCreate, db: Session = Depends(dependencies.get_db), user=Depends(dependencies.get_current_user)):
    return crud.create_task(db, task, user.id)

@router.get("/tasks/", response_model=list[schemas.TaskOut])
def read_tasks(db: Session = Depends(dependencies.get_db), user=Depends(dependencies.get_current_user)):
    return crud.get_tasks(db, user.id)

@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(dependencies.get_db), user=Depends(dependencies.get_current_user)):
    return crud.update_task(db, task_id, task)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(dependencies.get_db), user=Depends(dependencies.get_current_user)):
    return crud.delete_task(db, task_id)
