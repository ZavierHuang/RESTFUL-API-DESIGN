import os

import pathlib
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

ROOT = pathlib.Path(__file__).resolve().parent.parent

@pytest.fixture(autouse=True)
def setUp():
    print("SETUP")
    response = client.post("/init")
    assert response.status_code == 200

"""
Clear User List
"""
def test_clear_user_list():
    response = client.post("/init")
    assert response.status_code == 200
    assert 'Clear User List Successfully' in response.json()['message']

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

"""
Get User List
"""
def test_get_user_list_by_get_api():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []


"""
Add User
1.【200】Normal Case         (str: "User", int: 10)        =>  'Add User Successfully'

2.【200】Age is str number   (str: "User", int: "10")      =>  'Add User Successfully'
3.【422】Age is not number   (str: "User", str: "ab")      =>  'Input should be a valid integer'
4.【422】Age <= 0            (str: "User", int: -1)        =>  'Age must be greater than 0.'

**** ADD
【200】Age is float number (Integer)      (str: "User", float:10.0)              =>  'Add User Successfully'
【422】Age is float number (not Integer)  (str: "User", float:10.5)              =>  'Input should be a valid integer'
【200】Age is str number with space       (str: "User", str: "     10    ")      =>  'Add User Successfully'
【422】Age is str number with space (mid) (str: "User", str: " 1  0  ")          =>  'Input should be a valid integer'
****

5.【200】Name with Space     (str: "  User  ", int: 10)    =>  'Add User Successfully'
6.【422】Name is empty       (str: ""          , int: 10)  =>  'Name cannot be Empty.
7.【422】Name is empty(mul)  (str: "          ", int: 10)  =>  'Name cannot be Empty.'
8.【422】Name is not string  (int: 123         , int: 10)  =>  'Input should be a valid string'

**** MODIFY
9.【200】Update the age      ("User", 13) -> ("User", 10)  =>  'Add User Successfully'
----------------------------------------------------------------------------------------
9.【409】name already exist  ("User", 13)                  =>  'User already exist'
****

10.【422] Name Field doesn't exist (Non, int: 23)                    =>  'Field required'
11.【422] Age Field doesn't exist (str:"User", Non)                  =>  'Field required'
12.【422] Neither the name nor the age field exists (Non, Non)       =>  'Field required'
"""

def test_create_user_by_post_api_age_is_float_number_with_integer():
    response = client.post("/users", json={"name": "Zavier", "age": 10.0})
    assert response.status_code == 200
    assert response.json()["message"] == "Add Zavier Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 10} in response.json()
    assert len(response.json()) == 1

def test_create_user_by_post_api_age_is_float_number_with_not_integer():
    response = client.post("/users", json={"name": "Zavier", "age": 10.5})
    assert response.status_code == 422
    assert "Input should be a valid integer" in response.json()['detail'][0]['msg']

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_create_user_by_post_api_age_is_str_number_with_spaces():
    response = client.post("/users", json={"name": "Zavier", "age": "   10   "})
    assert response.status_code == 200
    assert response.json()["message"] == "Add Zavier Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 10} in response.json()
    assert len(response.json()) == 1

