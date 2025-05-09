from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_user_list_by_get_api():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user_by_post_api():
    response = client.post("/users", json={"name": "Zavier", "age":23})
    assert response.status_code == 200
    assert response.json()["message"] == "Add User Successfully"

    response = client.get("/users")
    assert {"name": "Zavier", "age":23} in response.json()


def test_delete_users_by_del_api():
    response = client.post("/users", json={"name": "John", "age":25})
    assert response.status_code == 200
    assert response.json()["message"] == "Delete User Successfully"

    response = client.get("/users")
    assert response.status_code == 200
    assert {"name": "John", "age":25} in response.json()

    response = client.delete("/users/{username}")
    assert response.status_code == 200
    assert {"name": "John", "age": 25} not in response.json()

def test_upload_users_by_post_api():
    pass

def test_average_age_by_get_api():
    pass
