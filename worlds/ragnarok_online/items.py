from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import data, dungeons, goals, skills

if TYPE_CHECKING:
    from .world import RagnarokWorld

FILLER_ITEMS = ["Zeny Pouch"]
TRAP_ITEMS = ["Trap: Ambush", "Trap: Warp"]

ITEM_NAME_TO_ID = {
    f"Unlock: {city}": index + 1 for index, city in enumerate(data.CITIES)
}
ITEM_NAME_TO_ID["Zeny Pouch"] = 100
ITEM_NAME_TO_ID["Ticket: Poring Village"] = 300
ITEM_NAME_TO_ID.update({name: index + 101 for index, name in enumerate(TRAP_ITEMS)})
ITEM_NAME_TO_ID.update(dungeons.item_ids())
ITEM_NAME_TO_ID.update(
    {name: grant["item_id"] for name, grant in skills.SKILL_ITEMS.items()}
)

DEFAULT_ITEM_CLASSIFICATIONS = {
    name: ItemClassification.progression
    for name in ITEM_NAME_TO_ID
    if name.startswith(("Unlock: ", "Permit: "))
}
DEFAULT_ITEM_CLASSIFICATIONS["Zeny Pouch"] = ItemClassification.filler
DEFAULT_ITEM_CLASSIFICATIONS["Ticket: Poring Village"] = ItemClassification.useful
DEFAULT_ITEM_CLASSIFICATIONS.update(
    {
        name: ItemClassification.useful
        for name in (*skills.SKILL_ITEMS, *dungeons.MAPS, *dungeons.COMPASSES)
    }
)
DEFAULT_ITEM_CLASSIFICATIONS.update(
    {name: ItemClassification.trap for name in TRAP_ITEMS}
)
DEFAULT_ITEM_CLASSIFICATIONS.update(
    {
        name: ItemClassification.progression
        for name in (
            "Final Boss Defeated",
            *(goals.certification(job) for job in data.JOBS),
        )
    }
)


class RagnarokItem(Item):
    game = "Ragnarok Online"


def create_item_with_correct_classification(
    world: RagnarokWorld, name: str
) -> RagnarokItem:
    return RagnarokItem(
        name,
        DEFAULT_ITEM_CLASSIFICATIONS[name],
        ITEM_NAME_TO_ID.get(name),
        world.player,
    )


def get_random_filler_item_name(world: RagnarokWorld) -> str:
    if world.random.randrange(100) < world.options.trap_chance.value:
        return world.random.choice(TRAP_ITEMS)
    return FILLER_ITEMS[world.random.randint(0, len(FILLER_ITEMS) - 1)]


def create_all_items(world: RagnarokWorld) -> None:
    itempool: list[Item] = [
        world.create_item(f"Unlock: {city}")
        for city in world.cities
        if city != world.start_city
    ]
    if world.dungeon_gating:
        itempool.extend(
            world.create_item(dungeons.permit_name(dungeon))
            for dungeon in world.dungeons
        )
    available = len(world.multiworld.get_unfilled_locations(world.player))
    if len(itempool) > available:
        raise ValueError("Not enough locations for city and dungeon progression")
    optional = list(world.skill_catalog["items"])
    if world.dungeon_gating:
        optional.extend(
            name
            for dungeon in world.dungeons
            for name in (dungeons.map_name(dungeon), dungeons.compass_name(dungeon))
        )
    optional.extend(
        "Ticket: Poring Village" for _ in range(max(1, len(world.cities) // 2))
    )
    if len(optional) > available - len(itempool):
        optional = world.random.sample(optional, available - len(itempool))
    itempool.extend(world.create_item(name) for name in optional)
    while len(itempool) < available:
        itempool.append(world.create_item(world.get_filler_item_name()))
    world.multiworld.itempool += itempool
