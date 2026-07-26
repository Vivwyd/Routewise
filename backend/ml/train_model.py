import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

def generate_mock_data(n_samples=5000, n_stations=5, seed=42):
    rng = np.random.default_rng(seed)

    station_id = rng.integers(1, n_stations + 1, n_samples)
    hour = rng.integers(0, 24, n_samples)
    day_of_week = rng.integers(0, 7, n_samples)

    base_load = rng.normal(20, 5, n_samples)

    rush_hour_mask = ((hour >= 7) & (hour <= 9)) | ((hour >= 17) & (hour <= 19))
    base_load += rush_hour_mask * rng.uniform(30, 60, n_samples)

    weekend_mask = day_of_week >= 5
    base_load *= np.where(weekend_mask, 0.5, 1.0)

    base_load += np.where(station_id == 1, 15, 0)

    passenger_count = np.clip(base_load, 0, None).astype(int)

    return pd.DataFrame({
        "station_id": station_id,
        "hour": hour,
        "day_of_week": day_of_week,
        "passenger_count": passenger_count
    })


def train_and_save_model(output_path="ml/passenger_model.pkl"):
    df = generate_mock_data()

    X = df[["station_id", "hour", "day_of_week"]]
    y = df["passenger_count"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Model trained. Test MAE: {mae:.2f} passengers")

    joblib.dump(model, output_path)
    print(f"Model saved to {output_path}")

    return model


if __name__ == "__main__":
    train_and_save_model()
