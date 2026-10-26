SKILLS = (
    (1, 2, "Sword Mastery", 10),
    (1, 3, "Two-Handed Sword Mastery", 10),
    (1, 4, "Increase HP Recovery", 10),
    (1, 5, "Bash", 10),
    (1, 6, "Provoke", 10),
    (1, 7, "Magnum Break", 10),
    (1, 8, "Endure", 10),
    (2, 9, "Increase SP Recovery", 10),
    (2, 10, "Sight", 1),
    (2, 14, "Cold Bolt", 10),
    (2, 18, "Fire Wall", 10),
    (2, 19, "Fire Bolt", 10),
    (2, 20, "Lightning Bolt", 10),
    (3, 43, "Owl's Eye", 10),
    (3, 44, "Vulture's Eye", 10),
    (3, 45, "Improve Concentration", 10),
    (3, 46, "Double Strafe", 10),
    (3, 47, "Arrow Shower", 10),
    (4, 22, "Divine Protection", 10),
    (4, 24, "Ruwach", 1),
    (4, 25, "Pneuma", 1),
    (4, 26, "Teleport", 2),
    (4, 27, "Warp Portal", 4),
    (4, 28, "Heal", 10),
    (4, 29, "Increase AGI", 10),
    (5, 36, "Enlarge Weight Limit", 10),
    (5, 37, "Discount", 10),
    (5, 38, "Overcharge", 10),
    (5, 39, "Pushcart", 10),
    (5, 40, "Item Appraisal", 1),
    (5, 41, "Vending", 10),
    (5, 42, "Mammonite", 10),
    (6, 48, "Double Attack", 10),
    (6, 49, "Improve Dodge", 10),
    (6, 50, "Steal", 10),
    (6, 51, "Hiding", 10),
    (6, 52, "Envenom", 10),
    (6, 53, "Detoxify", 1),
)

SKILL_ITEMS = {
    f"Skill: {name} +{levels}": {
        "item_id": 1000 + skill_id * 10 + levels,
        "job_id": job_id,
        "skill_id": skill_id,
        "levels": levels,
    }
    for job_id, skill_id, name, maximum in SKILLS
    for levels in ((6, 3) if maximum == 10 else (maximum - 1,) if maximum > 1 else ())
}


def slot_catalog(jobs=None):
    return {
        "skills": [
            {"job_id": job, "skill_id": skill, "maximum": maximum}
            for job, skill, _, maximum in SKILLS
            if jobs is None or job in jobs
        ],
        "items": {
            name: grant
            for name, grant in SKILL_ITEMS.items()
            if jobs is None or grant["job_id"] in jobs
        },
    }
