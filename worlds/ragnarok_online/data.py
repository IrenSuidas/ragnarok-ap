import json
from importlib.resources import files

REGION_DATA = json.loads(files(__package__).joinpath("region_data.json").read_text())
CONTENT_CHECKS = json.loads(files(__package__).joinpath("check_data.json").read_text())[
    "checks"
]
CITIES = REGION_DATA["cities"]
PORTALS = REGION_DATA["portals"]
MAPS = sorted({name for names in CITIES.values() for name in names})
JOBS = {
    "Swordman": 32700,
    "Archer": 32701,
    "Acolyte": 32702,
    "Thief": 32703,
    "Mage": 32704,
    "Merchant": 32705,
}
NOVICE_TOKEN = 32706
CITY_JOBS = {
    "izlude": "Swordman",
    "payon": "Archer",
    "prontera": "Acolyte",
    "morocc": "Thief",
    "geffen": "Mage",
    "alberta": "Merchant",
}
JOB_GUILDS = {
    "Swordman": "izlude_in",
    "Archer": "payon_in02",
    "Acolyte": "prt_church",
    "Thief": "moc_prydb1",
    "Mage": "geffen_in",
    "Merchant": "alberta_in",
}
DIFFICULTIES = {
    "easy": {"base_exp_rate": 200, "job_exp_rate": 200, "item_rate": 200},
    "normal": {"base_exp_rate": 300, "job_exp_rate": 300, "item_rate": 500},
    "mid": {"base_exp_rate": 500, "job_exp_rate": 500, "item_rate": 1000},
    "hard": {"base_exp_rate": 1000, "job_exp_rate": 1000, "item_rate": 2000},
}
BOSS_LOCATION = "Defeat Final Boss"
BOSS_LOCATION_ID = 23
