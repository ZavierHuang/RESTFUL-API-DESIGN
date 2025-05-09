import io
import os
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

ROOT = r'F:\GITHUB\FAST_API_Web_RESTFUL'

@pytest.fixture(autouse=True)
def setUp():
    print("SETUP")
    response = client.post("/init")
    assert response.status_code == 200


def test_get_user_list_by_get_api():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_create_user_by_post_api():
    response = client.post("/users", json={"name": "Zavier", "age":23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add User Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age":23} in response.json()
    assert len(response.json()) == 1



def test_delete_users_by_del_api():
    response = client.post("/users", json={"name": "John", "age":25})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "John", "age":25} in response.json()
    assert len(response.json()) == 1

    response = client.delete("/users/John")
    assert response.status_code == 200
    assert response.json()["message"] == "Delete John Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "John", "age": 25} not in response.json()
    assert len(response.json()) == 0


def test_upload_users_by_post_api():
    with open(os.path.join(ROOT, "data/backend_users.csv"),'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("backend_users.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

        csvfile.seek(0)  # go back to the start of csv file
        df = pd.read_csv(csvfile)
        totalData = df.shape[0]

    assert response.status_code == 200
    assert "Users Added From CSV" in response.json()["message"]

    response = client.get("/users")
    assert response.status_code == 200
    assert totalData == len(response.json())


def test_upload_users_by_post_api_with_empty_csv():
    file_path = os.path.join(ROOT, 'test/empty.csv')

    with open(file_path, 'w', encoding='utf-8') as writeFile:
        writeFile.write('')

    with open(file_path, 'rb') as readFile:
        response = client.post("/users/upload", files={"file": ("empty.csv", readFile, 'text/csv')})
        assert response.status_code == 404
        assert "No columns to parse" in response.json()["detail"]


def test_average_age_of_each_group_by_get_api():
    with open(os.path.join(ROOT, "data/backend_users.csv"),'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("backend_users.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

        csvfile.seek(0)  # go back to the start of csv file
        df = pd.read_csv(csvfile)
        df['firstCharacter'] = df['Name'].str[0]
        totalGroups = df.groupby('firstCharacter').ngroups

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert len(response.json()) == totalGroups



