from map_model import Map, Drone

# map = Map('maps/easy/01_linear_path.txt')
# for drone in map.drones:
#     drone.zone = map.start_hub
#     map.start_hub.current_drones.append(drone)

# turn: int = 0

# while True:
#     if len(map.end_hub.current_drones) == map.nb_drones:
#         break

#     for i in range(len(map.hubs) - 1, 0, -1):
#         current_hub = map.hubs[i - 1]
#         next_hub = map.hubs[i]
#         if current_hub.current_drones:
#             drone = current_hub.current_drones.pop(0)
#             next_hub.current_drones.append(drone)
#             drone.zone = next_hub

#     output: str = ''

#     for drone in map.drones:
#         if drone.zone:
#             output += f"D{drone.id}-{drone.zone.name} "

#     turn += 1

#     print(f"turn {turn}: {output}")


class Simulation:
    def __init__(self, map: Map):
        self.map: Map = map
        self.drones_moves: list[list[Drone]] = []
        self.init_drones_pos()

    def init_drones_pos(self) -> None:
        for drone in self.map.drones:
            drone.zone = self.map.start_hub
            self.map.start_hub.current_drones.append(drone)
        self.drones_moves.append(self.map.drones[:])

    def linear_solve(self) -> None:
        turn: int = 0

        while len(self.map.end_hub.current_drones) != self.map.nb_drones:
            for i in range(len(self.map.hubs) - 1, 0, -1):
                current_hub = self.map.hubs[i - 1]
                next_hub = self.map.hubs[i]
                if current_hub.current_drones:
                    drone = current_hub.current_drones.pop(0)
                    next_hub.current_drones.append(drone)
                    drone.zone = next_hub

            turn += 1

            self.drones_moves.append(self.map.drones[:])


if __name__ == "__main__":

    map = Map('maps/easy/01_linear_path.txt')
    simulation = Simulation(map)
    simulation.linear_solve()

    result: list[str] = []
    for i, moves in enumerate(simulation.drones_moves):
        line = ''
        for drone in moves:
            if drone.zone:
                line += f"D{drone.id}-{drone.zone.name} "
        result.append(f"turn {i}: {line}")

    for res in result:
        print(res)
