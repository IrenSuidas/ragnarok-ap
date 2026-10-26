from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups


class RagnarokWebWorld(WebWorld):
    game = "Ragnarok Online"
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Ragnarok Online for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Iren"],
    )

    tutorials = [setup_en]
    option_groups = option_groups
