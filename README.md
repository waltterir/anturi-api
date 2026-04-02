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

## Backend ja Arkkitehtuuri

- Modulaarinen projektirakenne (crud, database, models, routes)
- SQLite-integraatio SQLModelin kautta
- Perusvirheenkäsittely HTTPExceptioneilla
- Toteutettu riippuvuuksiin perustuva autentikointi (FastAPI Depends)
- Selkeä vastuunjako autentikoinnin, reitityksen ja tietokantakerroksen välillä

## Käyttöönotto ja ajaminen lokaalisti

1. #### Kopioi repositorio
   - git clone ... cd ...

2. #### Asenna riippuvuudet
   - pip install -r requirements.txt

3. #### Käynnistä sovellus

```md
uvicorn app.main:app --reload (Suositeltu)

TAI

fastapi dev app/main.py (FastAPI CLI)
```

4. Avaa API-dokumentaatio

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

- {
  "anturi": {
  "anturi_name": "Anturi A",
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

## Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
