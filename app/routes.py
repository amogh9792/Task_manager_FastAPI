from fastapi import APIRouter, HTTPException
from bson import ObjectId
from .database import task_collection
from .models import task_helper
from .schemas import TaskCreate, Task
from typing import List

router = APIRouter()

@router.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    task_dict = task.dict()
    result = task_collection.insert_one(task_dict)
    created_task = task_collection.find_one({"_id": result.inserted_id})
    return task_helper(created_task)

@router.get("/tasks/", response_model=List[Task])
def get_tasks():
    tasks = []
    for task in task_collection.find():
        tasks.append(task_helper(task))
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    task = task_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        return task_helper(task)
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_task: TaskCreate):
    result = task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": updated_task.dict()}
    )
    if result.modified_count == 1:
        task = task_collection.find_one({"_id": ObjectId(task_id)})
        return task_helper(task)
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    result = task_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 1:
        return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
