"""
secret_stage.py – Secret stage portal (left wall) + sparkles.

The background is the caller's responsibility (draw_bg(lvl) first).
This module only owns the portal and its particle effects.

API
    portal_rect   – pygame.Rect used for player collision
    reset()       – call when entering the secret state
    update()      – advance sparkles each frame
    draw_portal() – render portal + sparkles onto display.screen
"""

import random
import math
import pygame
import display
import assets
import constants as C

# Portal flush with the left wall, vertically centred
portal_rect = pygame.Rect(0, (C.SH - C.DH) // 2, C.DW, C.DH)

_CX = C.DW // 2          # portal centre x
_CY = (C.SH - C.DH) // 2 + C.DH // 2   # portal centre y

_MAX = 50
_sparkles: list = []

_COLORS = [
    (255, 255, 120),
    (255, 215,   0),
    (255, 255, 255),
    ( 80, 220, 255),
    (220, 130, 255),
    (255, 140, 200),
]


def _new_sparkle() -> dict:
    angle  = random.uniform(0, math.tau)
    radius = random.uniform(45, 90)
    return {
        "x":   _CX + math.cos(angle) * radius,
        "y":   _CY + math.sin(angle) * radius,
        "vx":  math.cos(angle) * random.uniform(0.2, 0.7),
        "vy":  math.sin(angle) * random.uniform(0.2, 0.7) - random.uniform(0.1, 0.5),
        "life": 0,
        "max":  random.randint(45, 85),
        "col":  random.choice(_COLORS),
        "size": random.randint(3, 7),
    }


def reset() -> None:
    global _sparkles
    _sparkles = [_new_sparkle() for _ in range(_MAX)]


def update() -> None:
    global _sparkles
    for s in _sparkles:
        s["life"] += 1
        s["x"]    += s["vx"]
        s["y"]    += s["vy"]
    _sparkles = [s for s in _sparkles if s["life"] < s["max"]]
    while len(_sparkles) < _MAX:
        _sparkles.append(_new_sparkle())


def draw_background() -> None:
    """Draw the secret area's own background (dark mystical room)."""
    scr = display.screen
    scr.fill((15, 10, 35))
    # Wall strips matching the main stage layout thickness
    pygame.draw.rect(scr, (35, 20, 65), (0, 0,          C.SW, C.WT))
    pygame.draw.rect(scr, (35, 20, 65), (0, C.SH - C.WT, C.SW, C.WT))
    pygame.draw.rect(scr, (25, 12, 50), (0, C.WT - 3,   C.SW, 3))
    pygame.draw.rect(scr, (25, 12, 50), (0, C.SH - C.WT, C.SW, 3))


def draw_portal() -> None:
    scr  = display.screen
    t_ms = pygame.time.get_ticks()

    # Pulsing glow behind the portal
    pulse = 0.5 + 0.5 * math.sin(t_ms / 380.0)
    for radius, base_a in ((85, 16), (68, 32), (52, 52)):
        alpha = int(base_a * (0.7 + 0.3 * pulse))
        glow  = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (160, 80, 255, alpha), (radius, radius), radius)
        scr.blit(glow, (_CX - radius, _CY - radius))

    # Portal sprite (same animated GIF used by regular doors)
    frame = assets.get_portal_frame(0)
    if frame:
        scr.blit(frame, (portal_rect.x, portal_rect.y))
    else:
        pygame.draw.ellipse(scr, (120, 50, 220), portal_rect)
        pygame.draw.ellipse(scr, (200, 140, 255), portal_rect, 3)

    # Sparkle particles
    for s in _sparkles:
        ratio = s["life"] / s["max"]
        alpha = int(255 * (1.0 - ratio))
        size  = max(1, int(s["size"] * (1.0 - ratio * 0.4)))
        r, g, b = s["col"]
        surf  = pygame.Surface((size * 2 + 1, size * 2 + 1), pygame.SRCALPHA)
        pygame.draw.circle(surf, (r, g, b, alpha), (size, size), size)
        scr.blit(surf, (int(s["x"]) - size, int(s["y"]) - size))
        if size >= 4:
            pygame.draw.line(scr, s["col"],
                             (int(s["x"]) - size, int(s["y"])),
                             (int(s["x"]) + size, int(s["y"])), 1)
            pygame.draw.line(scr, s["col"],
                             (int(s["x"]), int(s["y"]) - size),
                             (int(s["x"]), int(s["y"]) + size), 1)
