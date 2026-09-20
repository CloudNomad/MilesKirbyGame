"""
background.py – Draws the full-screen game arena for the current level.

Each level has a unique visual theme.  If a matching PNG exists in assets/
(background1.png … background6.png) it is used instead of the procedural
drawing.  A generic  background.png  is used as a fallback for any level that
has neither.

Themes
──────
  1 – Sunny Sky        (light blue, clouds, sun)
  2 – Forest           (green, trees)
  3 – Desert           (sandy, cacti)
  4 – Crystal Cave     (purple, stalactites / gems)
  5 – Ocean            (aqua, bubbles)
  6 – Outer Space      (dark, stars, planet)
"""

import math
import pygame
import display
import constants as C
import assets
from utils import txt


# ── Per-level theme palette ────────────────────────────────────────────────────
_THEMES = {
    1: dict(bg=(220, 235, 255), wall=(155, 170, 195),
            wall_lt=(180, 195, 218), wall_dk=(110, 128, 158)),
    2: dict(bg=(190, 225, 190), wall=(80, 130, 75),
            wall_lt=(110, 160, 100), wall_dk=(50,  95, 50)),
    3: dict(bg=(245, 220, 170), wall=(185, 145, 85),
            wall_lt=(210, 175, 115), wall_dk=(140, 105, 55)),
    4: dict(bg=(215, 195, 245), wall=(110, 70, 160),
            wall_lt=(145, 105, 200), wall_dk=( 75, 45, 115)),
    5: dict(bg=(175, 220, 240), wall=( 45,  90, 175),
            wall_lt=( 75, 125, 210), wall_dk=( 25,  60, 130)),
    6: dict(bg=( 12,  12,  38), wall=( 50,  55,  80),
            wall_lt=( 75,  80, 110), wall_dk=( 28,  30,  52)),
}


def draw_bg(lvl: int = 1) -> None:
    theme = _THEMES.get(lvl, _THEMES[1])

    # ── PNG background (level-specific → generic → procedural) ────────────────
    bg = assets.bg_imgs.get(lvl) or assets.bg_img
    if bg:
        display.screen.blit(bg, (0, 0))
    else:
        display.screen.fill(theme["bg"])
        _draw_decorations(lvl, theme)

    # ── Wall strips (flush with screen edges) ─────────────────────────────────
    wc  = theme["wall"]
    wlt = theme["wall_lt"]
    wdk = theme["wall_dk"]

    # Fills
    pygame.draw.rect(display.screen, wc, (0, 0,              C.SW, C.WT))
    pygame.draw.rect(display.screen, wc, (0, C.SH - C.WT,   C.SW, C.WT))
    pygame.draw.rect(display.screen, wc, (C.SW - C.WT, 0,   C.WT, C.SH))

    # Highlights
    pygame.draw.rect(display.screen, wlt, (0, 0,              C.SW, 3))
    pygame.draw.rect(display.screen, wlt, (0, C.SH - C.WT,   C.SW, 3))
    pygame.draw.rect(display.screen, wlt, (C.SW - C.WT, 0,   3, C.SH))

    # Shadows
    pygame.draw.rect(display.screen, wdk, (0, C.WT - 3,      C.SW, 3))
    pygame.draw.rect(display.screen, wdk, (0, C.SH - 3,      C.SW, 3))



# ── Procedural decorations per level ─────────────────────────────────────────

def _draw_decorations(lvl: int, theme: dict) -> None:
    if   lvl == 1: _level1_sky(theme)
    elif lvl == 2: _level2_forest(theme)
    elif lvl == 3: _level3_desert(theme)
    elif lvl == 4: _level4_cave(theme)
    elif lvl == 5: _level5_ocean(theme)
    elif lvl == 6: _level6_space(theme)


