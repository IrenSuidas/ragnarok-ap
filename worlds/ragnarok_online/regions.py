from BaseClasses import Region

from . import data


def create_and_connect_regions(world) -> None:
    names = [
        "Menu",
        "Jobs",
        *world.cities,
        *[name for name in world.maps if name not in world.cities],
    ]
    world.multiworld.regions += [
        Region(name, world.player, world.multiworld) for name in names
    ]
    world.get_region("Menu").connect(world.get_region("Jobs"))
    for city, maps in world.cities.items():
        world.get_region("Menu").connect(
            world.get_region(city),
            f"Travel to {city}",
            lambda state, city=city: world.has_unlock(
                state, f"Unlock: {city}", "cities"
            ),
        )
        for name in maps:
            if name != city:
                world.get_region(city).connect(
                    world.get_region(name), f"Explore {city}: {name}"
                )
    for source, target in world.portal_links.items():
        destination = data.PORTALS[target]["destination"]
        world.get_region(data.PORTALS[source]["source"]).connect(
            world.get_region(destination),
            f"Portal {source}",
            lambda state, destination=destination: any(
                world.has_unlock(state, f"Unlock: {city}", "cities")
                for city, maps in world.cities.items()
                if destination in maps
            ),
        )
