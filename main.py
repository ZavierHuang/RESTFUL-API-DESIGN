from fastapi import FastAPI

from src import routes

app = FastAPI(title="FastAPI")

app.include_router(routes.router)

# uvicorn main:app --port 8080
# 127.0.0.1:8080/docs