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

    result = service.add_user(user)
    if result:
        return {"message": f"Add {user.name} Successfully"}
    else:
        raise HTTPException(status_code=409, detail=f"{user.name} Already Exist")


@router.delete("/users/{username}")
def delete_user(username: str):
    deleted = service.delete_user(username)
    if deleted:
        return {"message": f"Delete {username} Successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"{username} does not exist")

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

@router.put("/users")
def update_user_age(user: User):
    user.name = user.name.strip()
    result = service.update_user_age(user)

    if result:
        return {"message": f"{user.name} Age Update Successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"{user.name} does not Exist")