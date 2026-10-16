def test_health(client):
    response = client.get("/health")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "broken"