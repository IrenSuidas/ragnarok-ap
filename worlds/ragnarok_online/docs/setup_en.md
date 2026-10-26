# Ragnarok Online Multiworld Setup Guide

## What is a YAML file and why do I need it?

A YAML file holds the options for *your* slot in a multiworld. It tells the generator which
Ragnarok Online content to randomize for you. See the
[Archipelago setup guide](https://archipelago.gg/tutorial/Archipelago/setup/en) if you have
never made one before.

You can create a Ragnarok Online YAML from the Archipelago Launcher's Options Creator (pick
"Ragnarok Online") or by editing `players/ragnarok.yaml` from this repository.

## What is randomized

Ragnarok Online is generated as one or more personal AP slots on a single shared game
server. The world decides:

* which **cities** are available in the run (the `job_pool_size` option), and which one you
  start in;
* which **paired hub exits** are shuffled inside each selected city (`randomize_maps`, and
  `chaos_warp_portals` for per-slot permutations);
* which **dungeon entrances** require a `Permit` (`dungeon_gating`);
* which **skills** each job can obtain from items;
* the **checks** (map visits, job acquisitions, kills, gathers, notables, base levels,
  wandering NPC, equipment);
* the **goal** (`goal`).

The generator emits a `slot_data` payload that the game server uses to lock cities,
install the portal permutation, seed the check catalog and apply difficulty tiers.

## Installing the APWorld

Download `ragnarok_online.apworld` from this repository's releases (or build it locally, see
`tools/`), then install it with the Archipelago Launcher's **Install APWorld** button.
Restart the Launcher and the game will appear in the generator's game list.

`minimum_ap_version` and `maximum_ap_version` in `worlds/ragnarok_online/archipelago.json`
pin the world to a specific Archipelago release. Do not generate a Ragnarok Online seed
with a different Archipelago version than the one the manifest allows.

## Running the game server

This APWorld covers only generation. Playing a seed requires the rAthena-based Ragnarok
Online server bundle plus its AP bridge, which connects to the multiworld server and turns
`slot_data`, checks and received items into server-side database state.

1. Start the server bundle (its Compose stack brings up MariaDB, rAthena, the game panel and
   the bridge).
2. Host a room: create a game on the Archipelago website or your own server with your YAML
   and `Ragnarok Online` as your game.
3. Open the game panel, enter the room's server address and slot name, then generate and host
   the room from the panel (or point the bridge at an external room).
4. Log in with the account the bridge provisioned for your slot. You start as a **Novice**
   (base level 1 / job level 1) in your slot's starting city.
5. Level to **job level 10**, then complete that city's guild job-change quest: it is the
   `Job: <job>` check, grants the class and its switch token, and a `Certified: <job>` event
   marks it. The **Novice token** (unlocked at job level 10) returns you to Novice base 10 /
   job 10 so you can earn the next selected job.
6. Play: unlock cities with `Unlock: <city>` items, find `Permit`, `Skill: <name> +<levels>`,
   `Map`, `Compass` and `Ticket: Poring Village` items, and complete checks until your goal is
   met.

The server bundle is not part of this repository. See its README for the Compose, database
and client setup.
