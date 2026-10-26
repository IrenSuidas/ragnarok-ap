from random import Random
from math import factorial, prod

from . import data


def selected_cities(world):
    random = Random(
        f"ragnarok-online:job-pool:v1:{world.multiworld.seed}:{world.player}"
    )
    return set(random.sample(list(data.CITIES), world.options.job_pool_size.value))


def portal_links(world):
    worlds = world.multiworld.get_game_worlds(world.game)
    settings = {bool(player.options.randomize_maps) for player in worlds}
    if len(settings) != 1:
        raise ValueError(
            "Randomize Maps must match for every Ragnarok Online player in the room"
        )
    randomize = settings.pop()
    chaos_settings = {bool(player.options.chaos_warp_portals) for player in worlds}
    if len(chaos_settings) != 1:
        raise ValueError(
            "Chaos Warp Portals must match for every Ragnarok Online player in the room"
        )
    if chaos_settings.pop():
        if not randomize:
            raise ValueError("Chaos Warp Portals requires Randomize Maps")
        used = {}
        for player in sorted(worlds, key=lambda player: player.player):
            random = Random(
                f"ragnarok-online:slot-portals:v1:{world.multiworld.seed}:{player.player}"
            )
            while True:
                cities = selected_cities(player)
                links = {
                    source: target
                    for source, target in shuffled_links(random, True).items()
                    if data.PORTALS[source]["city"] in cities
                }
                catalog = tuple(sorted(links))
                signatures = used.setdefault(catalog, set())
                signature = tuple(links.items())
                if signature not in signatures or len(signatures) == topology_count(
                    cities
                ):
                    signatures.add(signature)
                    break
            if player.player == world.player:
                return links
    random = Random(f"ragnarok-online:room-portals:v1:{world.multiworld.seed}")
    return {
        source: target
        for source, target in shuffled_links(random, randomize).items()
        if data.PORTALS[source]["city"] in world.cities
    }


def shuffled_links(random, randomize):
    links = {}
    for city in data.CITIES:
        sources = [
            name
            for name, portal in data.PORTALS.items()
            if portal["city"] == city and portal["outbound"]
        ]
        targets = list(sources)
        if randomize:
            if len(sources) < 2:
                raise ValueError(f"City has no nontrivial portal shuffle: {city}")
            while targets == sources:
                random.shuffle(targets)
        for source, target in zip(sources, targets):
            links[source] = target
            links[data.PORTALS[target]["reverse"]] = data.PORTALS[source]["reverse"]
    return links


def topology_count(cities):
    return prod(
        factorial(
            sum(p["city"] == city and p["outbound"] for p in data.PORTALS.values())
        )
        - 1
        for city in cities
    )
