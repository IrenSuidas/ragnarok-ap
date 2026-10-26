from __future__ import annotations

from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule

from . import data, dungeons, equipment, goals

if TYPE_CHECKING:
    from .world import RagnarokWorld


def set_all_rules(world: RagnarokWorld) -> None:
    set_rule(
        world.get_location(equipment.NAME),
        lambda state: (
            world.has_unlock(state, f"Unlock: {world.start_city}", "cities")
            and state.has(goals.certification(world.start_job), world.player)
        ),
    )
    city_checks = {f"Reach {city}" for city in world.cities} | {
        f"Job: {job}" for job in world.jobs
    }
    for location in world.multiworld.get_locations(world.player):
        if location.name not in city_checks:
            location.item_rule = lambda item: (
                not (item.game == world.game and item.name.startswith("Unlock: "))
            )
    for check in [*world.content_checks, world.wandering_npc]:
        permit = dungeons.PERMIT_FOR_MAP.get(check["map"])
        set_rule(
            world.get_location(check["name"]),
            lambda state, city=check["city"], permit=permit, maps=check.get("maps", []): (
                world.has_unlock(state, f"Unlock: {city}", "cities")
                and all(state.can_reach_region(name, world.player) for name in maps)
                and (
                    not world.dungeon_gating
                    or permit is None
                    or world.has_unlock(state, permit, "dungeon_permits")
                )
            ),
        )
    if world.dungeon_gating:
        for permit, map_ids in dungeons.PERMIT_MAPS.items():
            for map_id in map_ids:
                if map_id not in world.maps:
                    continue
                if map_id in dungeons.GUILD_APPROACH_MAPS:
                    continue
                set_rule(
                    world.get_location(f"Reach {map_id}"),
                    lambda state, permit=permit: world.has_unlock(
                        state, permit, "dungeon_permits"
                    ),
                )
    permit = dungeons.PERMIT_FOR_MAP.get(world.boss["map"])
    set_rule(
        world.get_location(data.BOSS_LOCATION),
        lambda state: (
            goals.all_jobs(world, state)
            and (
                not world.dungeon_gating
                or permit is None
                or world.has_unlock(state, permit, "dungeon_permits")
            )
        ),
    )
    for event, check in (
        *((goals.certification(job), f"Job: {job}") for job in world.jobs),
        ("Final Boss Defeated", data.BOSS_LOCATION),
    ):
        set_rule(
            world.get_location(event),
            lambda state, check=check: state.can_reach_location(check, world.player),
        )
    if world.options.goal.current_key == "complete_jobs":
        world.multiworld.completion_condition[world.player] = lambda state: (
            goals.all_jobs(world, state)
        )
    else:
        world.multiworld.completion_condition[world.player] = lambda state: state.has(
            "Final Boss Defeated", world.player
        )
