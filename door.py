"""
door.py – Door / portal class.

Renders an animated portal GIF (assets/portal.gif and variants) when available;
falls back to the old static PNG, and finally to fully procedural drawing.

Portal visual layers (back → front)
─────────────────────────────────────
  1. Multi-ring subject-coloured glow  (three translucent ellipses)
  2. Animated portal GIF frame
  3. State overlay:
       locked   → dark veil + padlock icon
       completed → gold shimmer + "✓" label
  4. Subject name label (drawn beside the portal)
"""
import math
import pygame
import display
import constants as C
import assets
from utils import txt, draw_hatch


class Door:
    def __init__(self, x: int, y: int, num: int, side: str,
                 locked: bool = False):
        self.x         = x
        self.y         = y
        self.num       = num
        self.side      = side
        self.locked    = locked
        self.completed = False
        self.r         = pygame.Rect(x, y, C.DW, C.DH)
        self.t         = 0

        self.subject = C.DOOR_SUBJECTS.get(num, {"name": "?", "color": C.GRAY})

    def update(self):
        self.t = (self.t + 2) % 360

    def draw(self):
        if assets.has_portal_gif():
            self._draw_portal()
        elif self._has_static_sprite():
            self._draw_static()
        else:
            self._draw_procedural()

        self._draw_labels()

    # ── Animated portal renderer ───────────────────────────────────────────────

    def _draw_portal(self):
        scr = display.screen
        cx  = self.x + C.DW // 2
        cy  = self.y + C.DH // 2

        # Portals are loaded square (DW×DW); centre them in the DH slot
        _PW = C.DW                          # portal visual width  = DW
        _PH = C.DW                          # portal visual height = DW (square)
        _PX = self.x                        # left edge (full width used)
        _PY = self.y + (C.DH - _PH) // 2   # vertically centred

        # Glow ellipse is centred the same way
        pcx = self.x + _PW // 2
        pcy = _PY    + _PH // 2

        # Choose glow colour and frame based on state
        if self.completed:
            pulse     = abs(math.sin(math.radians(self.t)))
            glow_col  = (int(220 + 35 * pulse), int(180 + 20 * pulse), 0)
            frame     = assets.get_portal_correct_frame(self.num)
        elif self.locked:
            glow_col  = (55, 55, 75)
            frame     = assets.get_portal_locked_frame(self.num)
        else:
            glow_col  = self.subject["color"]
            frame     = assets.get_portal_frame(self.num)

        # ── 1. Multi-ring glow (ellipses centred on the square portal) ────────
        for expand, alpha in ((14, 35), (8, 58), (3, 90)):
            gw = _PW + expand * 2
            gh = _PH + expand * 2
            gs = pygame.Surface((gw, gh), pygame.SRCALPHA)
            pygame.draw.ellipse(gs, (*glow_col, alpha), (0, 0, gw, gh))
            scr.blit(gs, (pcx - gw // 2, pcy - gh // 2))

        # ── 2. Portal GIF frame ───────────────────────────────────────────────
        if frame:
            scr.blit(frame, (_PX, _PY))

        # ── 3. State overlays ─────────────────────────────────────────────────
        if self.locked:
            if not assets.portal_locked_frames:
                veil = pygame.Surface((_PW, _PH), pygame.SRCALPHA)
                veil.fill((0, 0, 0, 145))
                scr.blit(veil, (_PX, _PY))
            self._draw_lock_icon(cx, cy)

        elif self.completed:
            if not assets.portal_correct_frames:
                pulse  = abs(math.sin(math.radians(self.t)))
                a_ring = int(120 + 80 * pulse)
                rs = pygame.Surface((_PW, _PH), pygame.SRCALPHA)
                pygame.draw.ellipse(rs, (255, 220, 0, a_ring), (0, 0, _PW, _PH), 4)
                scr.blit(rs, (_PX, _PY))
            txt("OK", display.f_big, C.GOLD, cx, cy - 10, center=True)

    # ── Static PNG renderer ────────────────────────────────────────────────────

    def _has_static_sprite(self) -> bool:
        return bool(assets.door_img or assets.door_locked_img or assets.door_correct_img)

    def _draw_static(self):
        if self.locked and assets.door_locked_img:
            sprite = assets.door_locked_img
        elif self.completed and assets.door_correct_img:
            sprite = assets.door_correct_img
        elif assets.door_img:
            sprite = assets.door_img
        else:
            self._draw_procedural()
            return
        display.screen.blit(sprite, (self.x, self.y))

    # ── Fully procedural renderer (no assets at all) ───────────────────────────

    def _draw_procedural(self):
        if self.completed:
            pulse  = int(abs(math.sin(math.radians(self.t))) * 55)
            border = C.GOLD
            face   = (35, 145 + pulse, 55)
            hatch  = (18, 72, 28)
        elif self.locked:
            border = C.DKGRAY
            face   = (60, 60, 80)
            hatch  = (40, 40, 55)
        else:
            sc     = self.subject["color"]
            border = sc
            face   = tuple(max(0, c - 40) for c in sc)
            hatch  = tuple(max(0, c - 80) for c in sc)

        pygame.draw.rect(display.screen, border,
                         (self.x - 5, self.y - 5, C.DW + 10, C.DH + 10),
                         border_radius=5)
        pygame.draw.rect(display.screen, face, self.r)
        draw_hatch(self.r, hatch, spacing=14, width=2)
        pygame.draw.rect(display.screen, border, self.r, 2)

        cx = self.x + C.DW // 2
        cy = self.y + C.DH // 2

        if self.locked:
            self._draw_lock_icon(cx, cy)
        if self.completed:
            txt("OK", display.f_big, C.GOLD, cx, cy - 10, center=True)

    # ── Shared icon helpers ────────────────────────────────────────────────────

    def _draw_lock_icon(self, cx: int, cy: int):
        lx = cx - 10
        ly = cy - 10
        pygame.draw.rect(display.screen, C.GOLD,
                         (lx, ly + 10, 20, 15), border_radius=3)
        pygame.draw.arc(display.screen, C.GOLD,
                        pygame.Rect(lx + 2, ly, 16, 18), 0, math.pi, 3)

    # ── Subject label ─────────────────────────────────────────────────────────

    @staticmethod
    def _shiny_txt(text, font, color, cx, cy):
        dark   = tuple(max(0,   c - 110) for c in color)
        mid    = tuple(max(0,   c -  60) for c in color)
        bright = tuple(min(255, c + 120) for c in color)
        for surf, ox, oy in [
            (font.render(text, True, dark),   3,  3),
            (font.render(text, True, mid),    1,  1),
            (font.render(text, True, color),  0,  0),
            (font.render(text, True, bright), -1, -1),
        ]:
            display.screen.blit(surf, (cx - surf.get_width() // 2 + ox, cy + oy))

    def _draw_labels(self):
        cx  = self.x + C.DW // 2
        cy  = self.y + C.DH // 2
        sub = self.subject["name"]
        sc  = self.subject["color"]

        if self.side == "top":
            self._shiny_txt(sub, display.f_big, sc, cx, self.y + C.DH + 14)
        elif self.side == "bottom":
            surf_h = display.f_big.size(sub)[1]
            self._shiny_txt(sub, display.f_big, sc, cx, self.y - surf_h - 10)
        elif self.side == "right":
            self._shiny_txt(sub, display.f_big, sc, self.x - 100, cy - 14)
