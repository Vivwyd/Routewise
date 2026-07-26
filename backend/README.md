# RouteWise Backend

FastAPI backend for RouteWise — a transit routing MVP that combines a graph-based
pathfinding engine (NetworkX/Dijkstra) with an ML congestion predictor
(scikit-learn RandomForest) to suggest the least-crowded route between two stations.

## Stack

- **FastAPI** — HTTP API layer
- **SQLAlchemy** — DB access
- **Supabase (Postgres)** — data storage
- **NetworkX** — graph building + Dijkstra shortest path
- **scikit-learn** — RandomForestRegressor for predicted passenger load per station/time

## Project structure
backend/
├── main.py # FastAPI app + endpoints
├── database.py # SQLAlchemy engine/session setup
├── routing.py # graph building, congestion penalties, Dijkstra
├── schemas.py # Pydantic response models
├── ml/
│ ├── train_model.py # trains RandomForest on mock data, saves .pkl
│ ├── predict.py # loads model, exposes predict_load()
│ └── passenger_model.pkl
├── requirements.txt
└── .env # not committed — see below
## Setup

```bash
cd backend
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash): venv/Scripts/activate
                                # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in `backend/` (never commit this):
SUPABASE_DB_URL=postgresql://postgres.xxxx:[PASSWORD]@aws-x-region.pooler.supabase.com:6543/postgres
Ask a teammate for the password, or use your own Supabase project's connection string
(Project Settings → Database → Connect → Transaction pooler → URI).

### Database schema

Run `seed.sql` (in the repo root or `backend/`, see file) in the Supabase SQL Editor
to create tables and seed sample stations/routes.

### Train the ML model

The trained model (`ml/passenger_model.pkl`) is committed to the repo, so this step
is optional unless you want to retrain:

```bash
python ml/train_model.py
```

This trains on synthetic data with realistic rush-hour spikes and saves the model.

### Run the API

```bash
uvicorn main:app --reload
```

API available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## Endpoints

### `GET /stations`
Returns all stations.

**Response:**
```json
[
  { "id": 1, "name": "Central", "lat": 40.758, "lon": -73.9855 },
  ...
]
```

### `GET /routes`
Returns all routes.

**Response:**
```json
[
  { "id": 1, "name": "Red Line" },
  { "id": 2, "name": "Blue Line" }
]
```

### `GET /optimal-route`
Returns the least-congested path between two stations at a given time.

**Query params:**
| Param | Type | Required | Description |
|---|---|---|---|
| `start_station` | int | yes | station ID to start from |
| `end_station` | int | yes | station ID to end at |
| `at_time` | ISO datetime | no | defaults to current time |

**Example:**
GET /optimal-route?start_station=3&end_station=4
**Response:**
```json
{
  "path": [3, 1, 2, 4],
  "total_weighted_cost": 27.0,
  "predicted_load": { "1": 82.3, "2": 66.6, "3": 65.9, "4": 65.7, "5": 63.4 },
  "error": null
}
```

`predicted_load` maps station ID → predicted passenger count at the given hour/day.
Routing avoids stations above a congestion threshold by penalizing their edges.

## Known limitations / future improvements

- `routing.py` uses hop-count as base edge weight rather than real geographic
  (haversine) distance between stations.
- The ML model trains on synthetic mock data, not real historical ridership.
  Designed to support retraining on real data (`historical_trips` table exists
  for this purpose) without changing the API contract.
- No authentication on endpoints — fine for an MVP demo, would need auth +
  rate limiting for production use.
