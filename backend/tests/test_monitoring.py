def test_monitoring_post_not_allowed(client):
    response = client.post("/monitoring/attendance")
    assert response.status_code == 404