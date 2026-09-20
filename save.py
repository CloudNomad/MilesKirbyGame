"""
save.py – Lightweight JSON save / load for a single save slot.

Saved data
──────────
  grade  – selected grade (1–6)
  lvl    – current level (1–6)
  score  – current score
  lives  – remaining lives
"""

import json
import os
import sys

_BASE      = (os.path.dirname(sys.executable) if getattr(sys, "frozen", False)
              else os.path.dirname(os.path.abspath(__file__)))
_SAVE_FILE = os.path.join(_BASE, "save.json")


def exists() -> bool:
    return os.path.isfile(_SAVE_FILE)


def save(grade: int, lvl: int, score: int, lives: int) -> None:
    with open(_SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump({"grade": grade, "lvl": lvl, "score": score, "lives": lives}, f)


def load() -> dict | None:
    """Return save dict or None if no valid save file exists."""
    if not exists():
        return None
    try:
        with open(_SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Basic validation
        if all(k in data for k in ("grade", "lvl", "score", "lives")):
            return data
    except Exception:
        pass
    return None


def delete() -> None:
    if exists():
        os.remove(_SAVE_FILE)
