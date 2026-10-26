from . import data, dungeons


def slot_topology(slot):
    memberships = {
        name: [city for city, maps in slot["cities"].items() if name in maps]
        for name in slot["map_locations"]
    }
    nodes = [
        {
            "map": name,
            "cities_any": memberships[name],
            "permit": dungeons.PERMIT_FOR_MAP.get(name)
            if slot["dungeon_gating"]
            else None,
            "location": slot["map_locations"][name],
        }
        for name in slot["map_locations"]
    ]
    edges = [
        {"source": "Menu", "destination": "Jobs", "kind": "logical"},
        *[
            {
                "source": "Menu",
                "destination": city,
                "kind": "hub_travel",
                "requires": f"Unlock: {city}",
            }
            for city in slot["cities"]
        ],
        *[
            {"source": city, "destination": name, "kind": "city_exploration"}
            for city, maps in slot["cities"].items()
            for name in maps
            if name != city
        ],
        *[
            {
                "source": data.PORTALS[source]["source"],
                "destination": data.PORTALS[target]["destination"],
                "kind": "shuffled_portal",
                "portal": source,
                "target_portal": target,
            }
            for source, target in slot["portal_links"].items()
        ],
    ]
    return {
        "version": 1,
        "world_version": "0.1.0",
        "graph_kind": "ap_logical_regions_not_physical_walking_routes",
        "runtime_reachability": False,
        "access_contract": {
            "destination": "any_city_membership_and_permit_if_gated",
            "unknown_destination": "deny",
            "map_compass": "information_only",
            "permit_free_guild_approaches": slot["guild_approach_maps"],
            "city_exploration": "logical_abstraction_not_a_direct_warp",
            "combat_and_inventory_requirements": "not_modelled_by_map_graph",
        },
        "maps": nodes,
        "logical_regions": ["Menu", "Jobs"],
        "edges": edges,
        "portal_catalog": slot["portal_catalog"],
        "portal_links": slot["portal_links"],
        "starting_state": {
            "city": slot["start_city"],
            "map": slot["start_map"],
            "job": "Novice",
            "first_guild_job": slot["start_job"],
            "precollected": [
                f"Unlock: {slot['start_city']}",
            ],
        },
        "options": slot["options"],
        "dungeons": slot["dungeons"],
        "map_locations": slot["map_locations"],
        "job_locations": slot["job_locations"],
        "content_checks": slot["content_checks"],
        "wandering_npc": slot["wandering_npc"],
        "combat_locations": [
            {
                "location": data.BOSS_LOCATION_ID,
                "map": slot["goal"]["boss"]["map"],
                "mob_id": slot["goal"]["boss"]["mob_id"],
            },
        ],
        "goal": slot["goal"],
    }
