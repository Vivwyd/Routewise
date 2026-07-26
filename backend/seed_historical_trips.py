"""
Generates realistic-looking historical_trips rows and inserts them into Supabase.
Separate from ml/train_model.py's mock data — this populates the actual DB table
for demo/dashboard purposes and as a stand-in for "real" ridership data.

Run: python seed_historical_trips.py
"""
import os
from datetime import datetime, timedelta
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("SUPABASE_DB_URL"))

N_TRIPS = 3000
N_STATIONS = 5
N_ROUTES = 2
DAYS_BACK = 30


def generate_trips(seed=7):
    rng = np.random.default_rng(seed)
    rows = []

    for _ in range(N_TRIPS):
        days_ago = rng.integers(0, DAYS_BACK)
        hour = rng.integers(0, 24)
        minute = rng.integers(0, 60)
        timestamp = datetime.now() - timedelta(days=int(days_ago))
        timestamp = timestamp.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)

        station_id = int(rng.integers(1, N_STATIONS + 1))
        route_id = int(rng.integers(1, N_ROUTES + 1))

        base = rng.normal(20, 5)
        is_rush = (7 <= hour <= 9) or (17 <= hour <= 19)
        if is_rush:
            base += rng.uniform(30, 60)
        if timestamp.weekday() >= 5:
            base *= 0.5
        if station_id == 1:
            base += 15

        passenger_count = max(0, int(base))

        rows.append({
            "trip_timestamp": timestamp,
            "route_id": route_id,
            "station_id": station_id,
            "passenger_count": passenger_count
        })

    return rows

def insert_trips(rows):
    values_clause = ", ".join(
        f"('{r['trip_timestamp']}', {r['route_id']}, {r['station_id']}, {r['passenger_count']})"
        for r in rows
    )
    query = f"""
        INSERT INTO historical_trips (trip_timestamp, route_id, station_id, passenger_count)
        VALUES {values_clause}
    """
    with engine.begin() as conn:
        conn.execute(text(query))
    print(f"Inserted {len(rows)} historical_trips rows.")


if __name__ == "__main__":
    trips = generate_trips()
    insert_trips(trips)
