# Ragnarok Online

Ragnarok Online is randomized as a solo, finishable run on a shared rAthena game server. Each
player owns one personal AP slot bound to exactly one game character. Unlocks, checks and
rewards are personal; the shuffled portal links of a room can be shared or per-slot.

## What the world randomizes

* **Cities and hub travel.** `job_pool_size` selects how many of the six main cities
  (Izlude, Payon, Prontera, Morocc, Geffen, Alberta) participate. The seed picks your
  starting city, which is granted at the start; every other selected city is gated behind an
  `Unlock: <city>` progression item. Your starting city fixes the first job you can earn.
* **Portal randomization.** `randomize_maps` permutes the paired exterior exits of every
  selected city, keeping returns paired so you come back beside the exit you used. Other
  portals are untouched. `chaos_warp_portals` gives each slot its own permutation instead of a
  room-wide one.
* **Dungeon gating.** `dungeon_gating` adds a `Permit: <dungeon>` progression item to every
  selected city's dungeons. A permit only helps once its city is unlocked. The dedicated
  `Map: <dungeon>` and `Compass: <dungeon>` items are informational (useful, never required).
* **Jobs.** Every slot starts as a Novice (base level 1 / job level 1). Reaching a selected
  city's guild and completing its job-change quest is the `Job: <job>` check; a
  `Certified: <job>` event marks the acquisition and grants that job's switch token. The
  Novice token (unlocked at job level 10) returns you to Novice base 10 / job 10 so you can
  earn the next selected job.
* **Skills.** `Skill: <name> +<levels>` items grant exact skill levels (for example
  "Double Strafe +7", later "+3"). Grants are clamped to each skill's native maximum.
* **Difficulty.** `difficulty` picks the base/job EXP and item drop multipliers applied to
  every character in the run.
* **Traps.** `trap_chance` is the chance that filler items are replaced with a trap.

## Locations

* **Reach `<map>`** - one per selected-city map.
* **Job: `<job>`** - one per selected job.
* **Kill / gather / notable content checks** - per selected city, toggled by the
  `kill_checks`, `gather_checks` and `notable_checks` options.
* **Reach Base Level `<n>`** - base level milestones, toggled by `base_level_checks`.
* **Seek the Wandering AP NPC** - one hidden wandering NPC placement.
* **Adventurer's Essentials** - wear a weapon, armor, garment and shoes at least once.
* **Defeat Final Boss** - defeat the seed's selected native boss.

## Goal

`goal` chooses the completion condition:

* `complete_jobs` (default) - complete every selected job's guild quest.
* `kill_boss` - complete every selected job's guild quest, then defeat the seed's selected
  native boss.

`campaign` is a separate, optional room-wide expedition goal (off or shared) that does not
replace a player's personal victory.

## Room-wide settings

Several options are frozen with a generation and must match across every Ragnarok Online slot
in the room, because the game server and bridge install them once for the whole room:

* `city_unlock_sharing`, `job_unlock_sharing`, `skill_unlock_sharing` and
  `dungeon_permit_sharing` (`per_person` or `server_wide`),
* `chaos_warp_portals` and `randomize_maps`,
* `campaign`.

Generation and bridge installation reject any disagreement. Changing a room-wide setting
requires generating and hosting a new room.

## DeathLink

`death_link` is opt-in and off by default. When enabled, the bridge joins the `DeathLink` tag
and applies an incoming link only to the receiving slot's bound character; NPC-side
suppression stops injected deaths from being rebroadcast.
