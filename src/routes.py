from fastapi import APIRouter

from src.models import User
from src.services import Services

router = APIRouter()
service = Services()

@router.get("/users")
def get_users():
    return service.list_users()

@router.post("/users")
def add_user(user: User):
    service.add_user(user)
    return {"message": "Add User Successfully"}

