from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

MONGO_URI = os.getenv("MONGO_URI")

# ✅ MongoDB Client
client = MongoClient(MONGO_URI)
db = client["task_manager_db"]

# ✅ Collections
task_collection = db["tasks"]
user_collection = db["users"]

# ✅ Ensure username is unique
user_collection.create_index("username", unique=True)
