"""
assets.py – PNG sprite loader with graceful fallback to procedural drawing.

Place your files in the  assets/  folder next to game.py:

    assets/
    ├── kirby.png          Player sprite        (recommended: 60 × 60 px, transparent bg)
    ├── door.png           Default door         (recommended: 90 × 130 px, transparent bg)
    ├── door_correct.png   Correct-answer door  (optional)
    ├── door_locked.png    Locked door          (optional)
    ├── background.png     Stage background     (optional, scaled to 1100 × 650)
    └── music/             Background music folder (see music.py)
        ├── track_01.mp3   Any number of .mp3 files
        └── track_02.mp3   Played in alphabetical order, looping

If any image file is missing the game falls back to built-in procedural drawing for
that element – you can add images incrementally without breaking anything.
Music files are handled separately by music.py (also optional).

Scaled sizes are taken from constants so everything stays consistent if you
change DW/DH or PR in constants.py.
"""

import os
import pygame
import constants as C

# Public sprite references – None until load_all() is called
player_img        = None   # kirby.png              scaled to (PR*2) × (PR*2)
miles_img         = None   # miles.png              scaled to (PR*2) × (PR*2)
door_img          = None   # door.png               scaled to DW × DH
door_correct_img  = None   # door_correct.png       scaled to DW × DH
door_locked_img   = None   # door_locked.png        scaled to DW × DH
bg_img            = None   # background.png         generic fallback, SW × SH
bg_imgs: dict     = {}     # background{N}.png      level-specific, keyed by int
question_panel_img = None  # question_panel.png     right-side panel on question screen (550×650)

_ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")


def _load(filename: str, size: tuple | None = None):
    """
    Try to load <filename> from the assets/ folder.
    Returns a scaled Surface on success, or None if the file is missing.
    """
    path = os.path.join(_ASSET_DIR, filename)
    if not os.path.isfile(path):
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error as e:
        print(f"[assets] Warning: could not load '{filename}': {e}")
        return None


def load_all() -> None:
    """
    Load every sprite from the assets/ folder.
    Call this once after pygame.init() and display.init().
    Missing files are silently skipped; their module-level variable stays None.
    """
    global player_img, miles_img, door_img, door_correct_img, door_locked_img
    global bg_img, bg_imgs, question_panel_img

    player_img         = _load("kirby.png",          (C.PR * 2, C.PR * 2))
    miles_img          = _load("miles.png",          (C.PR * 2, C.PR * 2))
    door_img           = _load("door.png",            (C.DW,     C.DH))
    door_correct_img   = _load("door_correct.png",    (C.DW,     C.DH))
    door_locked_img    = _load("door_locked.png",     (C.DW,     C.DH))
    bg_img             = _load("background.png",      (C.SW,     C.SH))
    question_panel_img = _load("question_panel.png",  (550,      C.SH))

    # Per-level backgrounds: background1.png … background6.png
    bg_imgs = {}
    for lvl in range(1, C.TOTAL + 1):
        img = _load(f"background{lvl}.png", (C.SW, C.SH))
        if img:
            bg_imgs[lvl] = img

    # ── Report ────────────────────────────────────────────────────────────────
    sprites = {
        "kirby.png":            player_img,
        "miles.png":            miles_img,
        "door.png":             door_img,
        "door_correct.png":     door_correct_img,
        "door_locked.png":      door_locked_img,
        "background.png":       bg_img,
        "question_panel.png":   question_panel_img,
    }
    for name, img in sprites.items():
        status = "loaded" if img else "not found – procedural fallback"
        print(f"[assets] {name:<24} {status}")
    for lvl in range(1, C.TOTAL + 1):
        img = bg_imgs.get(lvl)
        name = f"background{lvl}.png"
        status = "loaded" if img else "not found – procedural theme"
        print(f"[assets] {name:<24} {status}")
