from fastapi import APIRouter, UploadFile, File, HTTPException

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

@router.delete("/users/{username}")
def delete_user(username: str):
    service.delete_user(username)
    return {"message": f"Delete {username} Successfully"}

@router.post("/users/upload")
def upload_csv_users(file: UploadFile = File(...)):
    try:
        service.add_user_from_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Users Added From CSV"}