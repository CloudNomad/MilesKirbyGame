"""
player.py – Player class (Kirby-style, free 4-directional sliding, no jump).
Uses assets/kirby.png when available; falls back to procedural drawing.
"""
import math
import pygame
import display
import constants as C
import assets


class Player:
    def __init__(self, x: float, y: float, character: str = "kirby"):
        self.x         = float(x)
        self.y         = float(y)
        self.vx        = 0.0
        self.vy        = 0.0
        self.t         = 0          # animation timer
        self.lives     = 3
        self.keys      = []         # door numbers for collected keys
        self.push_cd   = 0          # frames of push-back (input suppressed)
        self.character = character  # "kirby" or "miles"

    @property
    def r(self) -> pygame.Rect:
        return pygame.Rect(int(self.x) - C.PR, int(self.y) - C.PR,
                           C.PR * 2, C.PR * 2)

    def update(self):
        self.t += 1
        if self.push_cd > 0:
            self.vx  *= 0.80
            self.vy  *= 0.80
            self.push_cd -= 1
        self.x += self.vx
        self.y += self.vy
        # Clamp to full screen bounds
        self.x = max(C.PR,       min(C.SW - C.PR, self.x))
        self.y = max(C.PR,       min(C.SH - C.PR, self.y))

    def push(self, door) -> None:
        """Bounce the player away from a door based on which wall it's in."""
        if door.side == "top":
            self.y   = float(door.y + C.DH + C.PR + 6)
            self.vx  = 0;  self.vy = 7
        elif door.side == "bottom":
            self.y   = float(door.y - C.PR - 6)
            self.vx  = 0;  self.vy = -7
        elif door.side == "right":
            self.x   = float(door.x - C.PR - 6)
            self.vx  = -7; self.vy = 0
        self.push_cd = 24

    def draw(self):
        x, y = int(self.x), int(self.y)

        if self.character == "miles":
            if assets.miles_img:
                rect = assets.miles_img.get_rect(center=(x, y))
                display.screen.blit(assets.miles_img, rect)
            else:
                self._draw_miles(x, y)
        else:
            if assets.player_img:
                rect = assets.player_img.get_rect(center=(x, y))
                display.screen.blit(assets.player_img, rect)
            else:
                self._draw_kirby(x, y)

    def _draw_kirby(self, x: int, y: int):
        moving = math.hypot(self.vx, self.vy) > 0.5
        bob    = int(math.sin(self.t * 0.25) * 2) if moving else 0
        R      = C.PR

        # Shadow
        pygame.draw.ellipse(display.screen, (130, 130, 130),
                            (x - R + 2, y + R - 8, R * 2 - 4, 12))

        # Body
        pygame.draw.circle(display.screen, C.HOTPNK, (x, y + bob), R)
        pygame.draw.circle(display.screen, C.PINK,   (x, y + bob), R, 2)

        # Cheek blush
        pygame.draw.ellipse(display.screen, (255, 118, 142),
                            (x - R + 4,  y + bob + 6, 15, 9))
        pygame.draw.ellipse(display.screen, (255, 118, 142),
                            (x + R - 19, y + bob + 6, 15, 9))

        # Eyes
        for ex in (x - 16, x + 4):
            pygame.draw.ellipse(display.screen, (38, 14, 58),
                                (ex, y + bob - 14, 13, 9))
            pygame.draw.circle(display.screen, C.WHITE,
                               (ex + 3, y + bob - 12), 2)

        # Mouth
        pygame.draw.ellipse(display.screen, (75, 12, 32),
                            (x - 10, y + bob + 4,  20, 14))
        pygame.draw.ellipse(display.screen, (195, 45, 75),
                            (x -  8, y + bob + 5,  16, 11))

        # Feet
        sw = int(math.sin(self.t * 0.25) * 5) if moving else 0
        pygame.draw.ellipse(display.screen, C.HOTPNK,
                            (x - R + 3,  y + bob + R - 12 + sw, 19, 14))
        pygame.draw.ellipse(display.screen, C.HOTPNK,
                            (x + R - 22, y + bob + R - 12 - sw, 19, 14))

        # Arms
        aw = int(math.sin(self.t * 0.25) * 5) if moving else 0
        pygame.draw.ellipse(display.screen, C.HOTPNK,
                            (x - R - 8, y + bob - 5 + aw, 14, 12))
        pygame.draw.ellipse(display.screen, C.HOTPNK,
                            (x + R - 6, y + bob - 5 - aw, 14, 12))

    def _draw_miles(self, x: int, y: int):
        """Procedural Miles Morales (Spider-Man) sprite."""
        moving = math.hypot(self.vx, self.vy) > 0.5
        bob    = int(math.sin(self.t * 0.25) * 2) if moving else 0
        R      = C.PR
        BLACK  = (10,  10,  10)
        RED    = (200, 20,  20)
        WHITE  = (230, 230, 230)

        # Shadow
        pygame.draw.ellipse(display.screen, (80, 80, 80),
                            (x - R + 4, y + R - 7, R * 2 - 8, 10))

        # Legs
        sw = int(math.sin(self.t * 0.25) * 5) if moving else 0
        pygame.draw.rect(display.screen, BLACK,
                         (x - 12, y + bob + 8,  10, R - 4 + sw))
        pygame.draw.rect(display.screen, BLACK,
                         (x + 2,  y + bob + 8,  10, R - 4 - sw))
        # Boots (red)
        pygame.draw.ellipse(display.screen, RED,
                            (x - 13, y + bob + R - 2 + sw, 13, 8))
        pygame.draw.ellipse(display.screen, RED,
                            (x + 1,  y + bob + R - 2 - sw, 13, 8))

        # Torso
        pygame.draw.rect(display.screen, BLACK,
                         (x - 13, y + bob - 8, 26, 18), border_radius=4)
        # Red chest stripe
        pygame.draw.rect(display.screen, RED,
                         (x - 13, y + bob - 1, 26, 5), border_radius=2)
        # Spider symbol (simple cross)
        pygame.draw.line(display.screen, WHITE,
                         (x, y + bob - 7), (x, y + bob + 4), 2)
        pygame.draw.line(display.screen, WHITE,
                         (x - 5, y + bob - 3), (x + 5, y + bob - 3), 2)

        # Arms
        aw = int(math.sin(self.t * 0.25) * 5) if moving else 0
        pygame.draw.rect(display.screen, BLACK,
                         (x - R + 2, y + bob - 8 + aw, 10, 14), border_radius=3)
        pygame.draw.rect(display.screen, BLACK,
                         (x + R - 12, y + bob - 8 - aw, 10, 14), border_radius=3)

        # Head / mask
        pygame.draw.circle(display.screen, BLACK, (x, y + bob - 18), 13)
        # White eye lenses
        pygame.draw.ellipse(display.screen, WHITE,
                            (x - 12, y + bob - 24, 10, 7))
        pygame.draw.ellipse(display.screen, WHITE,
                            (x + 2,  y + bob - 24, 10, 7))
        # Red accent above eyes
        pygame.draw.line(display.screen, RED,
                         (x - 10, y + bob - 26), (x + 10, y + bob - 26), 2)
