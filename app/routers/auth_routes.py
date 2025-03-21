from fastapi import APIRouter, HTTPException, Depends
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.schemas import UserCreate, LoginSchema
from app.crud import create_user_db, get_user_by_username_db


router = APIRouter()

# ✅ User Registration
@router.post("/register/")
def register_user(user: UserCreate):
    existing_user = get_user_by_username_db(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    created_user = create_user_db(user_data)
    return {"message": "User registered successfully", "user": created_user}

# ✅ User Login
@router.post("/login/")
def login_user(login_data: LoginSchema):
    user = get_user_by_username_db(login_data.username)
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Protected Route (Example)
@router.get("/me/")
def get_current_user_data(current_user: dict = Depends(get_current_user)):
    return current_user
