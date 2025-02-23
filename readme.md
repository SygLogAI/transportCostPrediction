# Microservice API Dokumentáció

# Bevezetés
A közzétett kód lehetővé teszi a tonna/kilométer alapú fuvardíjak előrejelzését, elkapva az éven belüli szezonalitást és távolságok közötti nem lineáris kapcsolatot. Például a mezőgazdasági termékek szállításhoz kapcsolódó aratási időszakban lévő emelkedő keresletet és rövidebb viszonylatokhoz tartozó magasabb kilométer árat.

A tréninget a lehető legtöbb  adattal érdemes végezni, az év lehető legtöbb hetére legyen adat, valamint minél több eltérő távolságú viszonylat legyen a tesztadatokban.

Az előrejelzett fuvardíjak felhasználhatóak logisztikai gráfok alkotására, és a legideálisabb szállítási időpontok és viszonylatok modellezésére.

A dokumentáció bemutatja a telepítés folyamatát, és hogyan lehet elérni a microservice API-ját, milyen végpontok állnak rendelkezésre, valamint a kérések és válaszok formátumát.

# Előfeltételek
- python3
- redis

# Telepítés

### Függőségek
```bash
cd project-root/server
pip install -r requirements.txt
```

### Indítás
#### App
```bash
cd project-root/server/app
DATA_DIR=../store BROKER_URL=redis://localhost:6379/0 uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
#### Celery
```bash
cd project-root/server/app
BROKER_URL=redis://localhost:6379/0 celery -A celery_app.worker worker -l info
```

# API leírás

## Alapinformációk
- **Base URL:** `localhost:8000/`
- **Hitelesítés:** Jelenleg hitelesítés nélkül elérhető
- **Válasz formátum:** JSON vagy String, a végpontok leírásában jelölve

## Végpontok

### 1. Fuvardíj előrejelzés
**Endpoint:** `POST /api/models/transport_cost/predict`  


#### Kérés:
```http
POST /api/models/transport_cost/predict HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: -

{
    "model_id": "661ff1eb-5ce8-4af5-8be6-0d3709be622c",
    "distances": [ 70, 70, 70, 70, 70, 40, 40, 40, 40, 40 ],
    "time_periods": [ 9, 10, 11, 12, 13, 9, 10, 11, 12, 13 ]
}
```

#### Válasz:
```json
{
   "costs": [
    103.0232558139535,
    102.79452054794521,
    102.65342960288808,
    102.55665310865776,
    102.4857142857143,
    107.91666666666667,
    108.14666666666666,
    108.28855721393036,
    108.38709677419352,
    108.46036585365852
  ]

}
```

### 2. Tréning
**Endpoint:** `POST /api/models/transport_cost/fit`



#### Kérés:
```http
POST /api/models/transport_cost/fit HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: -

{
    "distances": [ 
      70, 70, 70, 70, 70, 70, 70, 70,
      70, 70, 70, 70, 70, 70, 40, 40,
      40, 40, 40, 40, 40, 40, 40, 40,
      40, 40, 40, 40 
    ],
    "time_periods": [
      46, 47, 48, 49, 50, 51, 52,  1,
      2,  3,  4,  5,  6,  7, 46, 47,
      48, 49, 50, 51, 52,  1,  2,  3,
      4,  5,  6,  7
    ],
    "costs": [
      100, 110, 120, 100, 103, 111,
      105, 100, 110, 120, 100, 103,
      111, 105, 100, 110, 120, 100,
      103, 111, 105, 100, 110, 120,
      100, 103, 111, 105
    ]
,
}
```

#### Válasz:
```json
{
  "model_id:": "f4596d71-8105-4bfd-9851-538b0676017f"
}
```

### 3. Státusz
**Endpoint:** `GET /api/models/transport_cost/status`


#### Kérés:
```http
GET /api/models/transport_cost/status?model_id=989cd53d-160e-4bf8-a304-def2cdcfd2a5 HTTP/1.1
Host: localhost:8000
Authorization: -
```

#### Válasz:
```
"in_progress"
```

## Hibakódok

| Kód  | Leírás |
|-------|-----------|
| 400   | Hibás kérés |
| 404   | Nem található |
| 422   | Feldolgozhatatlan entitás |
| 500   | Szerverhiba |



