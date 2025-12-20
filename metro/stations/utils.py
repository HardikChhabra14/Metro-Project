from collections import deque
from .models import Station


def calculate_station_distance(source, destination):
    """
    Simple BFS to calculate shortest distance
    (number of stations) between two stations.
    """

    if source == destination:
        return 0

    visited = set()
    queue = deque([(source, 0)])

    while queue:
        current, distance = queue.popleft()
        if current == destination:
            return distance

        visited.add(current)

        neighbors = Station.objects.filter(metro_line=current.metro_line)
        for station in neighbors:
            if station not in visited:
                queue.append((station, distance + 1))

    return 0


def calculate_ticket_price(source, destination):
    base_fare = 10
    per_station_fare = 5

    distance = calculate_station_distance(source, destination)
    return base_fare + (distance * per_station_fare)
from collections import deque
from .models import Station

def shortest_path(source, destination):
    """
    Returns list of stations in shortest path
    """
    if source == destination:
        return [source]

    visited = set()
    queue = deque([[source]])

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == destination:
            return path

        if current in visited:
            continue

        visited.add(current)

        neighbors = Station.objects.filter(metro_line=current.metro_line)
        for station in neighbors:
            new_path = list(path)
            new_path.append(station)
            queue.append(new_path)

    return []