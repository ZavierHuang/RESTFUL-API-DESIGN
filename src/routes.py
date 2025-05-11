from fastapi import APIRouter, UploadFile, File, HTTPException

from src.models import User
from src.services import Services

router = APIRouter()
service = Services()

@router.post("/init")
def clear_users():
    service.clear_users()
    return {"message": "Clear User List Successfully"}
@router.get("/users")
def get_users():
    return service.list_users()

@router.post("/users")
def add_user(user: User):
    user.name = user.name.strip()
    if len(user.name) == 0:
        raise HTTPException(status_code=422, detail="Name cannot be Empty.")
    if user.age <= 0:
        raise HTTPException(status_code=422, detail="Age must be greater than 0.")

    service.add_user(user)
    return {"message": f"Add {user.name} Successfully"}


@router.delete("/users/{username}")
def delete_user(username: str):
    deleted = service.delete_user(username)
    if deleted:
        return {"message": f"Delete {username} Successfully"}
    else:
        return {"message": f"{username} does not exist"}

@router.post("/users/upload")
def upload_csv_users(file: UploadFile = File(...)):
    service.clear_users()
    if file.content_type not in ["text/csv"]:
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        result = service.add_user_from_csv(file.file)
        return {"message": f"Add Users From CSV Successfully {result}"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/users/averageAge")
def calculate_users_average_age_of_each_group():
    return service.calculate_users_average_age_of_each_group()