from bson import ObjectId

# Helper to convert MongoDB task document to JSON serializable dict
def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "completed": task.get("completed", False)
    }

# Helper for user data
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }
