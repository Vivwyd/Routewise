-- =========================================
-- SCHEMA
-- =========================================
CREATE TABLE IF NOT EXISTS stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS route_stations (
    id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    station_id INTEGER NOT NULL REFERENCES stations(id) ON DELETE CASCADE,
    sequence_order INTEGER NOT NULL,
    UNIQUE (route_id, sequence_order)
);

CREATE TABLE IF NOT EXISTS historical_trips (
    id SERIAL PRIMARY KEY,
    trip_timestamp TIMESTAMP NOT NULL,
    route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    station_id INTEGER NOT NULL REFERENCES stations(id) ON DELETE CASCADE,
    passenger_count INTEGER NOT NULL CHECK (passenger_count >= 0)
);

CREATE INDEX IF NOT EXISTS idx_route_stations_route_id ON route_stations(route_id);
CREATE INDEX IF NOT EXISTS idx_historical_trips_station_time ON historical_trips(station_id, trip_timestamp);

-- =========================================
-- SEED DATA
-- =========================================
INSERT INTO stations (name, lat, lon) VALUES
('Central', 40.7580, -73.9855),
('Uptown', 40.7831, -73.9712),
('Downtown', 40.7128, -74.0060),
('Eastside', 40.7489, -73.9680),
('Westgate', 40.7549, -74.0000);

INSERT INTO routes (name) VALUES
('Red Line'),
('Blue Line');

-- Red Line: Central -> Uptown -> Eastside
INSERT INTO route_stations (route_id, station_id, sequence_order) VALUES
(1, 1, 1), (1, 2, 2), (1, 4, 3);

-- Blue Line: Downtown -> Central -> Westgate
INSERT INTO route_stations (route_id, station_id, sequence_order) VALUES
(2, 3, 1), (2, 1, 2), (2, 5, 3);
