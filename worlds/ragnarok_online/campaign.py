def configuration(world):
    worlds = world.multiworld.get_game_worlds(world.game)
    modes = {player.options.campaign.current_key for player in worlds}
    if len(modes) != 1:
        raise ValueError("Server Campaign must match for every Ragnarok Online player")
    return {
        "version": 1,
        "mode": modes.pop(),
        "members": len(worlds),
        "surveys_per_member": min(
            12, 7 * min(player.options.job_pool_size.value for player in worlds)
        ),
        "jobs_per_member": min(
            2, min(player.options.job_pool_size.value for player in worlds)
        ),
    }
