from pydantic import BaseModel
from typing import List, Optional

class StationOut(BaseModel):
    id: int
    name: str
    lat: float
    lon: float

class RouteOut(BaseModel):
    id: int
    name: str

class OptimalRouteResponse(BaseModel):
    path: List[int]
    total_weighted_cost: Optional[float]
    predicted_load: dict
    error: Optional[str] = None
