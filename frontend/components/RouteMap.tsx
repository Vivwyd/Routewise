"use client";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

type Station = { id: number; name: string; lat: number; lon: number };

function getColorForLoad(load: number): string {
  if (load > 50) return "#dc2626"; // red - crowded
  if (load > 30) return "#f59e0b"; // amber - moderate
  return "#16a34a"; // green - light load
}

export default function RouteMap({
  stations,
  routeResult,
}: {
  stations: Station[];
  routeResult: any;
}) {
  const center: [number, number] = stations.length
    ? [stations[0].lat, stations[0].lon]
    : [0, 0];

  const pathStations = routeResult?.path
    ?.map((id: number) => stations.find((s) => s.id === id))
    .filter(Boolean);

  return (
    <MapContainer
      center={center}
      zoom={13}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />

      {stations.map((s) => (
        <Marker key={s.id} position={[s.lat, s.lon]}>
          <Popup>
            {s.name}
            {routeResult?.predicted_load?.[s.id] !== undefined && (
              <div>Predicted load: {routeResult.predicted_load[s.id]}</div>
            )}
          </Popup>
        </Marker>
      ))}

      {pathStations?.slice(0, -1).map((s: Station, i: number) => {
        const next = pathStations[i + 1];
        const loadA = routeResult.predicted_load[s.id] ?? 0;
        const loadB = routeResult.predicted_load[next.id] ?? 0;
        const avgLoad = (loadA + loadB) / 2;

        return (
          <Polyline
            key={`${s.id}-${next.id}`}
            positions={[
              [s.lat, s.lon],
              [next.lat, next.lon],
            ]}
            pathOptions={{ color: getColorForLoad(avgLoad), weight: 5 }}
          />
        );
      })}
    </MapContainer>
  );
}