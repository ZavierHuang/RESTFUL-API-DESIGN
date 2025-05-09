import csv
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

# Add User
def test_create_user_by_post_api():
    response = client.post("/users", json={"name": "Zavier", "age":23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add User Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age":23} in response.json()
    assert len(response.json()) == 1

def test_create_user_by_post_api_with_age_is_str_number():
    response = client.post("/users", json={"name": "Zavier", "age": "23"})
    assert response.status_code == 422
    assert "Input should be a valid integer" in response.json()["detail"][0]['msg']

def test_create_user_by_post_api_with_long_space_name():
    response = client.post("/users", json={"name": "    ", "age": 23})
    assert response.status_code == 422
    assert "Name cannot be Empty." in response.json()["detail"]

def test_create_user_by_post_api_with_name_is_empty():
    response = client.post("/users", json={"name": "", "age": 10})
    assert response.status_code == 422
    assert 'String should have at least 1 character' in response.json()["detail"][0]['msg']

def test_create_user_by_post_api_with_name_does_not_exist():
    response = client.post("/users", json={"age": 10})
    assert response.status_code == 422
    assert 'Field required' in response.json()["detail"][0]['msg']

def test_create_user_by_post_api_with_age_does_not_exist():
    response = client.post("/users", json={"name": 'Zavier'})
    assert response.status_code == 422
    assert 'Field required' in response.json()["detail"][0]['msg']

def test_create_user_by_post_api_with_empty_json():
    response = client.post("/users", json={})
    assert response.status_code == 422
    assert 'Field required' in response.json()["detail"][0]['msg']

def test_create_user_by_post_api_with_age_is_not_number():
    response = client.post("/users", json={"name": "Zavier", "age": "abc"})
    assert response.status_code == 422
    assert 'Input should be a valid integer' in response.json()["detail"][0]["msg"]

def test_create_user_by_post_api_with_age_is_not_larger_than_zero():
    response = client.post("/users", json={"name": "Zavier", "age": -1})
    assert response.status_code == 422
    assert 'Age must be greater than 0.' in response.json()["detail"]

def test_create_user_by_post_api_with_name_has_existed_to_update():
    response = client.post("/users", json={"name": "Zavier", "age": 23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add User Successfully"

    response = client.post("/users", json={"name": "Zavier", "age": 20})
    assert response.status_code == 200
    assert response.json()["message"] == "Add User Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 23} not in response.json()
    assert {"name": "Zavier", "age": 20} in response.json()
    assert len(response.json()) == 1

# Delete User
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

def test_delete_users_by_del_api_with_name_does_not_exist():
    response = client.delete("/users/John")
    assert response.status_code == 200
    assert response.json()["message"] == "John does not exist"

# Upload CSV + Add User
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

    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as readFile:
        response = client.post("/users/upload", files={"file": ("empty.csv", readFile, 'text/csv')})
        assert response.status_code == 404
        assert "No columns to parse" in response.json()["detail"]

def test_upload_users_by_post_api_with_Age_field_does_not_exist():
    file_path = os.path.join(ROOT, 'test/onlyNameField.csv')
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name'])
        writer.writerow(['Alice'])
        writer.writerow(['Bob'])
        writer.writerow(['Charlie'])

    assert os.path.exists(file_path) is True

    with open(file_path,'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("onlyNameField.csv", csvfile, 'text/csv')})
        assert response.status_code == 404
        assert 'Age' in response.json()["detail"]

def test_upload_users_by_post_api_with_age_is_not_number():
    file_path = os.path.join(ROOT, 'test/ageNotValid.csv')
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Age'])
        writer.writerow(['Alice', 'ab'])
        writer.writerow(['Bob', 11])
        writer.writerow(['Charlie', 12])

    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("ageNotValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_upload_users_by_post_api_remove_row_of_name_is_empty():
    file_path = os.path.join(ROOT, 'test/existNameIsEmpty.csv')
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Age'])
        writer.writerow(['Alice', 13])
        writer.writerow(['', 11])
        writer.writerow(['Charlie', 12])
        writer.writerow(['    ', 25])

    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("ageNotValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

# Calculate Average of each group
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

def test_average_age_of_each_group_by_get_api_with_no_data():
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == {}

def test_average_age_of_each_group_by_get_api_with_Age_field_does_not_exist():
    file_path = os.path.join(ROOT, 'test/onlyNameField.csv')
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name'])
        writer.writerow(['Alice'])
        writer.writerow(['Bob'])
        writer.writerow(['Charlie'])

    assert os.path.exists(file_path) is True

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_average_age_of_each_group_by_get_api_with_age_is_not_number():
    file_path = os.path.join(ROOT, 'test/ageNotValid.csv')
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Age'])
        writer.writerow(['Alice', 20])
        writer.writerow(['Bob', 11])
        writer.writerow(['Aharlie', 'ab'])

    assert os.path.exists(file_path) is True

    with open(os.path.join(file_path),'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("ageNotValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert len(response.json()) == 2

    
