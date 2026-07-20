from enum import Enum
import sys
try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError as err:
    print(f"Import Error: {err}")
    print("Please, install pydantic before any run.")
    print("Usage:\nsource venv/bin/activate\npython3 -m pip install pydantic")
    sys.exit(1)
from parse_map import parsed_map, parse_to_dict


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
    current_drones: int = Field(default=0)


class Connection(BaseModel):
    name: str = Field(..., min_length=2)
    origin: Hub | None = Field(default=None)
    destination: Hub | None = Field(default=None)
    max_link_capacity: int = Field(default=1)


class Map:
    def __init__(self, map_file: str) -> None:
        map = parsed_map(parse_to_dict(map_file))
        self.nb_drones: int = map['nb_drones']
        self.start_hub: Hub = Hub(
            name=map['start_hub'][0],
            x=map['start_hub'][1],
            y=map['start_hub'][2],
            zone=map['start_hub'][3].get('zone', Zone.normal),
            color=map['start_hub'][3].get('color', Color.none),
            max_drones=map['start_hub'][3].get('max_drones', 1)
        )
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
        self.end_hub: Hub = Hub(
            name=map['end_hub'][0],
            x=map['end_hub'][1],
            y=map['end_hub'][2],
            zone=map['end_hub'][3].get('zone', Zone.normal),
            color=map['end_hub'][3].get('color'),
            max_drones=map['end_hub'][3].get('max_drones', 1)
        )
        self.connections: list[Connection] = [
            Connection(
                name=link[0],
                origin=self.get_hub(self.hubs, link[1]),
                destination=self.get_hub(self.hubs, link[2]),
                max_link_capacity=link[3].get('max_link_capacity', 1)
            ) for link in map['connections']
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

        return (
            f"nb_drones: {self.nb_drones}\n\n"
            f"start_hub: {self.start_hub}\n\n"
            f"{hubs}\n"
            f"end_hub: {self.end_hub}\n\n"
            f"{connections}"
        )


if __name__ == "__main__":
    map_file = 'maps/hard/03_ultimate_challenge.txt'

    map = Map(map_file)
    print(map)
