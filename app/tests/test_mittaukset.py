from datetime import datetime
from app.models.models import MittausDB
from sqlmodel import select


# ---------- DELETE /mittaukset/{mittaus_id} ----------

def test_delete_mittaus_ei_loydy(client):
    response = client.delete("/mittaukset/999")
    assert response.status_code == 404


def test_delete_mittaus_onnistuu(client, session, anturi):
    mittaus = MittausDB(anturi_id=anturi.id, mittaus_arvo=10.0, aikaleima=datetime(2024, 1, 1))
    session.add(mittaus)
    session.commit()
    session.refresh(mittaus)

    response = client.delete(f"/mittaukset/{mittaus.id}")

    assert response.status_code == 204

    tulos = session.exec(select(MittausDB).where(MittausDB.id == mittaus.id)).first()
    assert tulos is None