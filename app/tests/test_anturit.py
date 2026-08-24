from datetime import datetime, timedelta
from app.models.models import LohkoDB, TilamuutosDB, AnturiDB, MittausDB, AnturiTila
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


# ---------- GET /anturit (suodatus) ----------

def test_get_anturit_suodattaa_id_lla(client, anturi):
    response = client.get(f"/anturit?id={anturi.id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == anturi.id


def test_get_anturit_suodattaa_tilalla(client, session, lohko):
    a1 = AnturiDB(anturi_name="A1", lohko_id=lohko.id, tila=AnturiTila.NORMAL)
    a2 = AnturiDB(anturi_name="A2", lohko_id=lohko.id, tila=AnturiTila.ERROR)
    session.add_all([a1, a2])
    session.commit()

    response = client.get("/anturit?tila=error")

    assert response.status_code == 200
    data = response.json()
    assert all(item["tila"] == "error" for item in data)
    assert any(item["id"] == a2.id for item in data)


# ---------- GET /anturit/{id}/mittaus_tulokset ----------

def test_get_mittaus_tulokset_ei_loydy(client):
    response = client.get("/anturit/999/mittaus_tulokset")
    assert response.status_code == 404


def test_get_mittaus_tulokset_error_tilassa(client, session, lohko):
    anturi = AnturiDB(anturi_name="Vika-anturi", lohko_id=lohko.id, tila=AnturiTila.ERROR)
    session.add(anturi)
    session.commit()
    session.refresh(anturi)

    response = client.get(f"/anturit/{anturi.id}/mittaus_tulokset")
    assert response.status_code == 409


def test_get_mittaus_tulokset_page_alle_yhden(client, anturi):
    response = client.get(f"/anturit/{anturi.id}/mittaus_tulokset?page=0")
    assert response.status_code == 400


def test_get_mittaus_tulokset_limit_alle_yhden(client, anturi):
    response = client.get(f"/anturit/{anturi.id}/mittaus_tulokset?limit=0")
    assert response.status_code == 400


def test_get_mittaus_tulokset_limit_yli_sadan(client, anturi):
    response = client.get(f"/anturit/{anturi.id}/mittaus_tulokset?limit=101")
    assert response.status_code == 400


def test_get_mittaus_tulokset_start_time_jalkeen_end_time(client, anturi):
    response = client.get(
        f"/anturit/{anturi.id}/mittaus_tulokset"
        "?start_time=2024-01-02T00:00:00&end_time=2024-01-01T00:00:00"
    )
    assert response.status_code == 400


def test_get_mittaus_tulokset_onnistuu_ilman_mittauksia(client, anturi):
    response = client.get(f"/anturit/{anturi.id}/mittaus_tulokset")

    assert response.status_code == 200
    data = response.json()
    assert data["anturi"]["id"] == anturi.id
    assert data["mittaukset"] == []


def test_get_mittaus_tulokset_jarjestys(client, session, anturi):
    now = datetime(2024, 1, 1, 12, 0, 0)
    for i in range(3):
        session.add(MittausDB(anturi_id=anturi.id, mittaus_arvo=float(i), aikaleima=now + timedelta(minutes=i)))
    session.commit()

    response = client.get(f"/anturit/{anturi.id}/mittaus_tulokset")

    assert response.status_code == 200
    mittaukset = response.json()["mittaukset"]
    assert len(mittaukset) == 3
    assert mittaukset[0]["mittaus_arvo"] == 2.0
    assert mittaukset[1]["mittaus_arvo"] == 1.0
    assert mittaukset[2]["mittaus_arvo"] == 0.0


def test_get_mittaus_tulokset_suodattaa_aikavalilla(client, session, anturi):
    base = datetime(2024, 1, 1, 0, 0, 0)
    for i in range(5):
        session.add(MittausDB(anturi_id=anturi.id, mittaus_arvo=float(i), aikaleima=base + timedelta(days=i)))
    session.commit()

    response = client.get(
        f"/anturit/{anturi.id}/mittaus_tulokset"
        "?start_time=2024-01-02T00:00:00&end_time=2024-01-04T00:00:00"
    )

    assert response.status_code == 200
    mittaukset = response.json()["mittaukset"]
    assert len(mittaukset) == 3


def test_get_mittaus_tulokset_paginointi(client, session, anturi):
    base = datetime(2024, 1, 1, 0, 0, 0)
    for i in range(15):
        session.add(MittausDB(anturi_id=anturi.id, mittaus_arvo=float(i), aikaleima=base + timedelta(minutes=i)))
    session.commit()

    sivu1 = client.get(f"/anturit/{anturi.id}/mittaus_tulokset?page=1&limit=10")
    sivu2 = client.get(f"/anturit/{anturi.id}/mittaus_tulokset?page=2&limit=10")

    assert len(sivu1.json()["mittaukset"]) == 10
    assert len(sivu2.json()["mittaukset"]) == 5
    id_sivu1 = {m["id"] for m in sivu1.json()["mittaukset"]}
    id_sivu2 = {m["id"] for m in sivu2.json()["mittaukset"]}
    assert id_sivu1.isdisjoint(id_sivu2)


# ---------- GET /anturit/{id}/tilamuutokset (onnistuminen + suodatus) ----------

def test_get_anturi_tilamuutos_palauttaa_kaikki(client, session, anturi):
    session.add(TilamuutosDB(anturi_id=anturi.id, tila=AnturiTila.NORMAL, aikaleima=datetime(2024, 1, 1)))
    session.add(TilamuutosDB(anturi_id=anturi.id, tila=AnturiTila.ERROR, aikaleima=datetime(2024, 1, 2)))
    session.commit()

    response = client.get(f"/anturit/{anturi.id}/tilamuutokset")

    assert response.status_code == 200
    data = response.json()
    assert data["anturi_id"] == anturi.id
    assert len(data["tilamuutokset"]) == 2


def test_get_anturi_tilamuutos_suodattaa_tilalla(client, session, anturi):
    session.add(TilamuutosDB(anturi_id=anturi.id, tila=AnturiTila.NORMAL, aikaleima=datetime(2024, 1, 1)))
    session.add(TilamuutosDB(anturi_id=anturi.id, tila=AnturiTila.ERROR, aikaleima=datetime(2024, 1, 2)))
    session.commit()

    response = client.get(f"/anturit/{anturi.id}/tilamuutokset?tila=error")

    assert response.status_code == 200
    data = response.json()
    assert len(data["tilamuutokset"]) == 1
    assert data["tilamuutokset"][0]["tila"] == "error"

