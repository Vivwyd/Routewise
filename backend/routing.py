import networkx as nx
from ml.predict import predict_load

CROWD_PENALTY_THRESHOLD = 50
PENALTY_MULTIPLIER = 3.0


def build_graph(route_stations: list[dict]) -> nx.Graph:
    """
    route_stations: list of dicts like
      {"route_id": 1, "station_id": 3, "sequence_order": 2, "lat":.., "lon":..}
    Builds an undirected graph connecting consecutive stations on each route.
    """
    G = nx.Graph()

    routes = {}
    for rs in route_stations:
        routes.setdefault(rs["route_id"], []).append(rs)

    for route_id, stops in routes.items():
        stops.sort(key=lambda s: s["sequence_order"])
        for i in range(len(stops) - 1):
            a, b = stops[i]["station_id"], stops[i + 1]["station_id"]
            G.add_edge(a, b, weight=1.0)

    return G


def apply_congestion_penalties(G: nx.Graph, hour: int, day_of_week: int):
    """
    Mutates edge weights: any edge touching a predicted-overcrowded
    station gets a heavier weight, discouraging Dijkstra from routing through it.
    """
    predictions = {}
    for node in G.nodes:
        load = predict_load(node, hour, day_of_week)
        predictions[node] = round(load, 1)

        if load > CROWD_PENALTY_THRESHOLD:
            for neighbor in G.neighbors(node):
                G[node][neighbor]["weight"] *= PENALTY_MULTIPLIER

    return predictions


def find_optimal_route(G: nx.Graph, start: int, end: int) -> dict:
    """Runs Dijkstra on the (already congestion-weighted) graph."""
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        cost = nx.dijkstra_path_length(G, start, end, weight="weight")
        return {"path": path, "total_weighted_cost": round(cost, 2)}
    except nx.NetworkXNoPath:
        return {"path": [], "total_weighted_cost": None, "error": "No path found"}
