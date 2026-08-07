const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Toggle this to false once your friend's FastAPI backend is running
const USE_MOCK_DATA = false;

type Station = { id: number; name: string; lat: number; lon: number };

const MOCK_STATIONS: Station[] = [
  { id: 1, name: "Central Station", lat: 25.789, lon: 55.981 },
  { id: 2, name: "North Terminal", lat: 25.805, lon: 55.975 },
  { id: 3, name: "East Junction", lat: 25.792, lon: 56.001 },
  { id: 4, name: "South Plaza", lat: 25.771, lon: 55.978 },
  { id: 5, name: "West End", lat: 25.783, lon: 55.955 },
];

const MOCK_ROUTE_RESULT = {
  path: [1, 2, 3],
  total_weighted_cost: 4.5,
  predicted_load: {
    1: 62.3,
    2: 28.1,
    3: 15.4,
    4: 40.2,
    5: 55.7,
  },
  error: null,
};

export async function fetchStations() {
  if (USE_MOCK_DATA) {
    // TODO: remove mock once backend is live
    return new Promise<Station[]>((resolve) =>
      setTimeout(() => resolve(MOCK_STATIONS), 300)
    );
  }

  const res = await fetch(`${API_BASE}/stations`);
  if (!res.ok) throw new Error("Failed to fetch stations");
  return res.json();
}

export async function fetchOptimalRoute(
  startId: number,
  endId: number,
  atTime?: string
) {
  if (USE_MOCK_DATA) {
    // TODO: remove mock once backend is live
    return new Promise((resolve) =>
      setTimeout(() => resolve(MOCK_ROUTE_RESULT), 500)
    );
  }

  const params = new URLSearchParams({
    start_station: String(startId),
    end_station: String(endId),
    ...(atTime ? { at_time: atTime } : {}),
  });
  const res = await fetch(`${API_BASE}/optimal-route?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch optimal route");
  return res.json();
}