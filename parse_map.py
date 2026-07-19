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

    nb_drones: str = ''
    start_hub: str = ''
    end_hub: str = ''
    hub: list[str] = []
    connection: list[str] = []

    for line in content:
        if not line or line.startswith('#'):
            continue

        parts = line.split(':', 1)
        if parts[0].strip() == 'nb_drones':
            nb_drones += parts[1].strip()
        elif parts[0].strip() == 'start_hub':
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
        'nb_drones': nb_drones,
        'start_hub': start_hub,
        'hub': hub,
        'connection': connection,
        'end_hub': end_hub
    }


def parse_metadata(s: str) -> dict[str, str]:
    s = s.strip()
    s = s.strip('[]')
    raw: list[str] = s.split()

    res: dict[str, str] = {}

    for element in raw:
        key, _, value = element.partition('=')
        key = key.strip()
        value = value.strip()
        res[key] = value

    return res


def parse_hub_data(s: str) -> tuple[str, str, str, dict[str, str]]:
    raw = s.split(' ', 3)
    metadata: str = ''
    try:
        metadata += raw[3]
    except IndexError:
        pass

    return (
        raw[0].strip(),
        raw[1].strip(),
        raw[2].strip(),
        parse_metadata(metadata)
        )


def parse_connection_data(s: str) -> tuple[str, str, dict[str, str]]:
    raw = s.split(' ', 1)
    hub = raw[0].split('-', 1)
    metadata: str = ''
    try:
        metadata += raw[1]
    except IndexError:
        pass

    return (
        hub[0].strip(),
        hub[1].strip(),
        parse_metadata(metadata)
        )


def get_hub_data(map: dict[str, Any]) -> list[
    tuple[str, str, str, dict[str, str]]
        ]:
    res: list[tuple[str, str, str, dict[str, str]]] = []

    res.append(parse_hub_data(map['start_hub']))

    for line in map['hub']:
        res.append(parse_hub_data(line))

    res.append(parse_hub_data(map['end_hub']))

    return res


def get_connection_data(map: dict[str, list[str]]) -> list[
    tuple[str, str, dict[str, str]]
        ]:
    res: list[tuple[str, str, dict[str, str]]] = []

    for line in map['connection']:
        res.append(parse_connection_data(line))

    return res


if __name__ == "__main__":
    map_file = 'maps/hard/03_ultimate_challenge.txt'

    map = parse_to_dict(map_file)
    nb_drones = map['nb_drones']
    hubs = get_hub_data(map)
    connections = get_connection_data(map)

    print(f"nb_drones: {nb_drones}")
    print()

    for i, hub in enumerate(hubs, start=1):
        print(f"hub {i}: {hub}")
    print()

    for i, connection in enumerate(connections, start=1):
        print(f"connection {i}: {connection}")
