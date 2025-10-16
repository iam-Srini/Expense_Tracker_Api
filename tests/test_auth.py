from fastapi import status

def test_login_user_success(client):
    # First, create a user to log in
    payload = {
        "name": "Login User",
        "email": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    # Now, attempt to log in
    login_payload = {
        "username": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_invalid_credentials(client):
    # Attempt to log in with invalid credentials
    login_payload = {
        "username": "invalid@gmail.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Incorrect email or password"

def test_refresh_token_success(client):
    # First, create a user to log in
    payload = {
        "name": "Refresh User",
        "email": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    # Now, log in to get tokens
    login_payload = {
        "username": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    refresh_token = data["refresh_token"]
    print("Refresh Token:", repr(refresh_token))
    # Now, attempt to refresh the access token
    response = client.post(f"/auth/refresh?refresh_token={refresh_token}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"   

def test_refresh_token_invalid_token(client):
    # Attempt to refresh with an invalid token
    invalid_refresh_token = "invalidtoken"
    response = client.post(f"/auth/refresh?refresh_token={invalid_refresh_token}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Invalid refresh token"        

def test_refresh_token_user_not_found(client):
    # Create a valid refresh token for a non-existent user
    from app.utils.security import create_refresh_token
    fake_email = "test@gmail.com"
    refresh_token = create_refresh_token({"sub": fake_email})
    # Attempt to refresh the access token
    print("Refresh Token for non-existent user:", repr(refresh_token))
    response = client.post(f"/auth/refresh?refresh_token={refresh_token}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    print("Response Data:", repr(data))
    assert data["detail"] == "User not found"   
