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

"""
Get User List
"""
def test_get_user_list_by_get_api():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0

"""
Add User
1.【200】Normal Case         (str: "User", int: 10)        =>  'Add User Successfully'

2.【200】Age is str number   (str: "User", int: "10")      =>  'Add User Successfully'
3.【422】Age is not number   (str: "User", str: "10")      =>  'Input should be a valid integer'
4.【422】Age <= 0            (str: "User", int: -1)        =>  'Age must be greater than 0.'

5.【200】Name with Space     (str: "  User  ", int: 10)    =>  'Add User Successfully'
6.【422】Name is empty       (str: ""          , int: 10)  =>  'Name cannot be Empty.
7.【422】Name is empty(mul)  (str: "          ", int: 10)  =>  'Name cannot be Empty.'
8.【422】Name is not string  (int: 123         , int: 10)  =>  'Input should be a valid string'
9.【200】Same name to update ("User", 13) -> ("User", 10)  =>  'Add User Successfully'

10.【422] Name Field doesn't exist (Non, int: 23)                    =>  'Field required'
11.【422] Age Field doesn't exist (str:"User", Non)                  =>  'Field required'
12.【422] Both of Name and Age Field don't exist (Non, Non)          =>  'Field required'
"""

def test_create_user_by_post_api():
    response = client.post("/users", json={"name": "Zavier", "age":23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add Zavier Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age":23} in response.json()
    assert len(response.json()) == 1

def test_create_user_by_post_api_with_age_is_str_number():
    response = client.post("/users", json={"name": "Zavier", "age": "23"})
    assert response.status_code == 200
    assert 'Add Zavier Successfully' in response.json()['message']

def test_create_user_by_post_api_with_age_is_not_number():
    response = client.post("/users", json={"name": "Zavier", "age": "abc"})
    assert response.status_code == 422
    assert 'Input should be a valid integer' in response.json()["detail"][0]["msg"]

def test_create_user_by_post_api_with_age_is_not_larger_than_zero():
    response = client.post("/users", json={"name": "Zavier", "age": -1})
    assert response.status_code == 422
    assert 'Age must be greater than 0.' in response.json()["detail"]

def test_create_user_by_post_api_with_space_in_name():
    response = client.post("/users", json={"name": "  Zavier  ", "age": 23})
    assert response.status_code == 200
    assert 'Add Zavier Successfully' in response.json()['message']

def test_create_user_by_post_api_with_name_is_empty():
    response = client.post("/users", json={"name": "", "age": 10})
    print(response.json())
    assert response.status_code == 422
    assert 'Name cannot be Empty.' in response.json()["detail"]

def test_create_user_by_post_api_with_only_multiple_space_in_name():
    response = client.post("/users", json={"name": "    ", "age": 23})
    assert response.status_code == 422
    assert "Name cannot be Empty." in response.json()["detail"]

def test_create_user_by_post_api_with_not_str_name():
    response = client.post("/users", json={"name": 123, "age": 23})
    assert response.status_code == 422
    assert 'Input should be a valid string' in response.json()['detail'][0]['msg']

def test_create_user_by_post_api_with_same_name_to_update():
    response = client.post("/users", json={"name": "Zavier", "age": 23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add Zavier Successfully"

    response = client.post("/users", json={"name": "Zavier", "age": 20})
    assert response.status_code == 200
    assert response.json()["message"] == "Add Zavier Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 23} not in response.json()
    assert {"name": "Zavier", "age": 20} in response.json()
    assert len(response.json()) == 1

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

"""
Delete User
1.【200】User exist in db             => "Delete User Successfully"
2.【200】User doesn't exist in db     => "User does not exist"
"""
def test_delete_users_by_del_api():
    response = client.post("/users", json={"name": "Zavier", "age":25})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age":25} in response.json()
    assert len(response.json()) == 1

    response = client.delete("/users/Zavier")
    assert response.status_code == 200
    assert response.json()["message"] == "Delete Zavier Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 25} not in response.json()
    assert len(response.json()) == 0

def test_delete_users_by_del_api_with_name_does_not_exist():
    response = client.delete("/users/Zavier")
    assert response.status_code == 200
    assert response.json()["message"] == "Zavier does not exist"

"""
Upload CSV + Add User
1.【200】Normal Case (All Valid Data)  => (data/backend_users.csv)        => "Add Users From CSV Successfully"

2.【200】Not All Age is Valid          => (data/test_ageIsNotValid.csv)     => * Only Store Valid Data *
3.【200】Not All Name is Valid         => (data/test_nameIsNotValid.csv)  => * Only Store Valid Data *

4.【422】Empty CSV                     => (data/test_emptyFile.csv)       => "No columns to parse"
5.【422】Only Name Field exist in CSV  => (data/test_onlyNameField.csv)   => "Age"
"""
def test_upload_users_by_post_api():
    file_path = os.path.join(ROOT, "data/backend_users.csv")
    assert os.path.exists(file_path) is True

    with open(file_path,'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("backend_users.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

        csvfile.seek(0)  # go back to the start of csv file
        df = pd.read_csv(csvfile)
        totalData = df.shape[0]

    assert response.status_code == 200
    assert "Add Users From CSV Successfully" in response.json()["message"]

    response = client.get("/users")
    assert response.status_code == 200
    assert totalData == len(response.json())

def test_upload_users_by_post_api_with_empty_csv():
    file_path = os.path.join(ROOT, 'data/test_emptyFile.csv')
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as readFile:
        response = client.post("/users/upload", files={"file": ("test_emptyFile.csv", readFile, 'text/csv')})
        assert response.status_code == 422
        assert "No columns to parse" in response.json()["detail"]

def test_upload_users_by_post_api_with_only_one_field():
    file_path = os.path.join(ROOT, 'data/test_onlyNameField.csv')
    assert os.path.exists(file_path) is True

    with open(file_path,'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("test_onlyNameField.csv", csvfile, 'text/csv')})
        assert response.status_code == 422
        assert 'Age' in response.json()["detail"]

def test_upload_users_by_post_api_with_age_is_not_valid():
    file_path = os.path.join(ROOT, 'data/test_ageIsNotValid.csv')
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_ageIsNotValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_upload_users_by_post_api_with_name_is_not_valid():
    file_path = os.path.join(ROOT, 'data/test_nameIsNotValid.csv')
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_ageIsNotValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

"""
Calculate Average of each group 
1.【200】Normal Case (All Valid Data)  => (data/backend_users.csv)        => response.json()) == {...}

2.【200】Not All Age is Valid          => (data/test_ageIsNotValid.csv)   => response.json()) == {...}
3.【200】Not All Name is Valid         => (data/test_nameIsNotValid.csv)  => response.json()) == {...}

4.【200】Empty CSV                     => (data/test_emptyFile.csv)       => response.json()) == {}
5.【200】Only Name Field exist in CSV  => (data/test_onlyNameField.csv)   => response.json()) == {}
"""

def calcualteGroupAndAverage(file_path):
    dictionary = {}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)

        for row in rows:
            try:
                name = row[0]
                age = row[1]

                if len(name.strip()) > 0 and age.isdigit() and int(age) > 0:
                    first_character = name.strip()[0]
                    if first_character in dictionary:
                        dictionary[first_character].append(int(age))
                    else:
                        dictionary[first_character] = [int(age)]
            except IndexError:
                return {}

    sorted_dict = dict(sorted(dictionary.items()))

    resultDict = {}

    for key, valueList in sorted_dict.items():
        resultDict[key] = sum(valueList)/len(valueList)

    return resultDict

def test_average_age_of_each_group_by_get_api():
    file_path = os.path.join(ROOT, "data/backend_users.csv")
    assert os.path.exists(file_path) is True

    with open(file_path,'rb') as csvfile:
        response = client.post("/users/upload", files={"file":("backend_users.csv", csvfile, 'text/csv')})
        assert response.status_code == 200


    expectedJson = calcualteGroupAndAverage(file_path)
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == expectedJson

def test_average_age_of_each_group_by_get_api_with_age_is_not_valid():
    file_path = os.path.join(ROOT, 'data/test_ageIsNotValid.csv')
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_ageIsNotValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    expectedJson = calcualteGroupAndAverage(file_path)
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == expectedJson

def test_average_age_of_each_group_by_get_api_with_name_is_not_valid():
    file_path = os.path.join(ROOT, 'data/test_nameIsNotValid.csv')
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_ageIsNotValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    expectedJson = calcualteGroupAndAverage(file_path)
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == expectedJson

def test_average_age_of_each_group_by_get_api_with_empty_csv():
    file_path = os.path.join(ROOT, "data/test_emptyFile.csv")
    assert os.path.exists(file_path) is True

    expectedJson = calcualteGroupAndAverage(file_path)
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == expectedJson

def test_average_age_of_each_group_by_get_api_with_only_one_field():
    file_path = os.path.join(ROOT, 'data/test_onlyNameField.csv')
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_onlyNameField.csv", csvfile, 'text/csv')})
        assert response.status_code == 422

    expectedJson = calcualteGroupAndAverage(file_path)
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == expectedJson