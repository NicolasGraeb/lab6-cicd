# Zadanie 5 - Tryb produkcyjny (uruchomienie)

Poniżej znajdują się krótkie instrukcje uruchomienia aplikacji FastAPI (ML) w trybie produkcyjnym:

- lokalnie
- w Dockera
- przez Docker Compose (z PostgreSQL)

## Wymagania / zasoby

Aplikacja to `FastAPI` + model `scikit-learn`. Do zapisu predykcji potrzebuje `PostgreSQL`.

Domyślnie API jest dostępne na porcie `8080`.

## Zmienne środowiskowe

### Aplikacja (`ml-app`)

- `DATABASE_URL` (opcjonalne)
  - przykład: `postgresql://mluser:mlpassword@postgres:5432/ml_db`
  - jeśli `DATABASE_URL` nie jest ustawione, aplikacja działa, ale nie zapisuje i nie zwraca rekordów z tabeli `predictions`.

### Baza danych (`postgres` - Docker Compose)

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Uruchomienie lokalnie

1. Zainstaluj zależności:
   ```powershell
   pip install -r requirements.txt
   ```
2. Ustaw zmienną środowiskową (jeśli chcesz zapisywać predykcje do Postgres):
   ```powershell
   $env:DATABASE_URL="postgresql://mluser:mlpassword@localhost:5432/ml_db"
   ```
3. Uruchom serwer produkcyjnie:
   ```powershell
   uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
   ```

Test endpointów:
- `GET  http://localhost:8080/health`
- `POST http://localhost:8080/predict`
- `GET  http://localhost:8080/predictions`

## Uruchomienie za pomocą Dockera

### Bez bazy (tylko ML, bez zapisu predykcji)

```powershell
docker build -t ml-api .
docker run --rm -p 8080:8080 ml-api
```

### Z bazą PostgreSQL (wymaga osobnego Postgresa)

1. Uruchom Postgres (np. na hostcie):
   ```powershell
   docker run --rm -d -p 5432:5432 `
     -e POSTGRES_USER=mluser `
     -e POSTGRES_PASSWORD=mlpassword `
     -e POSTGRES_DB=ml_db `
     postgres:16-alpine
   ```
2. Uruchom aplikację i przekaż `DATABASE_URL`:
   ```powershell
   docker run --rm -p 8080:8080 `
     -e DATABASE_URL="postgresql://mluser:mlpassword@host.docker.internal:5432/ml_db" `
     ml-api
   ```

## Uruchomienie za pomocą Docker Compose

Compose uruchamia 2 serwisy w jednej sieci:

- `ml-app` (aplikacja ML)
- `postgres` (baza do zapisu predykcji)

1. Start:
   ```powershell
   docker compose up -d --build
   ```
2. Sprawdzenie:
   - `GET http://localhost:8080/health`
3. Test zapisu:
   - `POST http://localhost:8080/predict`
   - `GET  http://localhost:8080/predictions`

