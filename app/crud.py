from sqlalchemy.orm import Session
from . import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and auth.verify_password(password, user.hashed_password):
        return user
    return None

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def update_task(db: Session, task_id: int, task_data: schemas.TaskCreate):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    for key, value in task_data.dict().items():
        setattr(task, key, value)
    db.commit()
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(task)
    db.commit()
