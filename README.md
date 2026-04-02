# Anturi API

REST API lämpötila-anturidatan keräämiseen.
Toteutettu kurssin päättötyönä.

## Status

Ydinominaisuudet toteutettu

## Ydinominaisuudet

- Toteutettu täydet CRUD operaatiot antureille, lohkoille ja mittauksille.
- Relaationaaliset data mallinnukset (Lohko → Anturi → Mittaus)
- Endpointit hakemaan lohkon anturit ja antureiden mittaukset
- Offset-pohjainen paginointi (sivu ja limit)
- Suodatus:
  - anturit tilan ja mitta-arvojen perusteella
  - lohkot lohko_id:n perusteella

## Backend ja Arkkitehtuuri

- Modulaarinen projektirakenne (crud, database, models, routes)
- SQLite-integraatio SQLModelin kautta
- Perusvirheenkäsittely HTTPExceptioneilla
- Toteutettu riippuvuuksiin perustuva autentikointi (FastAPI Depends)
- Selkeä vastuunjako autentikoinnin, reitityksen ja tietokantakerroksen välillä

## 📁 Project Structure

```text
app/
├── main.py
├── routes/        # API-endpointit
├── models/        # Tietokantamallit
├── crud/          # Tietokanta operaatiot
├── database/      # DB-alustus
```

# Esimerkki endpoint

- GET /anturit/{anturi_id}/mittaus_tulokset?page=1&limit=10&start_time=2024-01-01T00:00:00&end_time=2024-01-02T00:00:00

## Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite

## Ohjelman ajo lokaalisti

```md
Option 1 (Suositeltu)
uvicorn app.main:app --reload

Option 2 (FastAPI CLI)
fastapi dev app/main.py
```
