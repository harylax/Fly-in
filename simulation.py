from map_model import Map


map = Map('maps/easy/01_linear_path.txt')
for drone in map.drones:
    drone.zone = map.hubs[0]

map.start_hub.current_drones = map.drones

turn: int = 0
while True:
    if len(map.end_hub.current_drones) == map.nb_drones:
        break

    for i in range(1, len(map.hubs)):
        if not map.hubs[i].current_drones:
            j = i
            while j > 0 and map.hubs[j - 1].current_drones:
                drone = map.hubs[j - 1].current_drones.pop(0)
                map.hubs[j].current_drones.append(drone)
                drone.zone = map.hubs[j]
                j -= 1

    print(map.drones)
    turn += 1
