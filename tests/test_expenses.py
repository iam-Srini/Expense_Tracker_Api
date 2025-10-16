from fastapi import status

def test_create_expense_success(client):
    # First, create a user to associate the expense with
    user_payload = {
        "name": "Expense User",
        "email": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    login_payload = {
        "username": "testuser@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_200_OK
    print("Login Response:", repr(response.json()))
    token = response.json()["access_token"]
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}
    # Now, create an expense for that user
    expense_payload = {
        "amount": 50.75,
        "description": "Lunch at a restaurant",
        "expense_date": "2023-10-01",
        "category": "Food"
    }
    client.headers.update({"Authorization": f"Bearer {token}"})
    response = client.post("/expenses/", json=expense_payload)
    print("Expense Creation Response:", repr(response.json()))
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["amount"] == expense_payload["amount"]
    assert data["category"] == expense_payload["category"]
    assert data["description"] == expense_payload["description"]
    assert data["expense_date"] == expense_payload["expense_date"]
    assert "id" in data
    assert "user_id" in data


def test_create_expense_unauthorized(client):
    expense_payload = {
        "amount": 20.00,
        "description": "Taxi fare",
        "expense_date": "2023-10-02",
        "category": "Transport"
    }
    response = client.post("/expenses/", json=expense_payload)
    print("Unauthorized Expense Creation Response:", repr(response.json()))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Not authenticated"

def test_get_expense_not_found(client):
    # First, create a user and log in
    user_payload = {
        "name": "Expense User2",
        "email": "user@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    login_payload = {
        "username": "user@gmail.com",
        "password": "stronG@123"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_200_OK
    print("Login Response:", repr(response.json()))
    token = response.json()["access_token"]
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    # Attempt to get a non-existent expense
    response = client.get("/expenses/9999")  # Assuming 9999 is a non-existent expense ID
    print("Get Non-existent Expense Response:", repr(response.json()))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Expense not found"


def test_get_expense_unauthorized(client):
    response = client.get("/expenses/1")  # Attempt to get an expense without authentication
    print("Unauthorized Get Expense Response:", repr(response.json()))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Not authenticated"

def test_get_expenses_by_user(client):
    # First, create a user and log in
    user_payload = {
        "name": "Expense User3",
        "email": "user@example.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    login_payload = {
        "username": "user@example.com",
        "password": "stronG@123"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_200_OK
    print("Login Response:", repr(response.json()))
    token = response.json()["access_token"]
    assert token is not None
    client.headers.update({"Authorization": f"Bearer {token}"})
    # Create multiple expenses for that user
    expenses = [
        {"amount": 15.00, "description": "Coffee", "expense_date": "2023-10-03", "category": "Food"},
        {"amount": 30.00, "description": "Groceries", "expense_date": "2023-10-04", "category": "Food"},
        {"amount": 100.00, "description": "Monthly Rent", "expense_date": "2023-10-01", "category": "Housing"}
    ]
    for expense in expenses:
        response = client.post("/expenses/", json=expense)
        assert response.status_code == status.HTTP_201_CREATED
    # Now, retrieve expenses for the logged-in user
    response = client.get(f"/expenses/user/me")  # Assuming user ID is 1
    print("Get Expenses by User Response:", repr(response.json()))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # At least the 3 we just created
    for expense in data:
        assert "id" in expense
        assert "amount" in expense
        assert "description" in expense
        assert "expense_date" in expense
        assert "category" in expense
        assert "user_id" in expense
        assert expense["user_id"] == 1  # Ensure the expenses belong to the correct user


def test_delete_expense_success(client):
    # First, create a user and log in
    user_payload = {
        "name": "Expense User4",
        "email": "user@example.com",
        "password": "stronG@123"
    }
    response = client.post("/users/", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    login_payload = {
        "username": "user@example.com",
        "password": "stronG@123"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_200_OK
    print("Login Response:", repr(response.json()))
    token = response.json()["access_token"]
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    # Create an expense to delete
    expense_payload = {
        "amount": 75.00,
        "description": "Dinner",
        "expense_date": "2023-10-05",
        "category": "Food"
    }
    response = client.post("/expenses/", json=expense_payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    expense_id = response.json()["id"]
    # Now, delete the expense
    response = client.delete(f"/expenses/{expense_id}", headers=headers)
    print("Delete Expense Response:", repr(response.status_code))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify the expense is actually deleted
    response = client.get(f"/expenses/{expense_id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND    
    data = response.json()
    assert data["detail"] == "Expense not found"

def test_delete_expense_unauthorized(client):
    response = client.delete("/expenses/1")  # Attempt to delete an expense without authentication
    print("Unauthorized Delete Expense Response:", repr(response.json()))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Not authenticated"



