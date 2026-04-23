import uuid

def test_signup_and_login(client):
    unique_email = f"test_{uuid.uuid4()}@mail.com"

    response = client.post("/auth/signup", json={
        "name": "Test User",
        "email": unique_email,
        "password": "123",
        "role": "student"
    })

    assert response.status_code == 200