from enum import Enum
import os
import sys
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


class Hub:
    def __init__(self) -> None:
        self.name: str | None = None
        self.x: int | None = None
        self.y: int | None = None
        self.zone: Zone = Zone.normal
        self.color: Color | None = None
        self.max_drones: int = 1
        self.current_drones: int = 0


class Connection:
    def __init__(self) -> None:
        self.name: str | None = None
        self.origin: Hub | None = None
        self.destination: Hub | None = None
        self.max_capacity: int | None = None
        self.current_drones: int | None = None


def parse_to_dict(map_file: str) -> dict[str, Any]:
    if not os.path.isfile(map_file):
        print(f"{map_file} not found. Program exited.", file=sys.stderr)
        sys.exit(1)
    raw: str | None = None

    try:
        with open(map_file) as f:
            raw = f.read()
    except OSError as err:
        print(f"Map error: {err}", file=sys.stderr)

    if not raw:
        print("Map error: empty file.", file=sys.stderr)
        sys.exit(1)

    if raw:
        content: list[str] = raw.splitlines()

    if not content:
        print("Map error: empty file.", file=sys.stderr)
        sys.exit(1)

    start_hub: str = ''
    end_hub: str = ''
    hub: list[str] = []
    connection: list[str] = []

    for line in content:
        if not line or line.startswith('#'):
            continue

        parts = line.split(':', 1)
        if parts[0].strip() == 'start_hub':
            start_hub += parts[1].strip()
        elif parts[0].strip() == 'end_hub':
            end_hub += parts[1].strip()
        elif parts[0].strip() == 'hub':
            hub.append(parts[1].strip())
        elif parts[0].strip() == 'connection':
            connection.append(parts[1].strip())
        else:
            continue

    return {
        'start_hub': start_hub,
        'hub': hub,
        'connection': connection,
        'end_hub': end_hub
    }


    def get_hub_data(map: dict[str, Any]) -> list[tuple[str, int, int, dict[str, Any]]]:
        res: list[tuple[str, int, int, dict[str, Any]]] = []
        data = map['start_hub'].split('[')
        


if __name__ == "__main__":
    map = 'maps/hard/03_ultimate_challenge.txt'

    print(parse_to_dict(map))
