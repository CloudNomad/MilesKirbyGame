"""
key_item.py – Collectible key that unlocks a specific door.
Keys float/bob in place; the player walks over them to collect.
"""
import math
import pygame
import display
import constants as C
from utils import txt


class KeyItem:
    def __init__(self, x: int, y: int, door_num: int):
        self.x        = x
        self.base_y   = float(y)
        self.y        = float(y)
        self.door_num = door_num
        self.collected = False
        self.t         = 0.0

    @property
    def r(self) -> pygame.Rect:
        return pygame.Rect(self.x - 15, int(self.y) - 15, 30, 30)

    def update(self):
        self.t += 0.04
        self.y = self.base_y + math.sin(self.t) * 8

    def draw(self):
        if self.collected:
            return
        iy = int(self.y)

        # Key bow (round head)
        pygame.draw.circle(display.screen, C.GOLD,   (self.x, iy - 8), 11)
        pygame.draw.circle(display.screen, C.YELLOW, (self.x, iy - 8),  8)
        pygame.draw.circle(display.screen, C.BLACK,  (self.x, iy - 8),  4)

        # Key shaft
        pygame.draw.rect(display.screen, C.GOLD, (self.x - 3, iy + 3,  6, 18))

        # Key teeth
        pygame.draw.rect(display.screen, C.GOLD, (self.x + 1, iy + 9,  8,  4))
        pygame.draw.rect(display.screen, C.GOLD, (self.x + 1, iy + 15, 8,  4))

        # Label
        txt(f"Key {self.door_num}", display.f_xs, C.GOLD,
            self.x, iy + 28, center=True, shadow=True)
