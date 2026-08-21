def test_anturit_get(client):
    response = client.get("/anturit")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

from app.models import LohkoDB

def test_create_anturi(client, session):
    lohko = LohkoDB(lohko_name="Testilohko")
    session.add(lohko)
    session.commit()
    session.refresh(lohko)

    payload = {
        "anturi_name": "Testi",
        "lohko_id": lohko.id,
        "tila": "normal"
    }

    response = client.post("/anturit", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["anturi_name"] == "Testi"
    assert "id" in data