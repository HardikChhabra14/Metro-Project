def calculate_fare(source, destination):
    station_count = abs(destination.order - source.order)
    base_fare = 10
    per_station_fare = 5
    return base_fare + (station_count * per_station_fare)