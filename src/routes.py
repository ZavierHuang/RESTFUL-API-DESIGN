from fastapi import APIRouter
from src.services import Services

router = APIRouter()
service = Services()

@router.get("/users")
def get_users():
    return service.list_users()

