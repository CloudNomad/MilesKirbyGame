"""
assets.py – Sprite loader (PNG + animated GIF) with graceful fallback.

Place files in the  assets/  folder next to game.py:

    assets/
    ├── kirby.png              Player sprite           (60 × 60, transparent bg)
    ├── miles.png              Miles player sprite     (60 × 60, transparent bg)
    ├── portal.gif             Portal – default/base   (DW × DH, animated GIF)
    ├── portal1.gif            Portal door 1 override  (optional)
    ├── portal2.gif            Portal door 2 override  (optional)
    ├── portal3.gif            Portal door 3 override  (optional)
    ├── portal_locked.gif      Locked-portal override  (optional; falls back to portal.gif + dark overlay)
    ├── portal_correct.gif     Correct-portal override (optional; falls back to portal.gif + gold glow)
    ├── door.png               Static door fallback    (used only if no portal GIF is found)
    ├── door_correct.png       Static correct-door fallback (optional)
    ├── door_locked.png        Static locked-door fallback  (optional)
    ├── background.png         Stage background        (optional, scaled to 1100 × 650)
    ├── background1.png … background6.png  Per-world backgrounds
    ├── question_panel.png     Right panel on question screen (550 × 650)
    └── MainMenu.png           Title screen background

GIF animation uses Pillow (pip install pillow).  If Pillow is not installed the
loader falls back to pygame's own GIF loader (first frame only, no animation).
Missing files are silently skipped; their variable stays None / [].
"""

import os
import sys
from io import BytesIO

import pygame
import constants as C

# ── Static sprite references ──────────────────────────────────────────────────
player_img        = None
miles_img         = None
secret1_img       = None
secret2_img       = None
door_img          = None   # static fallback (no portal GIF present)
door_correct_img  = None
door_locked_img   = None
bg_img            = None
bg_imgs: dict     = {}
question_panel_img = None
main_menu_img     = None

# ── Animated portal frame lists: [(Surface, duration_ms), …] ─────────────────
portal_frames: list          = []   # portal.gif  – base for all doors
portal_locked_frames: list   = []   # portal_locked.gif  (optional)
portal_correct_frames: list  = []   # portal_correct.gif (optional)
portal_frames_by_num: dict   = {}   # portal{1|2|3}.gif  (optional per-door override)

_ASSET_DIR = os.path.join(
    getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))),
    "assets"
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _path(filename: str) -> str | None:
    """Return the full path for filename inside assets/, case-insensitively.
    Returns None if no match is found."""
    direct = os.path.join(_ASSET_DIR, filename)
    if os.path.isfile(direct):
        return direct
    # Case-insensitive fallback (useful on Linux; no-op on Windows)
    lower = filename.lower()
    try:
        for f in os.listdir(_ASSET_DIR):
            if f.lower() == lower:
                return os.path.join(_ASSET_DIR, f)
    except OSError:
        pass
    return None


def _load(filename: str, size: tuple | None = None) -> pygame.Surface | None:
    """Load a static image. Returns None if the file is missing."""
    p = _path(filename)
    if p is None:
        return None
    try:
        img = pygame.image.load(p).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except pygame.error as e:
        print(f"[assets] Warning: could not load '{filename}': {e}")
        return None


def _load_gif_frames(filename: str, size: tuple | None = None) -> list:
    """
    Load an animated GIF and return a list of (Surface, duration_ms) tuples.

    Requires Pillow.  Without Pillow, falls back to pygame's loader (first
    frame only — no animation).  Returns [] if the file is missing.
    """
    p = _path(filename)
    if p is None:
        return []

    # ── Pillow path (full animation) ─────────────────────────────────────────
    try:
        from PIL import Image as PilImage

        pil = PilImage.open(p)
        frames = []
        try:
            while True:
                duration = int(pil.info.get("duration", 100))
                if duration <= 0:
                    duration = 100

                # Convert this frame to RGBA — handles disposal / palette modes
                rgba = pil.convert("RGBA")

                # Use BytesIO round-trip for maximum pygame compatibility
                buf = BytesIO()
                rgba.save(buf, format="PNG")
                buf.seek(0)
                surf = pygame.image.load(buf).convert_alpha()
                if size:
                    surf = pygame.transform.smoothscale(surf, size)
                frames.append((surf, duration))

                pil.seek(pil.tell() + 1)
        except EOFError:
            pass

        print(f"[assets] {filename:<28} loaded ({len(frames)} frames)")
        return frames

    except ImportError:
        print(f"[assets] Pillow not installed — {filename}: loading first frame only")

    # ── Pygame fallback (first frame, no animation) ───────────────────────────
    try:
        surf = pygame.image.load(p).convert_alpha()
        if size:
            surf = pygame.transform.smoothscale(surf, size)
        return [(surf, 100)]
    except pygame.error as e:
        print(f"[assets] Could not load '{filename}': {e}")
        return []


