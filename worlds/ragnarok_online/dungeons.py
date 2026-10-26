import json
from importlib.resources import files

DUNGEON_DATA = json.loads(files(__package__).joinpath("dungeon_data.json").read_text())[
    "dungeons"
]


def permit_name(dungeon):
    return f"Permit: {dungeon['name']}"


def map_name(dungeon):
    return f"Map: {dungeon['name']}"


def compass_name(dungeon):
    return f"Compass: {dungeon['name']}"


def item_ids():
    ids = {}
    for dungeon in DUNGEON_DATA:
        ids[permit_name(dungeon)] = dungeon["permit_item"]
        ids[map_name(dungeon)] = dungeon["map_item"]
        ids[compass_name(dungeon)] = dungeon["compass_item"]
    return ids


GUILD_APPROACH_MAPS = {"moc_pryd01", "moc_prydb1"}
PERMIT_FOR_MAP = {
    map_name: permit_name(dungeon)
    for dungeon in DUNGEON_DATA
    for map_name in dungeon["maps"]
    if map_name not in GUILD_APPROACH_MAPS
}
PERMITS = [permit_name(dungeon) for dungeon in DUNGEON_DATA]
PERMIT_MAPS = {permit_name(dungeon): list(dungeon["maps"]) for dungeon in DUNGEON_DATA}
MAPS = [map_name(dungeon) for dungeon in DUNGEON_DATA]
COMPASSES = [compass_name(dungeon) for dungeon in DUNGEON_DATA]
