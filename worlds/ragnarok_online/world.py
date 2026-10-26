from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import (
    campaign,
    data,
    dungeons,
    equipment,
    goals,
    items,
    locations,
    levels,
    regions,
    room_topology,
    rules,
    skills,
    sharing,
    topology,
    web_world,
    wandering,
)
from . import options as ragnarok_options


class RagnarokWorld(World):
    game = "Ragnarok Online"
    web = web_world.RagnarokWebWorld()
    options_dataclass = ragnarok_options.RagnarokOptions
    options: ragnarok_options.RagnarokOptions
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    origin_region_name = "Menu"

    def generate_early(self) -> None:
        selected_cities = room_topology.selected_cities(self)
        self.cities = {
            city: maps for city, maps in data.CITIES.items() if city in selected_cities
        }
        self.maps = sorted({name for maps in self.cities.values() for name in maps})
        self.jobs = tuple(data.CITY_JOBS[city] for city in self.cities)
        self.job_ids = {
            "Swordman": 1,
            "Mage": 2,
            "Archer": 3,
            "Acolyte": 4,
            "Merchant": 5,
            "Thief": 6,
        }
        self.skill_catalog = skills.slot_catalog(
            {self.job_ids[job] for job in self.jobs}
        )
        self.dungeons = [
            dungeon
            for dungeon in dungeons.DUNGEON_DATA
            if set(dungeon["maps"]) & set(self.maps)
        ]
        self.unlock_sharing = sharing.configuration(self)
        self.campaign = campaign.configuration(self)
        self.content_checks = []
        for check in data.CONTENT_CHECKS:
            if check["city"] not in self.cities:
                continue
            kind = check["kind"]
            if kind == "kill":
                if self.options.notable_checks:
                    self.content_checks.append(dict(check))
                continue
            option = {"kill_set": "kill_checks", "gather_set": "gather_checks"}[kind]
            if getattr(self.options, option):
                self.content_checks.append(dict(check))
        self.start_city = self.random.choice(list(self.cities))
        self.start_job = data.CITY_JOBS[self.start_city]
        self.dungeon_gating = bool(self.options.dungeon_gating)
        self.slot_item_names = {
            "Zeny Pouch",
            "Ticket: Poring Village",
            *items.TRAP_ITEMS,
            *self.skill_catalog["items"],
            *(f"Unlock: {city}" for city in self.cities),
        }
        if self.dungeon_gating:
            self.slot_item_names.update(
                name
                for dungeon in self.dungeons
                for name in (
                    dungeons.permit_name(dungeon),
                    dungeons.map_name(dungeon),
                    dungeons.compass_name(dungeon),
                )
            )
        self.multiworld.push_precollected(
            self.create_item(f"Unlock: {self.start_city}")
        )
        self.portal_links = room_topology.portal_links(self)
        self.boss = goals.select_boss(self)
        self.wandering_npc = wandering.select(self)
        self.equipment_check = equipment.select(self)

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def has_unlock(self, state, name, kind):
        return sharing.has(self, state, name, kind)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.RagnarokItem:
        return items.create_item_with_correct_classification(self, name)

    def collect(self, state, item):
        changed = super().collect(state, item)
        if changed:
            sharing.invalidate(self, state, item)
        return changed

    def remove(self, state, item):
        changed = super().remove(state, item)
        if changed:
            sharing.invalidate(self, state, item, removing=True)
        return changed

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        difficulty = self.options.difficulty.current_key
        slot = {
            "schema_version": 6,
            "campaign": self.campaign,
            "unlock_sharing": self.unlock_sharing,
            "skill_progression": self.skill_catalog,
            "content_checks": self.content_checks,
            "level_checks": list(levels.CHECKS)
            if self.options.base_level_checks
            else [],
            "wandering_npc": self.wandering_npc,
            "equipment_check": self.equipment_check,
            "options": {
                name: (
                    option.current_key
                    if isinstance(option, ragnarok_options.Choice)
                    and not isinstance(option, ragnarok_options.DefaultOnToggle)
                    else option.value
                )
                for name in ragnarok_options.RagnarokOptions.__annotations__
                for option in (getattr(self.options, name),)
            },
            "start_city": self.start_city,
            "start_map": self.start_city,
            "start_job": self.start_job,
            "cities": self.cities,
            "dungeon_gating": self.dungeon_gating,
            "dungeons": self.dungeons,
            "seed": self.multiworld.seed,
            "difficulty": difficulty,
            **data.DIFFICULTIES[difficulty],
            "autoloot": bool(self.options.autoloot),
            "randomize_maps": bool(self.options.randomize_maps),
            "chaos_warp_portals": bool(self.options.chaos_warp_portals),
            "death_link": bool(self.options.death_link),
            "portal_catalog": {
                name: portal
                for name, portal in data.PORTALS.items()
                if portal["city"] in self.cities
            },
            "portal_links": self.portal_links,
            "map_edges": [
                [data.PORTALS[source]["source"], data.PORTALS[target]["destination"]]
                for source, target in self.portal_links.items()
            ],
            "goal": {
                "type": self.options.goal.current_key,
                "jobs": sorted(self.jobs),
                "boss": self.boss,
                "boss_location_id": data.BOSS_LOCATION_ID,
            },
            "trap_chance": self.options.trap_chance.value,
            "map_locations": {
                name: locations.LOCATION_NAME_TO_ID[f"Reach {name}"]
                for name in self.maps
            },
            "job_locations": {
                name: locations.LOCATION_NAME_TO_ID[f"Job: {name}"]
                for name in self.jobs
            },
            "job_tokens": {job: data.JOBS[job] for job in self.jobs},
            "novice_token": data.NOVICE_TOKEN,
            "novice_baseline": {
                "base_level": 10,
                "job_level": 10,
                "unlock_job_level": 10,
            },
            "job_guilds": {job: data.JOB_GUILDS[job] for job in self.jobs},
            "guild_approach_maps": sorted(
                dungeons.GUILD_APPROACH_MAPS & set(self.maps)
            ),
            "items": {
                str(code): name
                for name, code in items.ITEM_NAME_TO_ID.items()
                if name in self.slot_item_names
            },
        }
        slot["topology"] = topology.slot_topology(slot)
        return slot
