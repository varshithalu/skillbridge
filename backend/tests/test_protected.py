def test_no_token_protected(client):
    response = client.get("/auth/me")
    assert response.status_code == 401