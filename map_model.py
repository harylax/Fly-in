from enum import Enum
import sys
try:
    from pydantic import BaseModel, Field  # type: ignore
except ImportError as err:
    print(f"Import Error: {err}")
    print("Please, install pydantic before any run.")
    print(
        "Usage:\npython3 -m venv venv"
        "\nsource venv/bin/activate"
        "\npython3 -m pip install pydantic"
        )
    sys.exit(1)
from parse_map import parsed_map, parse_to_dict
from typing import Any


class Zone(Enum):
    normal = "normal"
    blocked = "blocked"
    restricted = "restricted"
    priority = "priority"
    start = "start"
    end = "end"


class Color(Enum):
    green = "green"
    blue = "blue"
    yellow = "yellow"
    orange = "orange"
    red = "red"
    purple = "purple"
    cyan = "cyan"
    none = "none"
    brown = "brown"
    lime = "lime"
    magenta = "magenta"
    gold = "gold"


class Hub(BaseModel):
    name: str = Field(..., min_length=2)
    x: int = Field(...)
    y: int = Field(...)
    zone: Zone = Field(default=Zone.normal)
    color: Color = Field(default=Color.none)
    max_drones: int = Field(default=1)
    current_drones: list[Any] = []


class Connection(BaseModel):
    name: str = Field(..., min_length=2)
    origin: Hub | None = Field(default=None)
    destination: Hub | None = Field(default=None)
    max_link_capacity: int = Field(default=1)


class Drone:
    def __init__(self, id: int = 0) -> None:
        self.id: int = id
        self.zone: Hub | Connection | None = None


class Map:
    def __init__(self, map_file: str) -> None:
        map = parsed_map(parse_to_dict(map_file))

        try:
            self.nb_drones: int = int(map['nb_drones'])
        except ValueError as err:
            print(err)
            sys.exit(1)

        self.hubs: list[Hub] = [
            Hub(
                name=hub[0],
                x=hub[1],
                y=hub[2],
                zone=hub[3].get('zone', Zone.normal),
                color=hub[3].get('color', Color.none),
                max_drones=hub[3].get('max_drones', 1)
            ) for hub in map['hubs']
        ]

        self.start_hub: Hub = self.hubs[0]
        self.end_hub: Hub = self.hubs[-1]

        # METTRE DANS UN VALIDATE AVEC D'AUTRE POSSIBLES ERR
        if self.end_hub.max_drones < self.nb_drones:
            print(
                "Error in the map file:\n"
                f"the end hub '{self.end_hub.name}' "
                "cannot have all the drone.\n"
                f"Max drone: {self.end_hub.max_drones}, "
                f"drones: {self.nb_drones}"
                )
            sys.exit(1)

        self.connections: list[Connection] = [
            Connection(
                name=link[0],
                origin=self.get_hub(self.hubs, link[1]),
                destination=self.get_hub(self.hubs, link[2]),
                max_link_capacity=link[3].get('max_link_capacity', 1)
            ) for link in map['connections']
        ]

        self.drones: list[Drone] = [
            Drone(i) for i in range(1, self.nb_drones + 1)
        ]

    def get_hub(self, hubs: list[Hub], name: str) -> Hub | None:
        for hub in hubs:
            if hub.name == name:
                return hub
        return None

    def __str__(self) -> str:
        hubs: str = ''
        for i, hub in enumerate(self.hubs[1:-1], start=1):
            hubs += f"hub {i}: {hub}\n"

        connections: str = ''
        for i, link in enumerate(self.connections, start=1):
            connections += f"connection {i}: {link}\n"

        drones: str = ''
        for drone in self.drones:
            drones += f"drone D{drone.id}-{drone.zone}\n"

        return (
            f"nb_drones: {self.nb_drones}\n\n"
            f"start_hub: {self.hubs[0]}\n\n"
            f"{hubs}\n"
            f"end_hub: {self.hubs[-1]}\n\n"
            f"{connections}\n"
            f"{drones}"
        )


if __name__ == "__main__":
    map_file = 'maps/hard/03_ultimate_challenge.txt'

    map = Map(map_file)
    print(map)
