# Anturi API

REST API lämpötila-anturidatan keräämiseen ja hallintaan. Toteutettu kurssin päättötyönä.

## Status

Ydinominaisuudet toteutettu

## Ydinominaisuudet

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

## Testit
Tämä projekti sisältää kattavan automaattisen testikannan, toteutettu pytestillä ja FastAPI:n TestClientillä.

Testien kattavuus

#### Anturit

- Anturin luonti (onnistunut ja virhetilanne: viittaus olemattomaan lohkoon)
- Anturien haku ja suodatus (id:llä, tilalla)
- Anturin päivitys, mukaan lukien tilamuutosten automaattinen kirjautuminen
  - Tilan muuttuessa luodaan tilamuutosmerkintä
  - Saman tilan asettaminen uudelleen ei luo turhaa merkintää
- Anturin tilamuutoshistorian haku ja suodatus tilan mukaan

#### Mittaukset

- Mittaustulosten haku anturikohtaisesti, mukaan lukien:
  - Aikajärjestys (uusin ensin)
  - Aikavälisuodatus (start_time/end_time) ja virheellisen aikavälin validointi
  - Paginointi (page & limit) ja rajojen validointi (page < 1, limit < 1, limit > 100)
  - Virhetilassa olevan anturin mittauksia ei palauteta (409)
- Mittauksen poisto (onnistunut poisto ja 404 olemattomalle mittaukselle)

#### Lohkot

- Lohkon luonti
- Lohkoon kuuluvien anturien haku, mukaan lukien:
  - Tyhjä lista kun lohkolla ei ole antureita
  - Anturi ilman mittauksia (viimeisin_arvo/aikaleima = null)
  - Viimeisimmän mittauksen näyttäminen useamman mittauksen joukosta
  - Useamman anturin listaus samasta lohkosta
  - 404 olemattomalle lohkolle



Aja testit lokaalisti:

```bash
python -m pytest -v
```
 
## Vaatimusten täyttyminen

Projektissa on toteutettu kaikki annetut backend-vaatimukset:

#### Hallinta:

- Antureiden lisääminen järjestelmään
- Anturin tilan muuttaminen
- Anturin lohkon muuttaminen
- Yksittäisen mittatuloksen poistaminen

#### Datan haku:

- Kaikkien antureiden listaus (tunniste, lohko ja tila)
- Lohkokohtainen anturien listaus (sisältäen viimeisimmän mittauksen)
- Yksittäisen anturin kaikki tiedot (sisältäen mittaukset)
- Mittausten rajaaminen aikavälille (start_time, end_time)
- Oletuksena rajattu määrä tuloksia (paginointi)

#### Lisäksi:

- Anturien suodatus tilan mukaan
- Anturin tilamuutosten seuranta
- Virhetilassa olevan anturin mittaustuloksia ei palauteta

## Backend ja Arkkitehtuuri

Modulaarinen projektirakenne (crud, database, models, routes) PostgreSQL-integraatio SQLModelin kautta, ajetaan Dockerissa (kehityksessä myös SQLite-tuki DATABASE_URL-ympäristömuuttujan kautta)


#### API noudattaa REST-periaatteita ja käyttää HTTP-metodeja seuraavasti:

* GET: datan haku
* POST: uusien resurssien luonti
* PUT: olemassa olevien resurssien päivittäminen
* DELETE: resurssien poistaminen


#### Virhetilanteita käsitellään HTTPExceptioneilla. API palauttaa selkeät HTTP-statuskoodit, kuten:
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

## Ajaminen Dockerilla (PostgreSQL)

Projekti tukee myös konttipohjaista ajoa Docker Composella, jolloin sovellus käyttää SQLiten sijaan PostgreSQL-tietokantaa

#### Käynnistä kontit

````bash
docker compose up -d --build
````
Tämä käynnistää kaksi konttia:
  - anturi-api - FastAPI-sovellus portissa 8000
  - anturi_db - PostgreSQL 16-tietokanta

#### Tarkista tila

````bash
docker compose ps
docker compose logs api
````

#### Avaa API-dokumentaatio
http://localhost:8000/docs

## Ajaminen AWS-Pilvessä

Sovellus on deployattu AWS:ään: ECR (image) → ECS/Fargate (kontti) → RDS PostgreSQL (tietokanta) → ALB (julkinen endpoint).

#### Live-endpoint
````bash
http://anturi-api-alb-1717429430.eu-north-1.elb.amazonaws.com/docs
````
#### Rakenna & Julkaise 
````bash
   docker build -t anturi-api .
   docker tag anturi-api:latest <account-id>.dkr.ecr.eu-north-1.amazonaws.com/anturi-api:latest
   docker push <account-id>.dkr.ecr.eu-north-1.amazonaws.com/anturi-api:latest
````

## 📁 Projektin rakenne

```text
app/
├── main.py
├── routes/        # API-endpointit
├── models/        # Tietokantamallit
├── crud/          # Tietokanta operaatiot
├── database/      # DB-alustus
├── tests/         # Testit
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
- PostgreSQL(tuotanto)
- SQLite(Paikallinen kehitys)
- Pytest
- Docker
- AWS(ECS/Fargate, RDS, ALB)
