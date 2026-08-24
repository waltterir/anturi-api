from app.models.models import LohkoDB, TilamuutosDB
from app.crud.anturit_crud import create_anturi
from sqlmodel import select


# ---------- GET /anturit ----------

def test_anturit_get(client):
    response = client.get("/anturit")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------- POST /anturit/ ----------

def test_anturi_create_löytyy(client, session):
    lohko = LohkoDB(lohko_name="Testilohko")
    session.add(lohko)
    session.commit()
    session.refresh(lohko)

    payload = {
        "anturi_name": "Testianturi", 
        "lohko_id": lohko.id,
        "tila": "normal"
    }
    
    response = client.post("/anturit/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["anturi_name"] == "Testianturi"
    assert data["lohko_id"] == lohko.id
    assert data["id"] is not None


def test_anturi_create_ei_löydy(client):
    payload = {
        "anturi_name": "Testianturi",
        "lohko_id": 999,
        "tila": "normal"
    }

    response = client.post("/anturit/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Lohko not found"


# ---------- GET /anturit/{id}/tilamuutokset ----------

def test_get_anturi_tilamuutos_ei_loydy(client):
    response = client.get("/anturit/999/tilamuutokset")
    assert response.status_code == 404


# ---------- PUT /anturit/{id} ----------

def test_update_anturi_ei_loydy(client):
    payload = {"lohko_id": 1, "tila": "normal"}
    response = client.put("/anturit/999", json=payload)
    assert response.status_code == 404


def test_update_anturi_tila_muuttuu_luo_tilamuutoksen(client, session, anturi):
    payload = {"lohko_id": anturi.lohko_id, "tila": "error"}
    response = client.put(f"/anturit/{anturi.id}", json=payload)

    assert response.status_code == 200
    assert response.json()["tila"] == "error"

    tilamuutokset = session.exec(
        select(TilamuutosDB).where(TilamuutosDB.anturi_id == anturi.id)
    ).all()
    assert len(tilamuutokset) == 1


def test_update_anturi_sama_tila_ei_luo_tilamuutosta(client, session, anturi):
    payload = {"lohko_id": anturi.lohko_id, "tila": "normal"}  
    client.put(f"/anturit/{anturi.id}", json=payload)

    tilamuutokset = session.exec(
        select(TilamuutosDB).where(TilamuutosDB.anturi_id == anturi.id)
    ).all()
    assert len(tilamuutokset) == 0


def test_update_anturi_uusi_lohko_ei_loydy(client, anturi):
    payload = {"lohko_id": 999, "tila": anturi.tila.value}
    response = client.put(f"/anturit/{anturi.id}", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Lohko not found"


