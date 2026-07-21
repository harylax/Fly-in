from map_model import Map


map = Map('maps/easy/01_linear_path.txt')
for drone in map.drones:
    drone.zone = map.start_hub
    map.start_hub.current_drones.append(drone)

turn: int = 0

while True:
    if len(map.end_hub.current_drones) == map.nb_drones:
        break

    for i in range(len(map.hubs) - 1, 0, -1):
        current_hub = map.hubs[i - 1]
        next_hub = map.hubs[i]
        if current_hub.current_drones:
            drone = current_hub.current_drones.pop(0)
            next_hub.current_drones.append(drone)
            drone.zone = next_hub

    output: str = ''

    for drone in map.drones:
        if drone.zone:
            output += f"D{drone.id}-{drone.zone.name} "

    turn += 1

    print(f"turn {turn}: {output}")
