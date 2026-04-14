"""
display.py – Pygame display initialisation, virtual canvas, clock, and fonts.

Virtual-canvas pattern
───────────────────────
All game drawing happens on `screen` – a Surface fixed at the base resolution
(SW × SH = 1100 × 650).  At the end of every frame, call display.flip() which:

  1. Smoothly scales `screen` to the actual fullscreen window while preserving
     aspect ratio (black letterbox/pillarbox bars fill leftover space).
  2. Calls pygame.display.flip().

4-K / DPI-scaling fix
──────────────────────
On Windows, the OS applies a DPI scale factor (125 %, 150 %, 200 % …) so that
applications appear the same physical size on high-density screens.  Without
intervention, pygame.display.Info() returns the *logical* (scaled-down)
resolution and the rendered canvas is upscaled by the OS, producing blur.

We call SetProcessDpiAwareness(2) via ctypes before pygame.init() so that the
OS reports the true physical pixel count (e.g. 3840 × 2160 on a 4-K screen).
pygame then gets the real resolution and our smoothscale fills every pixel.
"""

import sys
import pygame
from constants import SW, SH


# ── Public references (None until init() is called) ───────────────────────────
window  = None   # actual OS window / fullscreen surface
screen  = None   # virtual canvas at SW × SH  ← all modules draw here
clock   = None

f_title = None
f_big   = None
f_med   = None
f_sm    = None
f_xs    = None

# ── Letterbox geometry (computed once in init) ────────────────────────────────
_dst_rect = None   # pygame.Rect — where the canvas lands on the window
_win_w    = 0
_win_h    = 0

# ── Display-mode table ────────────────────────────────────────────────────────
# Each entry: (label shown in options, width, height)
# width/height of 0 means fullscreen at native resolution.
DISPLAY_MODES = [
    ("Fullscreen",       0,    0   ),
    ("Window 1100×650",  1100, 650 ),
    ("Window 1650×975",  1650, 975 ),
    ("Window 2200×1300", 2200, 1300),
]
_mode_idx: int = 0   # index into DISPLAY_MODES


# ── DPI awareness (Windows only) ─────────────────────────────────────────────
def _set_dpi_aware() -> None:
    """
    Tell Windows to report physical pixels, not DPI-scaled logical pixels.
    Must be called BEFORE pygame.init() / SDL initialises the display.

    Tries the modern per-monitor-aware API first (Windows 8.1+), falls back
    to the legacy system-DPI-aware call (Vista+).  No-op on non-Windows.
    """
    if sys.platform != "win32":
        return
    import ctypes
    try:
        # PROCESS_PER_MONITOR_DPI_AWARE = 2  (shcore, Win 8.1+)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except Exception:
        pass
    try:
        # Legacy fallback: SetProcessDPIAware (user32, Vista+)
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def init(title: str, fps: int) -> None:
    """
    Initialise pygame, open a fullscreen window at the true native resolution,
    create the virtual canvas, and load fonts.
    """
    global window, screen, clock, _dst_rect, _win_w, _win_h
    global f_title, f_big, f_med, f_sm, f_xs

    # Must come before pygame.init() so SDL sees the real pixel dimensions
    _set_dpi_aware()

    pygame.init()

    # ── Open fullscreen at the physical display resolution ────────────────────
    # Passing (0, 0) lets SDL choose the current display size automatically;
    # after set_mode we read the actual surface dimensions.
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    pygame.display.set_caption(title)

    _win_w, _win_h = window.get_size()

    # ── Virtual canvas ────────────────────────────────────────────────────────
    screen = pygame.Surface((SW, SH))

    # ── Aspect-ratio-preserving destination rect ──────────────────────────────
    _dst_rect = _compute_dst_rect(_win_w, _win_h)

    clock = pygame.time.Clock()

    # ── Fonts (sized for the virtual canvas; smoothscale handles the rest) ────
    f_title = pygame.font.SysFont("Arial", 46, bold=True)
    f_big   = pygame.font.SysFont("Arial", 32, bold=True)
    f_med   = pygame.font.SysFont("Arial", 23, bold=True)
    f_sm    = pygame.font.SysFont("Arial", 18)
    f_xs    = pygame.font.SysFont("Arial", 14)

    scale = _dst_rect.w / SW
    print(f"[display] Physical display : {_win_w} × {_win_h}")
    print(f"[display] Virtual canvas   : {SW} × {SH}")
    print(f"[display] Rendered canvas  : {_dst_rect.w} × {_dst_rect.h}  "
          f"(×{scale:.2f})  offset ({_dst_rect.x}, {_dst_rect.y})")


def to_canvas(mouse_pos: tuple) -> tuple:
    """Convert a window mouse position to virtual-canvas coordinates (SW × SH)."""
    if _dst_rect is None or _dst_rect.w == 0 or _dst_rect.h == 0:
        return mouse_pos
    mx, my = mouse_pos
    cx = (mx - _dst_rect.x) * SW / _dst_rect.w
    cy = (my - _dst_rect.y) * SH / _dst_rect.h
    return int(cx), int(cy)


def flip() -> None:
    """
    Scale the virtual canvas onto the fullscreen window (aspect-correct,
    black bars outside) and flip the display buffer.
    Call once per frame instead of pygame.display.flip().
    """
    window.fill((0, 0, 0))
    scaled = pygame.transform.smoothscale(screen, (_dst_rect.w, _dst_rect.h))
    window.blit(scaled, _dst_rect)
    pygame.display.flip()


# ── Display-mode helpers (call from options menu) ─────────────────────────────
def current_mode_idx() -> int:
    return _mode_idx


def current_mode_name() -> str:
    return DISPLAY_MODES[_mode_idx][0]


def mode_count() -> int:
    return len(DISPLAY_MODES)


def set_mode_idx(idx: int) -> None:
    """Switch to the display mode at the given index (wraps around)."""
    global window, _win_w, _win_h, _dst_rect, _mode_idx
    _mode_idx     = idx % len(DISPLAY_MODES)
    _, w, h       = DISPLAY_MODES[_mode_idx]
    if w == 0:
        window = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    else:
        window = pygame.display.set_mode(
            (w, h), pygame.DOUBLEBUF | pygame.RESIZABLE)
    _win_w, _win_h = window.get_size()
    _dst_rect      = _compute_dst_rect(_win_w, _win_h)
    print(f"[display] Mode → {current_mode_name()}  ({_win_w}×{_win_h})")


# ── Internal ──────────────────────────────────────────────────────────────────
def _compute_dst_rect(win_w: int, win_h: int) -> pygame.Rect:
    """Return the centred, aspect-correct destination rect for the canvas."""
    scale    = min(win_w / SW, win_h / SH)
    dst_w    = int(SW * scale)
    dst_h    = int(SH * scale)
    offset_x = (win_w - dst_w) // 2
    offset_y = (win_h - dst_h) // 2
    return pygame.Rect(offset_x, offset_y, dst_w, dst_h)
