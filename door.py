"""
door.py – Door class.
Uses assets/door.png (and variants) when available; falls back to procedural.
Three doors are placed at fixed wall positions: top / bottom / right.

Each door has a fixed subject (Grammar / Vocabulary / Science) shown on the door.
When completed (question answered correctly) the door glows green.
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
        """
        x, y    – top-left corner
        num     – door number (1, 2, or 3)
        side    – "top" | "bottom" | "right"
        locked  – whether a key is required to enter
        """
        self.x         = x
        self.y         = y
        self.num       = num
        self.side      = side
        self.locked    = locked
        self.completed = False   # True once question answered correctly
        self.r         = pygame.Rect(x, y, C.DW, C.DH)
        self.t         = 0

        # Subject assigned from DOOR_SUBJECTS in constants
        self.subject   = C.DOOR_SUBJECTS.get(num, {"name": "?", "color": C.GRAY})

    def update(self):
        self.t = (self.t + 2) % 360

    def draw(self):
        # ── Choose sprite (PNG path) ───────────────────────────────────────────
        if self.locked and assets.door_locked_img:
            sprite = assets.door_locked_img
        elif self.completed and assets.door_correct_img:
            sprite = assets.door_correct_img
        elif assets.door_img:
            sprite = assets.door_img
        else:
            sprite = None

        if sprite:
            display.screen.blit(sprite, (self.x, self.y))
        else:
            self._draw_procedural()

        self._draw_labels()

    # ── Procedural fallback ───────────────────────────────────────────────────
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
            # Tint by subject color
            sc     = self.subject["color"]
            border = sc
            face   = tuple(max(0, c - 40) for c in sc)
            hatch  = tuple(max(0, c - 80) for c in sc)

        # Frame
        pygame.draw.rect(display.screen, border,
                         (self.x - 5, self.y - 5, C.DW + 10, C.DH + 10),
                         border_radius=5)
        # Face + hatching
        pygame.draw.rect(display.screen, face, self.r)
        draw_hatch(self.r, hatch, spacing=14, width=2)
        pygame.draw.rect(display.screen, border, self.r, 2)

        # Lock icon
        if self.locked:
            lx = self.x + C.DW // 2 - 10
            ly = self.y + C.DH // 2 - 10
            pygame.draw.rect(display.screen, C.GOLD,
                             (lx, ly + 10, 20, 15), border_radius=3)
            pygame.draw.arc(display.screen, C.GOLD,
                            pygame.Rect(lx + 2, ly, 16, 18), 0, math.pi, 3)

        # Completed checkmark (large "OK" text)
        if self.completed:
            txt("OK", display.f_big, C.GOLD,
                self.x + C.DW // 2, self.y + C.DH // 2 - 10, center=True)

    # ── Shiny text helper ─────────────────────────────────────────────────────
    @staticmethod
    def _shiny_txt(text, font, color, cx, cy):
        """
        Render text centred at (cx, cy) with a shiny layered effect:
          1. Deep shadow   (+3, +3)   — very dark version of color
          2. Outer glow    (+1, +1)   — medium-dark tint
          3. Main text     ( 0,  0)   — full color
          4. Specular high (-1, -1)   — near-white highlight for the shine
        """
        dark    = tuple(max(0,   c - 110) for c in color)
        mid     = tuple(max(0,   c -  60) for c in color)
        bright  = tuple(min(255, c + 120) for c in color)

        for surf, ox, oy in [
            (font.render(text, True, dark),   3,  3),
            (font.render(text, True, mid),    1,  1),
            (font.render(text, True, color),  0,  0),
            (font.render(text, True, bright), -1, -1),
        ]:
            display.screen.blit(surf, (cx - surf.get_width() // 2 + ox,
                                       cy + oy))

    # ── Text labels ──────────────────────────────────────────────────────────
    def _draw_labels(self):
        cx  = self.x + C.DW // 2
        cy  = self.y + C.DH // 2
        sub = self.subject["name"]
        sc  = self.subject["color"]

        if self.side == "top":
            # Label sits below the door, clear of the wall strip
            self._shiny_txt(sub, display.f_big, sc,
                            cx, self.y + C.DH + 14)

        elif self.side == "bottom":
            # Label sits above the door
            surf_h = display.f_big.size(sub)[1]
            self._shiny_txt(sub, display.f_big, sc,
                            cx, self.y - surf_h - 10)

        elif self.side == "right":
            # Label sits to the left of the door
            self._shiny_txt(sub, display.f_big, sc,
                            self.x - 100, cy - 14)