def test_create_user_by_post_api_age_is_str_number_with_middle_spaces():
    response = client.post("/users", json={"name": "Zavier", "age": "   1  0   "})
    assert response.status_code == 422
    assert "Input should be a valid integer" in response.json()['detail'][0]['msg']

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_create_user_by_post_api():
    response = client.post("/users", json={"name": "Zavier", "age": 23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add Zavier Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 23} in response.json()
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


def test_create_user_by_post_api_with_same_name():
    response = client.post("/users", json={"name": "Zavier", "age": 23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add Zavier Successfully"

    response = client.post("/users", json={"name": "Zavier", "age": 20})
    assert response.status_code == 409
    assert response.json()["detail"] == "Zavier Already Exist"

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"name": "Zavier", "age": 23}]


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

*** Modify
2.【200】User doesn't exist in db     => "User does not exist"
--------------------------------------------------------------
2.【404】User doesn't exist in db     => "User does not exist"
"""


def test_delete_users_by_del_api():
    response = client.post("/users", json={"name": "Zavier", "age": 25})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 25} in response.json()
    assert len(response.json()) == 1

    response = client.delete("/users/Zavier")
    assert response.status_code == 200
    assert response.json()["message"] == "Delete Zavier Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "Zavier", "age": 25} not in response.json()
    assert response.json() == []


def test_delete_users_by_del_api_with_name_does_not_exist():
    response = client.delete("/users/Zavier")
    assert response.status_code == 404
    assert response.json()["detail"] == "Zavier does not exist"


"""
PUT (Update User age)
1.【200】Normal Case (user exist in db)
2.【404】User does not exist in db
"""

def test_update_user_by_put_api():
    response = client.post("/users", json={"name": "Zavier", "age": 25})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"name": "Zavier", "age": 25}]

    response = client.put("/users/", json={"name": "Zavier", "age": 20})
    assert response.status_code == 200
    assert response.json()['message'] == "Zavier Age Update Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"name": "Zavier", "age": 20}]

def test_update_user_by_put_api_but_name_does_not_exist():
    response = client.post("/users", json={"name": "Zavier", "age": 25})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"name": "Zavier", "age": 25}]

    response = client.put("/users/", json={"name": "User", "age": 20})
    assert response.status_code == 404
    assert "User does not Exist" == response.json()['detail']

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"name": "Zavier", "age": 25}]

"""
Upload CSV + Add User
1.【200】Normal Case (All Valid Data)  => (data/normal_user.csv)        => "Add Users From CSV Successfully"

2.【200】Not All Age is Valid          => (data/test_NotAllAgeIsValid.csv)   => * Only Store Valid Data *
3.【200】Not All Name is Valid         => (data/test_NotAllNameIsValid.csv)  => * Only Store Valid Data *
4.【200】Invalid Data Mix              => (data/test_InvalidDataMix.csv)     => * Only Store Valid Data *

5.【422】Empty CSV                     => (data/test_emptyFile.csv)       => "No columns to parse"
6.【422】Only Name Field exist in CSV  => (data/test_onlyNameField.csv)   => "Age"
7.【422】No Label in CSV               => (data/test_NoLabel.csv)         => "Name"
8.【400】Not CSV File                  => (data/test_PDF.pdf)             => "Only CSV files are allowed"
"""


def test_upload_users_by_post_api():
    file_path = f'{ROOT}/data/normal_user.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("normal_user.csv", csvfile, 'text/csv')})
        assert response.status_code == 200

    assert response.status_code == 200
    assert "Add Users From CSV Successfully (34/34)" in response.json()["message"]

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 34


def test_upload_users_by_post_api_with_age_is_not_valid():
    file_path = f'{ROOT}/data/test_NotAllAgeIsValid.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_NotAllAgeIsValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200
        assert "Add Users From CSV Successfully (2/3)" in response.json()["message"]

    expectedJson = [{'name': 'Bob', 'age': 11}, {'name': 'Charlie', 'age': 12}]

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == expectedJson


def test_upload_users_by_post_api_with_name_is_not_valid():
    file_path = f'{ROOT}/data/test_NotAllNameIsValid.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_NotAllAgeIsValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200
        assert "Add Users From CSV Successfully (2/4)" in response.json()["message"]

    expectedJson = [{'name': 'Alice', 'age': 13}, {'name': 'Charlie', 'age': 12}]

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == expectedJson


def test_upload_users_by_post_api_with_invalid_data_mix():
    file_path = f'{ROOT}/data/test_InValidDataMix.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_invalidDataMix.csv", csvfile, 'text/csv')})
        assert response.status_code == 200
        assert "Add Users From CSV Successfully (1/6)" in response.json()["message"]

    expectedJson = [{'name': 'User', 'age': 30}]
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == expectedJson


def test_upload_users_by_post_api_with_empty_csv():
    file_path = f'{ROOT}/data/test_emptyFile.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as readFile:
        response = client.post("/users/upload", files={"file": ("test_emptyFile.csv", readFile, 'text/csv')})
        assert response.status_code == 422
        assert "No columns to parse" in response.json()["detail"]

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_upload_users_by_post_api_with_only_one_field():
    file_path = f'{ROOT}/data/test_onlyNameField.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_onlyNameField.csv", csvfile, 'text/csv')})
        assert response.status_code == 422
        assert 'Age' in response.json()["detail"]

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_upload_users_by_post_api_with_no_label_in_csv():
    file_path = f'{ROOT}/data/test_NoLabelData.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_NoLabelData.csv", csvfile, 'text/csv')})
        assert response.status_code == 422
        assert 'Name' in response.json()["detail"]

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_users_by_post_api_with_not_csv_file():
    file_path = f'{ROOT}/data/test_PDF.pdf'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as pdfFile:
        response = client.post("/users/upload", files={"file": ("test_PDF.pdf", pdfFile, 'application/pdf')})
        assert response.status_code == 400
        assert 'Only CSV files are allowed' in response.json()["detail"]

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

"""
Calculate Average of each group 
1.【200】Normal Case (All Valid Data)  => (data/normal_user.csv)           => response.json() == {...}, 14 groups

2.【200】Not All Age is Valid          => (data/test_NotAllAgeIsValid.csv)   => response.json() == {...}, 2 groups
3.【200】Not All Name is Valid         => (data/test_NtAllNameIsValid.csv)   => response.json() == {...}, 2 groups
4.【200】Invalid Data Mix              => (data/test_InValidDataMix.csv)     => response.json() == {...}, 1 groups

5.【200】Empty CSV                     => (data/test_emptyFile.csv)       => response.json() == {}, 0 groups
6.【200】Only Name Field exist in CSV  => (data/test_onlyNameField.csv)   => response.json() == {}, 0 groups
7.【200】No Label in CSV               => (data/test_NoLabelData.csv)     => response.json() == {}, 0 groups
8.【200】Not CSV File                  => (data/test_PDF.pdf)             => response.json() == {}, 0 groups
"""


def test_average_age_of_each_group_by_get_api():
    file_path = f'{ROOT}/data/normal_user.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("normal_user.csv", csvfile, 'text/csv')})
        assert response.status_code == 200
        assert "Add Users From CSV Successfully" in response.json()["message"]

    expectedJson = {'A': 9.0, 'B': 14.0, 'C': 16.0, 'E': 29.0, 'F': 6.0,
                    'I': 13.0, 'K': 14.0, 'M': 27.0, 'N': 16.5, 'P': 16.25,
                    'R': 14.0, 'S': 20.25, 'V': 24.0, 'W': 9.5}

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert len(response.json()) == 14
    assert response.json() == expectedJson


def test_average_age_of_each_group_by_get_api_with_age_is_not_valid():
    file_path = f'{ROOT}/data/test_NotAllAgeIsValid.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_NotAllAgeIsValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200
        assert "Add Users From CSV Successfully" in response.json()["message"]

    expectedJson = {'B': 11.0, 'C': 12.0}
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == expectedJson


def test_average_age_of_each_group_by_get_api_with_name_is_not_valid():
    file_path = f'{ROOT}/data/test_NotAllNameIsValid.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_NotAllAgeIsValid.csv", csvfile, 'text/csv')})
        assert response.status_code == 200
        assert "Add Users From CSV Successfully" in response.json()["message"]

    expectedJson = {'A': 13.0, 'C': 12.0}
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == expectedJson


def test_average_age_of_each_group_by_get_api_with_invalid_data_mix():
    file_path = f'{ROOT}/data/test_InvalidDataMix.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_InvalidDataMix.csv", csvfile, 'text/csv')})
        assert response.status_code == 200
        assert "Add Users From CSV Successfully" in response.json()["message"]

    expectedJson = {'U': 30.0}
    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == expectedJson


def test_average_age_of_each_group_by_get_api_with_empty_csv():
    file_path = f'{ROOT}/data/test_emptyFile.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_emptyFile.csv", csvfile, 'text/csv')})
        assert response.status_code == 422
        assert 'No columns to parse from file' in response.json()["detail"]

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == {}


def test_average_age_of_each_group_by_get_api_with_only_one_field():
    file_path = f'{ROOT}/data/test_onlyNameField.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_onlyNameField.csv", csvfile, 'text/csv')})
        assert response.status_code == 422
        assert 'Age' in response.json()["detail"]

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == {}


def test_average_age_of_each_group_by_get_api_with_no_label_in_csv():
    file_path = f'{ROOT}/data/test_NoLabelData.csv'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_NoLabelData.csv", csvfile, 'text/csv')})
        assert response.status_code == 422
        assert 'Name' in response.json()["detail"]

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == {}

def test_average_age_of_each_group_by_get_api_with_not_csv_file():
    file_path = f'{ROOT}/data/test_PDF.pdf'
    assert os.path.exists(file_path) is True

    with open(file_path, 'rb') as csvfile:
        response = client.post("/users/upload", files={"file": ("test_PDF.pdf", csvfile, 'application/pdf')})
        assert response.status_code == 400
        assert 'Only CSV files are allowed' in response.json()["detail"]

    response = client.get("/users/averageAge")
    assert response.status_code == 200
    assert response.json() == {}