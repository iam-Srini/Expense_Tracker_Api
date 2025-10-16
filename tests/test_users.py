from fastapi import status


def test_create_user_success(client):
    payload = {
        "name": "Test User",
        "email": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data     
    assert "created_at" in data
    assert "password" not in data  # Ensure password is not returned


def test_create_user_existing_email(client):
    payload = {
        "name": "Test User",
        "email": "testuser@gmail.com",
        "password": "stronG@123"
    }
    # Create the first user
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    # Attempt to create a second user with the same email
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Email already registered"


def test_create_user_invalid_email(client):
    payload = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    detail = data["detail"][0]
    assert detail["type"] == "value_error"
    assert "value is not a valid email address" in detail["msg"]

def test_create_user_password_no_digit(client):
    payload = {
        "name": "Weak Password User",
        "email": "testuser@gamil.com",
        "password": "weakpass"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    detail = data["detail"][0]
    assert "Password must contain at least one digit." in detail["msg"]
    assert detail["type"] == "value_error"


def test_create_user_password_no_uppercase(client):
    payload = {
        "name": "Weak Password User",
        "email": "testuser@gmail.com",
        "password": "weakpass1@"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    detail = data["detail"][0]
    assert "Password must contain at least one uppercase letter." in detail["msg"]
    assert detail["type"] == "value_error"  


def test_create_user_password_no_lowercase(client):
    payload = {
        "name": "Weak Password User",
        "email": "testuser@gmail.com",
        "password": "WEAKPASS1@"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    detail = data["detail"][0]
    assert "Password must contain at least one lowercase letter." in detail["msg"]
    assert detail["type"] == "value_error"


def test_create_user_password_no_special_char(client):
    payload = {
        "name": "Weak Password User",
        "email": "testuser@gmail.com",
        "password": "Weakpass1"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    detail = data["detail"][0]
    assert "Password must contain at least one special character." in detail["msg"]
    assert detail["type"] == "value_error"   


def test_create_user_password_too_short(client):
    payload = {
        "name": "Weak Password User",
        "email": "testuser@gmail.com",
        "password": "Wp1@"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    detail = data["detail"][0]
    assert "String should have at least 8 characters" in detail["msg"]
    assert detail["type"] == "string_too_short"


def test_create_user_password_too_long(client):
    payload = {
        "name": "Weak Password User",
        "email": "testuser@gmail.com",
        "password": "Weakpassword1@Weakpassword1@"
    }
    response = client.post("/users/", json=payload)
    print(response.json())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    detail = data["detail"][0]
    assert "String should have at most 20 characters" in detail["msg"]
    assert detail["type"] == "string_too_long"


def test_read_user_success(client):
    # First, create a user to read
    payload = {
        "name": "Read User",
        "email": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    user_id = response.json()["id"]
    # Now, read the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "password" not in data  # Ensure password is not returned
    assert "created_at" in data
    assert "id" in data


def test_read_user_not_found(client):
    response = client.get("/users/9999")  # Assuming this ID does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User not found"


def test_update_user_success(client):
    # First, create a user to update
    payload = {
        "name": "Update User",
        "email": "testuser@gmail.com",  
        "password": "stronG@123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    user_id = response.json()["id"]
    # Now, update the user
    update_payload = {
        "name": "Updated User",
        "email": "updatetestuser@gmail.com",
        "password": "NewstronG@123"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == update_payload["name"]
    assert data["email"] == update_payload["email"]
    assert "password" not in data  # Ensure password is not returned
    assert "created_at" in data
    assert "id" in data


def test_update_user_not_found(client):
    update_payload = {
        "name": "Updated User",
        "email": "testuser@gmail.com",
        "password": "NewstronG@123"
    }
    response = client.put("/users/9999", json=update_payload)  # Assuming this ID does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User not found"   


def test_delete_user_success(client):
    # First, create a user to delete
    payload = {
        "name": "Delete User",
        "email": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=payload) 
    assert response.status_code == status.HTTP_201_CREATED
    user_id = response.json()["id"]
    # Now, delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify the user is deleted    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_not_found(client):
    response = client.delete("/users/9999")  # Assuming this ID does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User not found"
