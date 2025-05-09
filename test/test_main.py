from fastapi.testclient import TestClient

from main import app
from test.util import Util

client = TestClient(app)
util = Util()

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
    pass

def test_upload_users_by_post_api():
    pass

def test_average_age_by_get_api():
    pass
