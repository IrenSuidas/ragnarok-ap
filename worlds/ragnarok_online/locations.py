from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import data, equipment, goals, levels, wandering

if TYPE_CHECKING:
    from .world import RagnarokWorld

MAP_LOCATIONS = [f"Reach {map_id}" for map_id in data.MAPS]

LOCATION_NAME_TO_ID = {name: index + 1000 for index, name in enumerate(MAP_LOCATIONS)}
LOCATION_NAME_TO_ID.update(
    {f"Job: {name}": index + 2000 for index, name in enumerate(data.JOBS)}
)
LOCATION_NAME_TO_ID[data.BOSS_LOCATION] = data.BOSS_LOCATION_ID
LOCATION_NAME_TO_ID[wandering.NAME] = wandering.LOCATION_ID
LOCATION_NAME_TO_ID[equipment.NAME] = equipment.LOCATION_ID
LOCATION_NAME_TO_ID.update(
    {check["name"]: check["location"] for check in levels.CHECKS}
)
LOCATION_NAME_TO_ID.update(
    {check["name"]: check["location"] for check in data.CONTENT_CHECKS}
)


class RagnarokLocation(Location):
    game = "Ragnarok Online"


def create_all_locations(world: RagnarokWorld) -> None:
    if world.options.base_level_checks:
        world.get_region("Menu").add_locations(
            {check["name"]: check["location"] for check in levels.CHECKS},
            RagnarokLocation,
        )
    world.get_region(world.equipment_check["map"]).add_locations(
        {equipment.NAME: equipment.LOCATION_ID}, RagnarokLocation
    )
    world.get_region(world.wandering_npc["map"]).add_locations(
        {wandering.NAME: wandering.LOCATION_ID}, RagnarokLocation
    )
    for check in world.content_checks:
        world.get_region(check["map"]).add_locations(
            {check["name"]: check["location"]}, RagnarokLocation
        )
    for map_id in world.maps:
        location_name = f"Reach {map_id}"
        region = world.get_region(map_id)
        region.add_locations(
            {location_name: LOCATION_NAME_TO_ID[location_name]}, RagnarokLocation
        )
    world.get_region(world.boss["map"]).add_locations(
        {data.BOSS_LOCATION: data.BOSS_LOCATION_ID}, RagnarokLocation
    )
    for name in world.jobs:
        guild = data.JOB_GUILDS[name]
        world.get_region(guild).add_locations(
            {f"Job: {name}": LOCATION_NAME_TO_ID[f"Job: {name}"]}, RagnarokLocation
        )
    for name, region in (
        *(
            (goals.certification(job), world.get_region(data.JOB_GUILDS[job]))
            for job in world.jobs
        ),
        ("Final Boss Defeated", world.get_region(world.boss["map"])),
    ):
        event = RagnarokLocation(world.player, name, None, region)
        region.locations.append(event)
        event.place_locked_item(world.create_item(name))
