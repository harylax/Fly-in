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
                                restricted: Drone = hub.current_drones.pop(0)
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

    def sorted_links_by_restriction(
            self,
            links: list[Connection]
            ) -> list[Connection]:
        return sorted(
            links, key=lambda link: (
                link.destination.zone == Zone.restricted
                if link.destination else False
            )
        )

    def sorted_links_by_priority(
            self,
            links: list[Connection]
            ) -> list[Connection]:
        return sorted(
            links, key=lambda link: (
                link.destination.zone == Zone.priority
                if link.destination else False
            ),
            reverse=True
        )

    def circular_solve(self) -> None:
        turn: int = 0

        links: list[Connection] = \
            self.sorted_links_by_restriction(self.map.connections)

        while len(self.map.end_hub.current_drones) != self.map.nb_drones:

            for h in self.map.hubs:
                if h.zone == Zone.restricted:
                    for d in h.current_drones:
                        if d.restricted:
                            d.restricted = False
                        else:
                            d.restricted = True

            moved_this_turn: set[int] = set()

            for hub in reversed(self.map.hubs):
                if hub == self.map.end_hub:
                    continue
                if not hub.current_drones:
                    continue

                for link in links:
                    if link.origin == hub and link.destination:

                        if self.is_dead_end(link.destination):
                            continue

                        next_hub: Hub = link.destination

                        next_hub_capacity: int = \
                            next_hub.max_drones - len(next_hub.current_drones)

                        nb_to_move: int = min(
                            link.max_link_capacity, next_hub_capacity
                            )

                        i: int = 0

                        while nb_to_move and i < len(hub.current_drones):
                            if not hub.current_drones:
                                break

                            drone: Drone = hub.current_drones[i]

                            if drone.id in moved_this_turn:
                                i += 1
                                continue

                            if drone.restricted:
                                i += 1
                                continue

                            hub.current_drones.pop(i)
                            next_hub.current_drones.append(drone)
                            drone.zone = next_hub
                            moved_this_turn.add(drone.id)
                            nb_to_move -= 1

            turn += 1

            self.drones_moves.append(self.snapshot())

    def priority_solve(self) -> None:
        turn: int = 0

        links: list[Connection] = \
            self.sorted_links_by_priority(self.map.connections)

        links = self.sorted_links_by_restriction(links)

        while len(self.map.end_hub.current_drones) != self.map.nb_drones:

            for h in self.map.hubs:
                if h.zone == Zone.restricted:
                    for d in h.current_drones:
                        if d.restricted:
                            d.restricted = False
                        else:
                            d.restricted = True

            moved_this_turn: set[int] = set()

            for hub in reversed(self.map.hubs):
                if hub == self.map.end_hub:
                    continue
                if not hub.current_drones:
                    continue

                for link in links:
                    if link.origin == hub and link.destination:

                        if self.is_dead_end(link.destination):
                            continue

                        next_hub: Hub = link.destination

                        next_hub_capacity: int = \
                            next_hub.max_drones - len(next_hub.current_drones)

                        nb_to_move: int = min(
                            link.max_link_capacity, next_hub_capacity
                            )

                        i: int = 0

                        while nb_to_move and i < len(hub.current_drones):
                            if not hub.current_drones:
                                break

                            drone: Drone = hub.current_drones[i]

                            if drone.id in moved_this_turn:
                                i += 1
                                continue

                            if drone.restricted:
                                i += 1
                                continue

                            hub.current_drones.pop(i)
                            next_hub.current_drones.append(drone)
                            drone.zone = next_hub
                            moved_this_turn.add(drone.id)
                            nb_to_move -= 1

            turn += 1

            self.drones_moves.append(self.snapshot())

    def is_path(self) -> bool:

        def recursive(hub: Hub) -> bool:
            if hub == self.map.start_hub:
                return True

            for link in self.map.connections:
                if link.destination == hub:
                    if link.origin:
                        previous_hub: Hub = link.origin
                        if self.is_dead_end(previous_hub):
                            continue
                        if recursive(previous_hub):
                            return True
            return False

        return recursive(self.map.end_hub)


if __name__ == "__main__":

    # map = Map('maps/easy/01_linear_path.txt')
    # map = Map('maps/easy/02_simple_fork.txt')
    # map = Map('maps/easy/03_basic_capacity.txt')
    # map = Map('maps/medium/01_dead_end_trap.txt')
    # map = Map('maps/medium/02_circular_loop.txt')
    # map = Map('maps/medium/03_priority_puzzle.txt')
    map = Map('maps/test.txt')

    simulation = Simulation(map)

    # print("Not sorted")
    # for link in simulation.map.connections:
    #     print(link.name)

    # links = simulation.sorted_links_by_priority(simulation.map.connections)

    # print("\nFirst sort (priority):")
    # for lnk in links:
    #     print(lnk.name)

    # links = simulation.sorted_links_by_restriction(links)

    # print("\nSecond sort (restriction):")
    # for lk in links:
    #     print(lk.name)
    # exit()

    if not simulation.is_path():
        print("No path found, program ended.")
        exit(0)

    # simulation.linear_solve()
    # simulation.simple_fork_solve()
    # simulation.dead_end_solve()
    # simulation.restricted_solve()
    simulation.circular_solve()

    result: list[str] = []
    for i, moves in enumerate(simulation.drones_moves):
        line = ''
        for drone_id, hub_name in moves:
            line += f"D{drone_id}-{hub_name} "
        result.append(f"turn {i}: {line}")

    for res in result:
        print(res)