def _level1_sky(theme):
    """Sunny sky – clouds and a sun."""
    # Sun
    pygame.draw.circle(display.screen, (255, 235, 80), (960, 80), 52)
    pygame.draw.circle(display.screen, (255, 245, 140), (960, 80), 42)
    # Clouds (overlapping ellipses)
    for cx, cy, scale in [(200, 90, 1.0), (420, 60, 0.8), (700, 100, 1.1),
                           (140, 160, 0.7), (560, 50, 0.9)]:
        w, h = int(90 * scale), int(42 * scale)
        pygame.draw.ellipse(display.screen, (250, 252, 255), (cx - w//2, cy - h//2, w, h))
        pygame.draw.ellipse(display.screen, (250, 252, 255),
                            (cx - w//2 + 20, cy - h//2 - 10, int(w * 0.7), int(h * 0.7)))
        pygame.draw.ellipse(display.screen, (250, 252, 255),
                            (cx - w//2 - 15, cy - h//2 - 8, int(w * 0.6), int(h * 0.6)))
    # Ground gradient strip
    pygame.draw.rect(display.screen, (185, 220, 160), (0, C.SH - 60, C.SW, 60))
    pygame.draw.rect(display.screen, (160, 200, 135), (0, C.SH - 30, C.SW, 30))


def _level2_forest(theme):
    """Green forest – layered trees."""
    # Sky gradient (top portion)
    pygame.draw.rect(display.screen, (205, 235, 205), (0, 0, C.SW, C.SH // 2))
    # Ground
    pygame.draw.rect(display.screen, (100, 160, 80),  (0, C.SH - 55, C.SW, 55))
    pygame.draw.rect(display.screen, (80,  135, 60),  (0, C.SH - 28, C.SW, 28))

    # Trees – back row (shorter, darker)
    for tx in range(80, C.SW - 60, 160):
        _tree(tx, C.SH - 55, 28, 60, (70, 115, 60), (110, 160, 80))
    # Trees – front row (taller, brighter)
    for tx in range(160, C.SW - 100, 220):
        _tree(tx, C.SH - 55, 36, 80, (55,  95, 50), (90, 145, 65))


def _tree(cx, base_y, trunk_w, crown_r, trunk_col, leaf_col):
    trunk_h = crown_r
    pygame.draw.rect(display.screen, trunk_col,
                     (cx - trunk_w // 2, base_y - trunk_h, trunk_w, trunk_h))
    pygame.draw.circle(display.screen, leaf_col, (cx, base_y - trunk_h), crown_r)
    pygame.draw.circle(display.screen, tuple(min(255, c + 25) for c in leaf_col),
                       (cx - crown_r // 3, base_y - trunk_h - crown_r // 4), crown_r // 2)


def _level3_desert(theme):
    """Sandy desert – dunes and cacti."""
    # Sky
    pygame.draw.rect(display.screen, (255, 200, 130), (0, 0, C.SW, C.SH // 2))
    # Dunes
    for dx, dy in [(0, C.SH - 90), (250, C.SH - 75), (550, C.SH - 100), (820, C.SH - 80)]:
        pygame.draw.ellipse(display.screen, (220, 190, 130),
                            (dx, dy, 380, 120))
    # Sand floor
    pygame.draw.rect(display.screen, (215, 185, 120), (0, C.SH - 55, C.SW, 55))
    pygame.draw.rect(display.screen, (195, 165, 100), (0, C.SH - 25, C.SW, 25))
    # Sun
    pygame.draw.circle(display.screen, (255, 215, 60), (120, 70), 44)
    # Cacti
    for cx in (200, 520, 800):
        _cactus(cx, C.SH - 55)


def _cactus(cx, base_y):
    col = (60, 140, 60)
    h   = 80
    w   = 18
    # Main trunk
    pygame.draw.rect(display.screen, col, (cx - w//2, base_y - h, w, h))
    # Left arm
    pygame.draw.rect(display.screen, col, (cx - w//2 - 26, base_y - h + 26, 26, 12))
    pygame.draw.rect(display.screen, col, (cx - w//2 - 26, base_y - h + 14, 12, 26))
    # Right arm
    pygame.draw.rect(display.screen, col, (cx + w//2,      base_y - h + 34, 26, 12))
    pygame.draw.rect(display.screen, col, (cx + w//2 + 14, base_y - h + 22, 12, 26))
    # Top round
    pygame.draw.circle(display.screen, col, (cx, base_y - h), w // 2 + 2)


def _level4_cave(theme):
    """Crystal cave – stalactites and glowing gems."""
    # Stone wall texture
    pygame.draw.rect(display.screen, (185, 165, 215), (0, 0, C.SW, C.SH // 3))
    pygame.draw.rect(display.screen, (165, 140, 200), (0, C.SH // 3, C.SW, C.SH // 3))
    pygame.draw.rect(display.screen, (145, 120, 180), (0, 2 * C.SH // 3, C.SW, C.SH // 3))

    # Stalactites from top
    for sx in range(60, C.SW - 40, 90):
        h = 30 + (sx * 7 % 45)
        pygame.draw.polygon(display.screen, (100, 65, 150),
                            [(sx - 14, C.WT), (sx + 14, C.WT), (sx, C.WT + h)])

    # Stalagmites from bottom
    for sx in range(100, C.SW - 60, 120):
        h = 20 + (sx * 5 % 35)
        pygame.draw.polygon(display.screen, (90, 55, 135),
                            [(sx - 12, C.SH - C.WT), (sx + 12, C.SH - C.WT),
                             (sx, C.SH - C.WT - h)])

    # Glowing gem dots
    gem_cols = [(255, 100, 200), (100, 220, 255), (200, 255, 100), (255, 200, 50)]
    for i, (gx, gy) in enumerate([(180, 200), (400, 350), (650, 180), (850, 420),
                                   (300, 480), (750, 320)]):
        col = gem_cols[i % len(gem_cols)]
        pygame.draw.circle(display.screen, col, (gx, gy), 8)
        pygame.draw.circle(display.screen, (255, 255, 255), (gx - 2, gy - 2), 3)


def _level5_ocean(theme):
    """Underwater – gradient depth and bubbles."""
    # Depth gradient bands
    bands = [
        (0,   100, (160, 215, 240)),
        (100, 200, (140, 200, 230)),
        (200, 320, (120, 185, 220)),
        (320, 460, (100, 165, 210)),
        (460, 650, ( 80, 145, 195)),
    ]
    for y1, y2, col in bands:
        pygame.draw.rect(display.screen, col, (0, y1, C.SW, y2 - y1))

    # Sandy seabed
    pygame.draw.rect(display.screen, (195, 180, 130), (0, C.SH - 45, C.SW, 45))
    pygame.draw.rect(display.screen, (175, 160, 110), (0, C.SH - 20, C.SW, 20))

    # Seaweed
    for wx in range(80, C.SW - 40, 110):
        h = 40 + (wx * 3 % 50)
        for seg in range(0, h, 14):
            ox = int(math.sin(seg * 0.5 + wx * 0.1) * 8)
            pygame.draw.ellipse(display.screen, (40, 160, 90),
                                (wx + ox - 7, C.SH - 45 - seg - 14, 14, 18))

    # Bubbles (fixed positions – deterministic)
    for i, (bx, by) in enumerate([(150, 420), (300, 280), (480, 380),
                                   (620, 200), (800, 320), (950, 450),
                                   (200, 180), (700, 460), (550, 130)]):
        r = 6 + (i * 3 % 10)
        pygame.draw.circle(display.screen, (200, 235, 250), (bx, by), r, 2)
        pygame.draw.circle(display.screen, (240, 250, 255), (bx - r//3, by - r//3), r//3)


def _level6_space(theme):
    """Outer space – stars, nebula glow, planet."""
    # Stars (deterministic positions via simple formula)
    for i in range(120):
        sx = (i * 137 + 42)  % C.SW
        sy = (i * 97  + 17)  % C.SH
        br = 160 + (i * 53 % 95)
        r  = 1 + (i % 3 == 0)
        pygame.draw.circle(display.screen, (br, br, br), (sx, sy), r)

    # Nebula blobs
    neb = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
    for nx, ny, nr, nc in [(250, 180, 100, (80, 0, 120, 35)),
                            (700, 400, 130, (0, 60, 120, 30)),
                            (500, 300, 80,  (120, 0, 80, 25))]:
        pygame.draw.circle(neb, nc, (nx, ny), nr)
    display.screen.blit(neb, (0, 0))

    # Planet (right side, partially cut off)
    pygame.draw.circle(display.screen, (80, 50, 140), (980, 180), 90)
    pygame.draw.circle(display.screen, (110, 75, 175), (960, 160), 60)
    # Ring
    pygame.draw.ellipse(display.screen, (140, 100, 200),
                        (880, 152, 200, 55), 4)

    # Distant small moon
    pygame.draw.circle(display.screen, (190, 185, 200), (180, 130), 28)
    pygame.draw.circle(display.screen, (165, 160, 175), (192, 120), 10)
