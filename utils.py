"""
utils.py – Shared drawing helper functions.
All functions draw to display.screen; call display.init() before using them.
"""
import display


def txt(text: str, font, color: tuple, x: int, y: int,
        center: bool = False, shadow: bool = False):
    """Render text to display.screen. Returns the blit Rect."""
    if shadow:
        s = font.render(text, True, (0, 0, 0))
        r = s.get_rect(center=(x, y)) if center else s.get_rect(topleft=(x, y))
        display.screen.blit(s, (r.x + 2, r.y + 2))
    s = font.render(text, True, color)
    r = s.get_rect(center=(x, y)) if center else s.get_rect(topleft=(x, y))
    display.screen.blit(s, r)
    return r


def wrap_text(text: str, font, max_w: int) -> list:
    """Split text into lines that each fit within max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_hatch(rect, line_col: tuple, spacing: int = 14, width: int = 2):
    """
    Draw diagonal (\\) hatching clipped to rect – replicates the door style
    in the original concept sketch.
    """
    prev = display.screen.get_clip()
    display.screen.set_clip(rect)
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    import pygame
    for off in range(-h, w + h, spacing):
        pygame.draw.line(display.screen, line_col,
                         (x + off, y), (x + off + h, y + h), width)
    display.screen.set_clip(prev)
