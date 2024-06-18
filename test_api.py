import pytest, string, random
from typing import Generator
from playwright.sync_api import APIRequestContext, Playwright


@pytest.fixture(scope="session")
def user_api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url="https://gorest.co.in"
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="session")
def user_ids():
    ids = []
    yield ids

def random_strings(length):
    letters = string.ascii_letters
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for i in range(length))
    payload = {
        "id": 6967498,
        "name": "Anal Nair",
        "email": "anal_nair-"+random_string+"@hintz.example",
        "gender": "female",
        "status": "active"
    }
    return payload
    
headers={
            "Authorization" : 
        }
def test_create_new_user(user_api_request_context: APIRequestContext, user_ids) -> None:
    payload = random_strings(8)
    response = user_api_request_context.post(
        url=f"/public/v2/users",
        headers=headers,
        data=payload
        )
    assert response.ok
    assert response.status == 201
    assert response.status_text == "Created"
    json_response = response.json()
    print("Create User API Response:\n{}".format(json_response))
    assert json_response["name"] == payload.get("name")
    user_ids.append(json_response["id"])

def test_get_user_details(user_api_request_context: APIRequestContext, user_ids) -> None:
    response = user_api_request_context.get(
        url=f"/public/v2/users/"+str(user_ids[0]),
        headers=headers
    )
    assert response.ok
    assert response.status == 200
    assert response.status_text == "OK"
    json_response = response.json()
    print("Create User API Response:\n{}".format(json_response))
    assert json_response["name"] == "Anal Nair"

def test_update_user_details(user_api_request_context: APIRequestContext, user_ids) -> None:
    payload = {
            "name": "Anal Nair Update"
            }
    response = user_api_request_context.put(
        url=f"/public/v2/users/"+str(user_ids[0]),
        headers=headers,
        data=payload
    )
    assert response.ok
    assert response.status == 200
    assert response.status_text == "OK"
    json_response = response.json()
    print("Create User API Response:\n{}".format(json_response))
    assert json_response["name"] == payload.get("name")


def test_delete_user(user_api_request_context: APIRequestContext, user_ids) -> None:
    response = user_api_request_context.delete(
        url=f"/public/v2/users/"+str(user_ids[0]),
        headers=headers
    )
    assert response.ok
    assert response.status == 204
    assert response.status_text == "No Content"
