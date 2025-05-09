import os

import pandas as pd
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

ROOT = 'F:\GITHUB\FAST_API_Web_RESTFUL'

def test_get_user_list_by_get_api():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user_by_post_api():
    response = client.post("/users", json={"name": "Zavier", "age":23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add User Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age":23} in response.json()


def test_delete_users_by_del_api():
    response = client.post("/users", json={"name": "John", "age":25})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "John", "age":25} in response.json()

    response = client.delete("/users/John")
    assert response.status_code == 200
    assert response.json()["message"] == "Delete John Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "John", "age": 25} not in response.json()

def test_upload_users_by_post_api():
    with open(os.path.join(ROOT, "data/backend_users.csv"),'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("backend_users.csv", csvfile, 'text/csv')})
        csvfile.seek(0)  # go back to the start of csv file
        totalData = pd.read_csv(csvfile).shape[0]

    assert response.status_code == 200
    assert "Users Added From CSV" in response.json()["message"]

    response = client.get("/users")
    assert response.status_code == 200
    assert totalData == len(response.json())

def test_average_age_by_get_api():
    pass
