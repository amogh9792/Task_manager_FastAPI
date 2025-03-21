from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Task Management API with MongoDB",
    version="1.0.0"
)

app.include_router(router)
