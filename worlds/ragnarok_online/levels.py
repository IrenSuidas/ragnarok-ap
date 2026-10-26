THRESHOLDS = (10, 20, 40)
CHECKS = tuple(
    {
        "location": 3100 + level,
        "name": f"Reach Base Level {level}",
        "kind": "base_level",
        "required_count": level,
    }
    for level in THRESHOLDS
)