# ── Frame-picker (called every draw) ─────────────────────────────────────────

def _pick_frame(frames: list) -> pygame.Surface | None:
    """Return the animation frame that matches the current clock tick."""
    if not frames:
        return None
    if len(frames) == 1:
        return frames[0][0]
    total_ms = sum(d for _, d in frames)
    if total_ms <= 0:
        return frames[0][0]
    t = pygame.time.get_ticks() % total_ms
    cumul = 0
    for surf, dur in frames:
        cumul += dur
        if t < cumul:
            return surf
    return frames[-1][0]


def get_portal_frame(door_num: int = 0) -> pygame.Surface | None:
    """Current animation frame for a normal (unlocked, incomplete) portal."""
    return _pick_frame(portal_frames_by_num.get(door_num) or portal_frames)


def get_portal_locked_frame(door_num: int = 0) -> pygame.Surface | None:
    """Current frame for locked portal (falls back to base portal GIF)."""
    return _pick_frame(portal_locked_frames) or get_portal_frame(door_num)


def get_portal_correct_frame(door_num: int = 0) -> pygame.Surface | None:
    """Current frame for completed portal (falls back to base portal GIF)."""
    return _pick_frame(portal_correct_frames) or get_portal_frame(door_num)


def has_portal_gif() -> bool:
    """True if at least the base portal.gif was loaded."""
    return bool(portal_frames)


# ── Main loader ───────────────────────────────────────────────────────────────

def load_all() -> None:
    """
    Load every sprite from the assets/ folder.
    Call once after pygame.init() and display.init().
    """
    global player_img, miles_img, secret1_img, secret2_img
    global door_img, door_correct_img, door_locked_img
    global bg_img, bg_imgs, question_panel_img, main_menu_img
    global portal_frames, portal_locked_frames, portal_correct_frames
    global portal_frames_by_num

    # ── Static sprites ────────────────────────────────────────────────────────
    player_img         = _load("kirby.png",          (C.PR * 3, C.PR * 3))
    miles_img          = _load("miles.png",           (C.PR * 3, C.PR * 3))
    secret1_img        = _load("secret1.png",         (C.PR * 3, C.PR * 3))
    secret2_img        = _load("secret2.png",         (C.PR * 3, C.PR * 3))
    door_img           = _load("door.png",             (C.DW,     C.DH))
    door_correct_img   = _load("door_correct.png",     (C.DW,     C.DH))
    door_locked_img    = _load("door_locked.png",      (C.DW,     C.DH))
    bg_img             = _load("background.png",       (C.SW,     C.SH))
    question_panel_img = _load("question_panel.png",   (550,      C.SH))
    main_menu_img      = _load("MainMenu.png",         (C.SW,     C.SH))

    # ── Per-level backgrounds ─────────────────────────────────────────────────
    bg_imgs = {}
    for lvl in range(1, C.TOTAL + 1):
        img = _load(f"background{lvl}.png", (C.SW, C.SH))
        if img:
            bg_imgs[lvl] = img

    # ── Animated portal GIFs ──────────────────────────────────────────────────
    # Portals are drawn square (DW×DW) and centred vertically in the DH slot
    _ps = (C.DW, C.DW)
    portal_frames        = _load_gif_frames("portal.gif",         _ps)
    portal_locked_frames = _load_gif_frames("portal_locked.gif",  _ps)
    portal_correct_frames= _load_gif_frames("portal_correct.gif", _ps)

    portal_frames_by_num = {}
    for i in range(1, 4):
        frames = _load_gif_frames(f"portal{i}.gif", _ps)
        if frames:
            portal_frames_by_num[i] = frames

    # ── Report ────────────────────────────────────────────────────────────────
    static_sprites = {
        "kirby.png":          player_img,
        "miles.png":          miles_img,
        "secret1.png":        secret1_img,
        "secret2.png":        secret2_img,
        "door.png":           door_img,
        "door_correct.png":   door_correct_img,
        "door_locked.png":    door_locked_img,
        "background.png":     bg_img,
        "question_panel.png": question_panel_img,
        "MainMenu.png":       main_menu_img,
    }
    for name, img in static_sprites.items():
        status = "loaded" if img else "not found – procedural fallback"
        print(f"[assets] {name:<28} {status}")
    for lvl in range(1, C.TOTAL + 1):
        name   = f"background{lvl}.png"
        status = "loaded" if bg_imgs.get(lvl) else "not found – procedural theme"
        print(f"[assets] {name:<28} {status}")
