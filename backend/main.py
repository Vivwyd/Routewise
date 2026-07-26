from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from routing import build_graph, apply_congestion_penalties, find_optimal_route
from schemas import OptimalRouteResponse

app = FastAPI(title="RouteWise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stations")
def get_stations(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, name, lat, lon FROM stations")).mappings().all()
    return list(result)


@app.get("/routes")
def get_routes(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, name FROM routes")).mappings().all()
    return list(result)


@app.get("/optimal-route", response_model=OptimalRouteResponse)
def optimal_route(
    start_station: int = Query(...),
    end_station: int = Query(...),
    at_time: datetime = Query(default_factory=datetime.now),
    db: Session = Depends(get_db)
):
    rows = db.execute(
        text("""
            SELECT rs.route_id, rs.station_id, rs.sequence_order,
                   s.lat, s.lon
            FROM route_stations rs
            JOIN stations s ON s.id = rs.station_id
        """)
    ).mappings().all()

    graph = build_graph([dict(r) for r in rows])
    predicted_load = apply_congestion_penalties(
        graph, hour=at_time.hour, day_of_week=at_time.weekday()
    )
    result = find_optimal_route(graph, start_station, end_station)

    return {
        **result,
        "predicted_load": predicted_load
    }
