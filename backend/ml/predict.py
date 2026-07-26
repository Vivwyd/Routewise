import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "passenger_model.pkl"
_model = None

def get_model():
    """Lazy-load the model once, reuse across requests."""
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_load(station_id: int, hour: int, day_of_week: int) -> float:
    """Predict passenger count for a given station/time."""
    model = get_model()
    X = pd.DataFrame([{
        "station_id": station_id,
        "hour": hour,
        "day_of_week": day_of_week
    }])
    return float(model.predict(X)[0])
