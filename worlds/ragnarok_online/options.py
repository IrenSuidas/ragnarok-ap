from dataclasses import dataclass

from Options import (
    Choice,
    DefaultOnToggle,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    Toggle,
)


class Difficulty(Choice):
    """How generous the run is. Higher tiers multiply base/job EXP and item drop rates.

    mid = x5 base/job EXP and x10 item drops.
    """

    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_mid = 2
    option_hard = 3
    default = option_mid


class Autoloot(DefaultOnToggle):
    """Automatically pick up items dropped by monsters."""

    display_name = "Auto Loot"


class RandomizeMaps(DefaultOnToggle):
    """Permute the paired hub exits within every selected city.

    Each city keeps its own complete paired-return permutation; a run's pool may
    select any one to all six cities. Other portals are unchanged. City
    entitlement and internal reachability are unchanged. This room-wide setting
    must match for every Ragnarok Online player.
    """

    display_name = "Randomize Maps"


class DungeonGating(DefaultOnToggle):
    """Gate every dungeon entrance behind a per-dungeon Permit item.

    Additive to city access: a permit only helps once the dungeon's city is also unlocked.
    Disabling it removes all permits, dungeon maps and compasses from the item pool.
    """

    display_name = "Dungeon Gating"


class ChaosWarpPortals(Toggle):
    """Give every player a different paired portal permutation instead of a shared one.

    Requires Randomize Maps. Party members entering the same portal can split.
    This higher-difficulty room-wide setting must match for every player.
    """

    display_name = "Chaos Warp Portals"


class DeathLink(Toggle):
    """Share deaths with other DeathLink players in the multiworld.

    Off by default. When enabled the bridge joins the DeathLink tag: every death
    on this server announces one link, and every received link kills all online
    characters once per cooldown. Injected deaths are never rebroadcast.
    """

    display_name = "Death Link"
    default = 0


class Campaign(Choice):
    """Optional room-wide expedition, separate from every player's personal victory.

    Shared requires 12 distinct map surveys and 2 job certifications per roster member.
    Each slot/milestone counts once. Solo shared uses the same single-member targets.
    Must match for every Ragnarok Online player; no party or trading is required.
    """

    display_name = "Server Campaign"
    option_off = 0
    option_shared = 1
    default = option_off


class Goal(Choice):
    """Complete every selected guild quest, or complete them all and defeat the seeded native boss.

    Certifications are personal. Shared job rights and city unlocks do not complete quests.
    """

    display_name = "Goal"
    option_complete_jobs = 0
    option_kill_boss = 2
    default = option_complete_jobs


class JobPoolSize(Range):
    """Number of randomized first-job guilds and their cities included in the run."""

    display_name = "Randomized Job Count"
    range_start = 1
    range_end = 6
    default = 6


class TrapChance(Range):
    """Percentage chance for each filler item to be a trap instead of Zeny."""

    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 20


class KillChecks(DefaultOnToggle):
    """Include one slay-all-mob-types check per eligible outdoor region and dungeon chain."""

    display_name = "Kill Checks"


class GatherChecks(DefaultOnToggle):
    """Collect every eligible common drop type once per region. Items need not be retained."""

    display_name = "Gather Checks"


class NotableChecks(DefaultOnToggle):
    """Defeat one native notable monster per region, including reachable native bosses."""

    display_name = "Notable Monster Checks"


class BaseLevelChecks(DefaultOnToggle):
    """Reach base levels 10, 20 and 40 on one character. No unlocks are required."""

    display_name = "Base Level Checks"


class CityUnlockSharing(Choice):
    """Share city unlocks, including starting cities, with every Ragnarok slot in the room.

    Must match for every player. Per Person preserves independent access.
    """

    display_name = "City Unlock Sharing"
    option_per_person = 0
    option_server_wide = 1
    default = 0


class JobUnlockSharing(CityUnlockSharing):
    """Share guild-earned job entitlements, but not career state or quest checks.

    Must match for every player. Tokens never grant an entitlement by themselves.
    """

    display_name = "Job Unlock Sharing"


class SkillUnlockSharing(CityUnlockSharing):
    """Share each received skill grant. Grants add across slots, capped at skill maximum.

    Base skill levels are not multiplied. Must match for every player.
    """

    display_name = "Skill Unlock Sharing"


class DungeonPermitSharing(CityUnlockSharing):
    """Share dungeon permits, not maps or compasses. City access is still required.

    A slot with Dungeon Gating disabled needs no permit. Must match for every player.
    """

    display_name = "Dungeon Permit Sharing"


@dataclass
class RagnarokOptions(PerGameCommonOptions):
    difficulty: Difficulty
    autoloot: Autoloot
    randomize_maps: RandomizeMaps
    chaos_warp_portals: ChaosWarpPortals
    dungeon_gating: DungeonGating
    death_link: DeathLink
    campaign: Campaign
    city_unlock_sharing: CityUnlockSharing
    job_unlock_sharing: JobUnlockSharing
    skill_unlock_sharing: SkillUnlockSharing
    dungeon_permit_sharing: DungeonPermitSharing
    job_pool_size: JobPoolSize
    goal: Goal
    trap_chance: TrapChance
    kill_checks: KillChecks
    gather_checks: GatherChecks
    notable_checks: NotableChecks
    base_level_checks: BaseLevelChecks


option_groups = [
    OptionGroup(
        "Room Unlock Sharing",
        [CityUnlockSharing, JobUnlockSharing, SkillUnlockSharing, DungeonPermitSharing],
    ),
    OptionGroup(
        "Gameplay Options",
        [
            Difficulty,
            Autoloot,
            RandomizeMaps,
            ChaosWarpPortals,
            DungeonGating,
            DeathLink,
            Campaign,
            JobPoolSize,
            Goal,
            TrapChance,
        ],
    ),
    OptionGroup(
        "Content Checks",
        [
            KillChecks,
            GatherChecks,
            NotableChecks,
            BaseLevelChecks,
        ],
    ),
]
