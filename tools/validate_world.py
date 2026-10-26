import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_apworld import build, verify

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "worlds/ragnarok_online"
MANIFEST = WORLD / "archipelago.json"
PLAYERS = ROOT / "players/ragnarok.yaml"
GAME = "Ragnarok Online"
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
DATA_FILES = (
    "check_data.json",
    "dungeon_data.json",
    "region_data.json",
    "wandering_data.json",
)


def inventory(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def check_manifest():
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["game"] == GAME, manifest
    assert VERSION.fullmatch(manifest["world_version"]), manifest
    assert isinstance(manifest.get("authors"), list) and manifest["authors"], manifest
    for field in ("minimum_ap_version", "maximum_ap_version"):
        if field in manifest:
            assert VERSION.fullmatch(manifest[field]), manifest
    return manifest


def check_package():
    modules = {path.name for path in WORLD.glob("*.py")}
    for required in ("__init__.py", "world.py", "options.py", "web_world.py"):
        assert required in modules, sorted(modules)
    for data in DATA_FILES:
        assert (WORLD / data).is_file(), data
    checks = json.loads((WORLD / "check_data.json").read_text())["checks"]
    assert checks, "The content check catalog is empty"
    return len(checks)


def check_docs():
    game = (WORLD / "docs" / f"en_{GAME}.md").read_text()
    setup = (WORLD / "docs" / "setup_en.md").read_text()
    assert game.strip() and setup.strip()
    web = (WORLD / "web_world.py").read_text()
    assert "setup_en.md" in web, web
    assert "tutorials" in web, web
    assert f'game = "{GAME}"' in web, web
    return len(game) + len(setup)


def check_players():
    player = yaml.safe_load(PLAYERS.read_text())
    assert player["game"] == GAME, player
    declared = set(re.findall(r"^    (\w+):", (WORLD / "options.py").read_text(), re.M))
    unknown = sorted(set(player[GAME]) - declared)
    assert not unknown, unknown
    return sorted(player[GAME])


def check_build():
    with tempfile.TemporaryDirectory(prefix="ragnarok-apworld-") as directory:
        first = Path(directory) / "first.apworld"
        second = Path(directory) / "second.apworld"
        manifest = build(WORLD, first)
        verify(first, WORLD)
        build(WORLD, second)
        assert first.read_bytes() == second.read_bytes(), (
            "Builds are not byte-identical"
        )
        assert manifest == {
            **json.loads(MANIFEST.read_text()),
            "version": 7,
            "compatible_version": 7,
        }, manifest
        return hashlib.sha256(first.read_bytes()).hexdigest()


def main():
    manifest = check_manifest()
    checks = check_package()
    docs = check_docs()
    players = check_players()
    artifact = check_build()
    print(
        f"PASS world {manifest['game']} {manifest['world_version']}: "
        f"{len(inventory(WORLD))} files, {checks} content checks, {docs} doc chars, "
        f"players {players}; reproducible apworld {artifact}"
    )


if __name__ == "__main__":
    main()
