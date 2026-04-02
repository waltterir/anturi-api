# Anturi API

REST API lämpötila-anturidatan keräämiseen.
Toteutettu kurssin päättötyönä.

## Status

Ydinominaisuudet toteutettu

## Ydinominaisuudet

- Toteutettu täydet CRUD-operaatiot antureille, lohkoille ja mittauksille
- Relaationaaliset datamallit (Lohko → Anturi → Mittaus)

- Anturien hallinta:
  - Anturien haku ja luonti
  - Yksittäisen anturin mittaustulosten haku
  - Anturin tilamuutosten seuranta

- Lohkojen hallinta:
  - Lohkojen luonti
  - Lohkoon kuuluvien anturien haku

- Mittausten hallinta:
  - Uusien mittausten luonti antureille
  - Mittausten poistaminen
  - Mittausten haku anturin perusteella
  - Aikavälisuodatus mittauksille (start_time, end_time)

- Offset-pohjainen paginointi (page & limit)

- Suodatus:
  - anturit tilan ja mitta-arvojen perusteella
  - lohkot lohko_id:n perusteella
 
## Vaatimusten täyttyminen

Projektissa on toteutettu kaikki annetut backend-vaatimukset:

Hallinta:
- Antureiden lisääminen järjestelmään
- Anturin tilan muuttaminen
- Anturin lohkon muuttaminen
- Yksittäisen mittatuloksen poistaminen

Datan haku:
- Kaikkien antureiden listaus (tunniste, lohko ja tila)
- Lohkokohtainen anturien listaus (sisältäen viimeisimmän mittauksen)
- Yksittäisen anturin kaikki tiedot (sisältäen mittaukset)
- Mittausten rajaaminen aikavälille (start_time, end_time)
- Oletuksena rajattu määrä tuloksia (paginointi)

Lisäksi:
- Anturien suodatus tilan mukaan
- Anturin tilamuutosten seuranta

## Backend ja Arkkitehtuuri

Modulaarinen projektirakenne (crud, database, models, routes)
SQLite-integraatio SQLModelin kautta

API noudattaa REST-periaatteita ja käyttää HTTP-metodeja seuraavasti:
- GET: datan haku
- POST: uusien resurssien luonti
- DELETE: resurssien poistaminen

Virhetilanteita käsitellään HTTPExceptioneilla. API palauttaa selkeät HTTP-statuskoodit, kuten:
- 404 jos resurssia ei löydy
- 400 virheelliselle syötteelle

Selkeä vastuunjako reitityksen ja tietokantakerroksen välillä

## Käyttöönotto ja ajaminen lokaalisti

1. #### Kopioi repositorio
   - git clone https://github.com/waltterir/anturi-api.git
   - cd anturi-api

2. #### Luo ja aktivoi virtuaaliympäristö
   - python -m venv .venv

   Aktivoi ympäristö:

   Windows:
   - .venv\Scripts\activate

3. #### Asenna riippuvuudet
   - pip install -r requirements.txt

4. #### Käynnistä sovellus

```bash
uvicorn app.main:app --reload  # Suositeltu

# TAI

fastapi dev app/main.py        # FastAPI CLI
```

#### Avaa API-dokumentaatio
http://localhost:8000/docs

## 📁 Projektin rakenne

```text
app/
├── main.py
├── routes/        # API-endpointit
├── models/        # Tietokantamallit
├── crud/          # Tietokanta operaatiot
├── database/      # DB-alustus
```

## Esimerkkikutsu

- GET /anturit/{anturi_id}/mittaus_tulokset?page=1&limit=10

## Esimerkkivastaus

```md
{
"anturi": {
"anturi_name": "Anturi 32",
"lohko_id": 1,
"tila": "error",
"id": 1
},
"mittaukset": [
{
"anturi_id": 1,
"mittaus_arvo": 20.5,
"aikaleima": "2026-04-02T10:31:26.623000",
"id": 1
}
]
}
```

## Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
