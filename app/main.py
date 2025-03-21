from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth_routes, task_routes

app = FastAPI(
    title="Task Manager API with FastAPI + MongoDB + JWT",
    version="1.0.0"
)

# ✅ CORS (Optional - for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(auth_routes.router, tags=["Auth"])
app.include_router(task_routes.router, tags=["Tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager API!"}
