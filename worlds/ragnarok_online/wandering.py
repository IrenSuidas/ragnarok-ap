import json
from importlib.resources import files


NAME = "Seek the Wandering AP NPC"
LOCATION_ID = 3000
CANDIDATES = json.loads(files(__package__).joinpath("wandering_data.json").read_text())


def select(world):
    placement = world.random.choice(
        [
            candidate
            for candidate in CANDIDATES
            if any(city in world.cities for city in candidate["cities"])
        ]
    )
    return {
        **{key: placement[key] for key in ("map", "x", "y", "npc_name")},
        "city": next(city for city in placement["cities"] if city in world.cities),
        "kind": "seek",
        "name": NAME,
        "location": LOCATION_ID,
    }
