NAME = "Adventurer's Essentials"
LOCATION_ID = 3001
SLOTS = [9, 7, 3, 2]


def select(world):
    return {
        "name": NAME,
        "location": LOCATION_ID,
        "kind": "equip",
        "city": world.start_city,
        "map": world.start_city,
        "required_count": len(SLOTS),
        "slots": list(SLOTS),
        "criterion": "each_slot_worn_at_least_once_per_character",
    }
