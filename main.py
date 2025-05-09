from fastapi import FastAPI

from src import routes

app = FastAPI(title="FastAPI")

app.include_router(routes.router)