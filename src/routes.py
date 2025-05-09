from fastapi import APIRouter, UploadFile, File, HTTPException

from src.models import User
from src.services import Services

router = APIRouter()
service = Services()

@router.post("/init")
def clear_users():
    return service.clear_users()
@router.get("/users")
def get_users():
    return service.list_users()

@router.post("/users")
def add_user(user: User):
    if len(user.name) == 0:
        raise HTTPException(status_code=422, detail="Name cannot be empty.")
    if user.age <= 0:
        raise HTTPException(status_code=422, detail="Age must be greater than 0.")

    service.add_user(user)
    return {"message": "Add User Successfully"}


@router.delete("/users/{username}")
def delete_user(username: str):
    deleted = service.delete_user(username)
    if deleted:
        return {"message": f"Delete {username} Successfully"}
    else:
        return {"message": f"{username} does not exist"}

@router.post("/users/upload")
def upload_csv_users(file: UploadFile = File(...)):
    try:
        service.add_user_from_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Users Added From CSV"}

@router.get("/users/averageAge")
def calculate_users_average_age_of_each_group():
    return service.calculate_users_average_age_of_each_group()