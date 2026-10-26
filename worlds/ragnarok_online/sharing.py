OPTION_NAMES = {
    "cities": "city_unlock_sharing",
    "jobs": "job_unlock_sharing",
    "skills": "skill_unlock_sharing",
    "dungeon_permits": "dungeon_permit_sharing",
}


def configuration(world):
    worlds = world.multiworld.get_game_worlds(world.game)
    result = {}
    for kind, name in OPTION_NAMES.items():
        values = {getattr(player.options, name).current_key for player in worlds}
        if len(values) != 1:
            raise ValueError(f"{name} must match for every Ragnarok Online player")
        result[kind] = values.pop()
    return result


def recipients(world, kind):
    if world.unlock_sharing[kind] == "per_person":
        return (world.player,)
    return tuple(
        player.player for player in world.multiworld.get_game_worlds(world.game)
    )


def count(world, state, name, kind):
    return sum(state.count(name, player) for player in recipients(world, kind))


def has(world, state, name, kind):
    return any(state.has(name, player) for player in recipients(world, kind))


def invalidate(world, state, item, removing=False):
    selected = getattr(world, "unlock_sharing", None)
    if selected is None:
        return
    kind = next(
        (
            kind
            for prefix, kind in (
                ("Unlock: ", "cities"),
                ("Permit: ", "dungeon_permits"),
            )
            if item.name.startswith(prefix)
        ),
        None,
    )
    if kind is None or selected[kind] != "server_wide":
        return
    for player in recipients(world, kind):
        state.stale[player] = True
        if removing:
            state.reachable_regions[player].clear()
            state.blocked_connections[player].clear()
