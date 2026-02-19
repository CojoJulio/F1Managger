from models.race_car import RaceCar


def update_positions_and_gaps(cars, track_length):

    # Orden correcto
    cars.sort(key=lambda c: (-c.state.lap, -c.state.lapProgress))

    for i, car in enumerate(cars):
        car.state.position = i + 1

    if not cars:
        return

    leader = cars[0]

    for car in cars:
        lap_diff = leader.state.lap - car.state.lap
        progress_diff = leader.state.lapProgress - car.state.lapProgress

        distance_gap = (lap_diff * track_length) + (progress_diff * track_length)

        # convertir distancia a tiempo usando velocidad actual
        if car.state.speed > 0:
            car.state.gap_to_leader = distance_gap / car.state.speed
        else:
            car.state.gap_to_leader = 0
