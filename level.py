"""
level.py – Builds the door and key objects for each level.

Each door has a fixed subject (Door 1=Grammar, Door 2=Vocabulary, Door 3=Science).
Questions are NOT assigned here; they are drawn per-door on first touch (see game.py).
"""
import random
import constants as C
from questions import LEVEL_CFG, BONUS_POOL
from door import Door
from key_item import KeyItem


def new_level_data(lvl: int) -> tuple:
    """
    Build and return (doors, key_items) for the given level.

    doors     – list of 3 Door objects at fixed wall positions
    key_items – list of KeyItem objects (empty for levels 1–3)
    """
    cfg = LEVEL_CFG.get(lvl, {"locked": [], "keys": []})

    # ── Three doors at fixed positions ────────────────────────────────────────
    doors = [
        Door(C.D1X, C.D1Y, 1, side="top"),
        Door(C.D2X, C.D2Y, 2, side="bottom"),
        Door(C.D3X, C.D3Y, 3, side="right"),
    ]
    for d in doors:
        d.locked = d.num in cfg["locked"]

    # ── Key items ─────────────────────────────────────────────────────────────
    key_items = [KeyItem(kx, ky, kn) for kx, ky, kn in cfg["keys"]]

    return doors, key_items


def random_bonus_question() -> dict:
    """Return a random bonus-round question."""
    return random.choice(BONUS_POOL)
