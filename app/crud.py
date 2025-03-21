from .database import task_collection, user_collection
from .models import task_helper, user_helper
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

# ✅ TASK OPERATIONS
def create_task_db(task_data: dict):
    result = task_collection.insert_one(task_data)
    task = task_collection.find_one({"_id": result.inserted_id})
    return task_helper(task)

def get_all_tasks_db():
    return [task_helper(task) for task in task_collection.find()]

def get_task_by_id_db(task_id: str):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid Task ID")
    task = task_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        return task_helper(task)
    raise HTTPException(status_code=404, detail="Task not found")

def update_task_db(task_id: str, updated_data: dict):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid Task ID")
    result = task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_data})
    if result.modified_count:
        return get_task_by_id_db(task_id)
    raise HTTPException(status_code=404, detail="Task not found")

def delete_task_db(task_id: str):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid Task ID")
    result = task_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count:
        return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

# ✅ USER OPERATIONS
def create_user_db(user_data: dict):
    try:
        result = user_collection.insert_one(user_data)
        user = user_collection.find_one({"_id": result.inserted_id})
        return user_helper(user)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")

def get_user_by_username_db(username: str):
    user = user_collection.find_one({"username": username})
    if user:
        return user
    return None
