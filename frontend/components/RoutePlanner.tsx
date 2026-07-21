"use client";

import { useEffect, useState } from "react";
import { fetchStations, fetchOptimalRoute } from "@/lib/api";
import RouteMap from "./RouteMap";

type Station = { id: number; name: string; lat: number; lon: number };

export default function RoutePlanner() {
  const [stations, setStations] = useState<Station[]>([]);
  const [start, setStart] = useState<number | null>(null);
  const [end, setEnd] = useState<number | null>(null);
  const [routeResult, setRouteResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStations().then(setStations).catch(console.error);
  }, []);

  const handleFindRoute = async () => {
    if (!start || !end) return;
    setLoading(true);
    try {
      const result = await fetchOptimalRoute(start, end);
      setRouteResult(result);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4 p-6">
      <h1 className="text-2xl font-bold">RouteWise Dashboard</h1>

      <div className="flex gap-4">
        <select
          className="border rounded p-2"
          onChange={(e) => setStart(Number(e.target.value))}
        >
          <option value="">Start Station</option>
          {stations.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>

        <select
          className="border rounded p-2"
          onChange={(e) => setEnd(Number(e.target.value))}
        >
          <option value="">End Station</option>
          {stations.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>

        <button
          onClick={handleFindRoute}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={!start || !end || loading}
        >
          {loading ? "Calculating..." : "Find Route"}
        </button>
      </div>

      <RouteMap stations={stations} routeResult={routeResult} />
    </div>
  );
}