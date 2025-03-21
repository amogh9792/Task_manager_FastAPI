from fastapi import APIRouter, Depends
from app.auth import get_current_user
from ..schemas import TaskCreate
from ..crud import (
    create_task_db, 
    get_all_tasks_db, 
    get_task_by_id_db, 
    update_task_db, 
    delete_task_db
)

router = APIRouter()

# ✅ Create Task (Protected)
@router.post("/tasks/")
def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    return create_task_db(task.dict())

# ✅ Get All Tasks (Protected)
@router.get("/tasks/")
def get_tasks(current_user: dict = Depends(get_current_user)):
    return get_all_tasks_db()

# ✅ Get Task by ID (Protected)
@router.get("/tasks/{task_id}")
def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    return get_task_by_id_db(task_id)

# ✅ Update Task (Protected)
@router.put("/tasks/{task_id}")
def update_task(task_id: str, task: TaskCreate, current_user: dict = Depends(get_current_user)):
    return update_task_db(task_id, task.dict())

# ✅ Delete Task (Protected)
@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    return delete_task_db(task_id)
