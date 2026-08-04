def test_anturit_get(client):
    response = client.get("/anturit")
    assert response.status_code == 200
    assert isinstance(response.json(), list)