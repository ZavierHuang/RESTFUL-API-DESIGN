from fastapi import APIRouter
from src import services

router = APIRouter()

@router.get("/users")
def get_users():
    return services.list_users()

