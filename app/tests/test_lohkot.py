from datetime import datetime

from app.models.models import AnturiDB, MittausDB, AnturiTila


# ---------- POST /lohkot/ ----------

def test_create_lohko_onnistuu(client):
    payload = {"lohko_name": "Testilohko"}

    response = client.post("/lohkot/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["lohko_name"] == "Testilohko"
    assert data["id"] is not None


# ---------- GET /lohkot/{id}/anturit ----------

def test_get_lohko_anturit_ei_loydy(client):
    response = client.get("/lohkot/999/anturit")
    assert response.status_code == 404


def test_get_lohko_anturit_tyhja_lista(client, lohko):
    response = client.get(f"/lohkot/{lohko.id}/anturit")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == lohko.id
    assert data["name"] == lohko.lohko_name
    assert data["anturit"] == []


def test_get_lohko_anturit_anturi_ilman_mittauksia(client, session, anturi):
    response = client.get(f"/lohkot/{anturi.lohko_id}/anturit")

    assert response.status_code == 200
    data = response.json()
    assert len(data["anturit"]) == 1
    assert data["anturit"][0]["id"] == anturi.id
    assert data["anturit"][0]["viimeisin_arvo"] is None
    assert data["anturit"][0]["viimeisin_aikaleima"] is None


def test_get_lohko_anturit_palauttaa_viimeisimman_mittauksen(client, session, anturi):
    session.add(MittausDB(anturi_id=anturi.id, mittaus_arvo=1.0, aikaleima=datetime(2024, 1, 1)))
    session.add(MittausDB(anturi_id=anturi.id, mittaus_arvo=3.0, aikaleima=datetime(2024, 1, 3)))
    session.add(MittausDB(anturi_id=anturi.id, mittaus_arvo=2.0, aikaleima=datetime(2024, 1, 2)))
    session.commit()

    response = client.get(f"/lohkot/{anturi.lohko_id}/anturit")

    assert response.status_code == 200
    anturi_data = response.json()["anturit"][0]
    assert anturi_data["viimeisin_arvo"] == 3.0
    assert anturi_data["viimeisin_aikaleima"] == "2024-01-03T00:00:00"


def test_get_lohko_anturit_useampi_anturi(client, session, lohko):
    anturi1 = AnturiDB(anturi_name="A1", lohko_id=lohko.id, tila=AnturiTila.NORMAL)
    anturi2 = AnturiDB(anturi_name="A2", lohko_id=lohko.id, tila=AnturiTila.ERROR)
    session.add_all([anturi1, anturi2])
    session.commit()

    response = client.get(f"/lohkot/{lohko.id}/anturit")

    data = response.json()
    assert len(data["anturit"]) == 2
    ids = {a["id"] for a in data["anturit"]}
    assert ids == {anturi1.id, anturi2.id}