from map_model import Map, Hub, Connection, Drone, Zone, Color


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
                current_hub: Hub = self.map.hubs[i - 1]
                next_hub: Hub = self.map.hubs[i]
                if current_hub.current_drones:
                    drone = current_hub.current_drones.pop(0)
                    next_hub.current_drones.append(drone)
                    drone.zone = next_hub

            turn += 1

            self.drones_moves.append(self.snapshot())

    def simple_fork_solve(self) -> None:
        turn: int = 0

        while len(self.map.end_hub.current_drones) != self.map.nb_drones:
            for hub in reversed(self.map.hubs):
                if hub == self.map.end_hub:
                    continue
                if not hub.current_drones:
                    continue

                for link in self.map.connections:
                    if link.origin == hub and link.destination:
                        next_hub: Hub = link.destination

                        next_hub_capacity: int = \
                            next_hub.max_drones - len(next_hub.current_drones)

                        nb_to_move: int = min(
                            link.max_link_capacity, next_hub_capacity
                            )

                        for _ in range(nb_to_move):
                            if not hub.current_drones:
                                break
                            drone: Drone = hub.current_drones.pop(0)
                            next_hub.current_drones.append(drone)
                            drone.zone = next_hub

            turn += 1

            self.drones_moves.append(self.snapshot())

    def is_dead_end(self, hub: Hub) -> bool:
        if hub == self.map.end_hub or hub.name == 'goal':
            return False
        return hub.zone == Zone.blocked or hub.color == Color.red

    def dead_end_solve(self) -> None:
        turn: int = 0

        while len(self.map.end_hub.current_drones) != self.map.nb_drones:
            for hub in reversed(self.map.hubs):
                if hub == self.map.end_hub:
                    continue
                if not hub.current_drones:
                    continue

                for link in self.map.connections:
                    if link.origin == hub and link.destination:

                        if self.is_dead_end(link.destination):
                            continue

                        next_hub: Hub = link.destination

                        next_hub_capacity: int = \
                            next_hub.max_drones - len(next_hub.current_drones)

                        nb_to_move: int = min(
                            link.max_link_capacity, next_hub_capacity
                            )

                        for _ in range(nb_to_move):
                            if not hub.current_drones:
                                break
                            drone: Drone = hub.current_drones.pop(0)
                            next_hub.current_drones.append(drone)
                            drone.zone = next_hub

            turn += 1

            self.drones_moves.append(self.snapshot())

    def restricted_solve(self) -> None:
        turn: int = 0

        while len(self.map.end_hub.current_drones) != self.map.nb_drones:
            for hub in reversed(self.map.hubs):
                if hub == self.map.end_hub:
                    continue
                if not hub.current_drones:
                    continue

                if hub.zone == Zone.restricted:
                    for d in hub.current_drones:
                        if d.restricted:
                            d.restricted = False
                        else:
                            d.restricted = True

                for link in self.map.connections:
                    if link.origin == hub and link.destination:

                        if self.is_dead_end(link.destination):
                            continue

                        next_hub: Hub = link.destination

                        next_hub_capacity: int = \
                            next_hub.max_drones - len(next_hub.current_drones)

                        nb_to_move: int = min(
                            link.max_link_capacity, next_hub_capacity
                            )

                        n_drones: int = len(hub.current_drones)
                        while nb_to_move:
                            if not hub.current_drones:
                                break

                            if not n_drones:
                                break

                            if hub.current_drones[0].restricted:
                                restricted = hub.current_drones.pop(0)
                                hub.current_drones.append(restricted)
                                n_drones -= 1

                            else:
                                drone: Drone = hub.current_drones.pop(0)
                                next_hub.current_drones.append(drone)
                                drone.zone = next_hub

                                n_drones -= 1
                                nb_to_move -= 1

            turn += 1

            self.drones_moves.append(self.snapshot())


if __name__ == "__main__":

    # map = Map('maps/easy/01_linear_path.txt')
    # map = Map('maps/easy/02_simple_fork.txt')
    # map = Map('maps/easy/03_basic_capacity.txt')
    map = Map('maps/medium/01_dead_end_trap.txt')
    # map = Map('maps/medium/02_circular_loop.txt')

    simulation = Simulation(map)

    # simulation.linear_solve()
    # simulation.simple_fork_solve()
    # simulation.dead_end_solve()
    simulation.restricted_solve()

    result: list[str] = []
    for i, moves in enumerate(simulation.drones_moves):
        line = ''
        for drone_id, hub_name in moves:
            line += f"D{drone_id}-{hub_name} "
        result.append(f"turn {i}: {line}")

    for res in result:
        print(res)
