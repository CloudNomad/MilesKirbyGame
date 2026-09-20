"""
sounds.py – UI sound-effect loader and player.

Place sound files in  assets/sounds/  :

    menu_nav.mp3       – played when the cursor moves in a menu (↑ / ↓)
    menu_select.mp3    – played when confirming a selection (Enter)
    grade_select.mp3   – played when a grade is chosen on the grade screen

Supports .mp3, .wav, and .ogg (checked in that order).
If a file is missing the call is silently ignored.
pygame.mixer must already be initialised (music.init() does this).
"""

import os
import sys
import pygame

_SOUNDS_DIR = os.path.join(
    getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))),
    "assets", "sounds"
)

_snd:        dict  = {}    # key → pygame.Sound  (populated by init())
_sfx_volume: float = 0.6   # 0.0 – 1.0  (persists across set_volume calls)

# Per-key multipliers applied on top of _sfx_volume (capped at 1.0).
_MULTIPLIERS: dict = {"select": 2.0}

_FILES = {
    "nav":    ["menu_nav.mp3",      "menu_nav.wav",      "menu_nav.ogg"],
    "select": ["menu_select.mp3",   "menu_select.wav",   "menu_select.ogg"],
    "grade":  ["grade_select.mp3",  "grade_select.wav",  "grade_select.ogg"],
    "star":   ["star_reveal.mp3",   "star_reveal.wav",   "star_reveal.ogg"],
}


def init() -> None:
    """Load sound effects.  Safe to call even if the folder is missing."""
    if not os.path.isdir(_SOUNDS_DIR):
        print(f"[sounds] No sounds folder at {_SOUNDS_DIR} – UI sounds disabled.")
        print( "[sounds] Create  assets/sounds/  and add  menu_nav.wav, "
               "menu_select.wav, grade_select.wav  to enable them.")
        return

    for key, candidates in _FILES.items():
        for fname in candidates:
            path = os.path.join(_SOUNDS_DIR, fname)
            if os.path.isfile(path):
                try:
                    _snd[key] = pygame.mixer.Sound(path)
                    _snd[key].set_volume(min(1.0, _sfx_volume * _MULTIPLIERS.get(key, 1.0)))
                    print(f"[sounds] Loaded {key:8s} <- {fname}")
                except pygame.error as e:
                    print(f"[sounds] Could not load {fname}: {e}")
                break

    missing = [k for k in _FILES if k not in _snd]
    if missing:
        print(f"[sounds] Missing: {', '.join(missing)}"
              f"  (add files to assets/sounds/ to enable)")


# ── Volume control ─────────────────────────────────────────────────────────────

def volume() -> float:
    """Return the current sound-effect volume (0.0 – 1.0)."""
    return _sfx_volume


def set_volume(v: float) -> None:
    """Set sound-effect volume and apply it to all loaded sounds."""
    global _sfx_volume
    _sfx_volume = max(0.0, min(1.0, v))
    for key, snd in _snd.items():
        snd.set_volume(min(1.0, _sfx_volume * _MULTIPLIERS.get(key, 1.0)))


def volume_up(step: float = 0.1) -> None:
    set_volume(_sfx_volume + step)


def volume_down(step: float = 0.1) -> None:
    set_volume(_sfx_volume - step)


# ── Playback ───────────────────────────────────────────────────────────────────

def _play(key: str) -> None:
    snd = _snd.get(key)
    if snd:
        snd.play()


def play_nav() -> None:
    """Cursor-move tick — arrow key pressed in any menu."""
    _play("nav")


def play_select() -> None:
    """Confirm / enter a menu item."""
    _play("select")


def play_grade_select() -> None:
    """Grade confirmed on the grade-select screen."""
    snd = _snd.get("grade") or _snd.get("select")
    if snd:
        snd.play()


def play_star_reveal() -> None:
    """Triumphant sting played on the star-reveal popup after a correct answer."""
    snd = _snd.get("star") or _snd.get("select")
    if snd:
        snd.play()
