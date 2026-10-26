BOSSES = (
    {"name": "King Dramoh", "city": "izlude", "map": "iz_dun05", "mob_id": 2198},
    {"name": "Moonlight Flower", "city": "payon", "map": "pay_dun04", "mob_id": 1150},
    {
        "name": "Golden Thief Bug",
        "city": "prontera",
        "map": "prt_sewb4",
        "mob_id": 1086,
    },
    {"name": "Osiris", "city": "morocc", "map": "moc_pryd04", "mob_id": 1038},
    {"name": "Doppelganger", "city": "geffen", "map": "gef_dun02", "mob_id": 1046},
    {"name": "Drake", "city": "alberta", "map": "treasure02", "mob_id": 1112},
)


def certification(job):
    return f"Certified: {job}"


def all_jobs(world, state):
    return state.has_all([certification(job) for job in world.jobs], world.player)


def select_boss(world):
    candidates = [
        boss
        for boss in BOSSES
        if boss["city"] in world.cities and boss["map"] in world.maps
    ]
    if not candidates:
        raise ValueError("The job pool has no reachable native boss candidate")
    return dict(world.random.choice(candidates))
