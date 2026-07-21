from map_model import Map


class Simulation:
    def __init__(self, map: Map):
        self.map: Map = map
        self.drones_moves: list[list[tuple[int, str]]] = []
        self.init_drones_pos()

    def snapshot(self) -> list[tuple[int, str]]:
        res: list[tuple[int, str]] = []
        for drone in self.map.drones:
            if drone.zone:
                res.append((drone.id, drone.zone.name))
        return res

    def init_drones_pos(self) -> None:
        for drone in self.map.drones:
            drone.zone = self.map.start_hub
            self.map.start_hub.current_drones.append(drone)
        self.drones_moves.append(self.snapshot())

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

            self.drones_moves.append(self.snapshot())


if __name__ == "__main__":

    map = Map('maps/easy/01_linear_path.txt')
    simulation = Simulation(map)
    simulation.linear_solve()

    result: list[str] = []
    for i, moves in enumerate(simulation.drones_moves):
        line = ''
        for drone_id, hub_name in moves:
            line += f"D{drone_id}-{hub_name} "
        result.append(f"turn {i}: {line}")

    for res in result:
        print(res)
