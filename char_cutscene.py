"""
char_cutscene.py – Character intro cutscene shown after grade selection.

Displays a character-specific background with three typewriter text boxes,
then hands off to C.TUTORIAL_PROMPT.

Assets (all optional – fall back through the list in order):
    assets/cutscene_kirby.png  /  cutscene_kirby.jpg
    assets/cutscene_miles.png  /  cutscene_miles.jpg
    assets/cutscene_bg.png     (shared fallback)
    Procedural starfield       (last resort)

Public API
──────────
    reset(char)      – init for "kirby" or "miles"; call before C.CHAR_CUTSCENE
    advance()        – key-press handler: finish typing / skip pause / next box
    skip()           – jump straight to done
    update() -> bool – advance one frame; returns True when finished
    draw()           – render onto display.screen
    done             – True once all three boxes have played
"""

import os
import sys
import random
import pygame

import display
import constants as C

# ── Timing ─────────────────────────────────────────────────────────────────────
_BG_FADE_SPEED   = 3    # alpha added per frame  (255/3 ≈ 85 f ≈ 1.4 s)
_TYPE_DELAY      = 2    # frames between characters  (~30 chars/s at 60 fps)
_PAUSE_FRAMES    = 180  # frames to hold fully-typed text  (3 s)
_TEXT_FADE_SPEED = 6    # alpha removed per frame  (~0.7 s)

# ── Story text ─────────────────────────────────────────────────────────────────
_KIRBY_SEGMENTS = [
    "In the peaceful realm of Dream Land, Kirby lived a quiet life — "
    "floating through cotton-candy skies and munching on every treat he could find.\n\n"
    "But Kirby was never just a dreamer. Behind those bright eyes was a curious mind, "
    "always hungry for more than just food.",

    "When strange portals began appearing across Dream Land, "
    "Kirby was the first to investigate.\n\n"
    "Each portal led to a new world filled with puzzles, riddles, and questions "
    "unlike anything Kirby had ever seen.\n\n"
    "The cosmos was calling — and Kirby never backs down from an adventure.",

    "Now it's your turn to help Kirby conquer every challenge that lies ahead.\n\n"
    "From grammar to science, six worlds of learning await.\n\n"
    "Are you ready?  Let's go!",
]

_MILES_SEGMENTS = [
    "Miles Morales juggles a lot. School, friends, family — and a little secret "
    "that keeps the streets of Brooklyn safe at night.\n\n"
    "But even Spider-Man knows that the greatest power isn't the web-shooters. "
    "It's knowledge.",

    "When a series of glowing portals appeared above the city, "
    "Miles swung in to investigate.\n\n"
    "Each one opened into a world of challenges — questions that tested every skill "
    "Miles had ever learned, and some he hadn't discovered yet.\n\n"
    "This was a mission no web could solve.  It required brains.",

    "Now Miles needs your help to conquer six worlds of learning.\n\n"
    "Every correct answer brings him one step closer to proving that "
    "education is the greatest superpower of all.\n\n"
    "Let's do this — together.",
]

# ── Internal state ─────────────────────────────────────────────────────────────
_bg_img      = None
_stars: list = []
_segments    = _KIRBY_SEGMENTS

_phase       = 0    # 0=bg_fade  1=typing  2=pause  3=text_fade
_bg_alpha    = 0
_seg_idx     = 0
_char_idx    = 0
_type_timer  = 0
_pause_timer = 0
_text_alpha  = 255
_wrapped: list = []
_flat_text   = ""

done = False

_BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


# ── Public ─────────────────────────────────────────────────────────────────────

def reset(char: str) -> None:
    global _bg_img, _stars, _segments, _phase, _bg_alpha
    global _seg_idx, _char_idx, _type_timer, _pause_timer
    global _text_alpha, _wrapped, _flat_text, done

    _segments = _MILES_SEGMENTS if char == "miles" else _KIRBY_SEGMENTS

    _bg_img = None
    for fname in (f"cutscene_{char}.png", f"cutscene_{char}.jpg",
                  "cutscene_bg.png", "cutscene_bg.jpg"):
        path = os.path.join(_BASE_DIR, "assets", fname)
        if os.path.isfile(path):
            try:
                raw     = pygame.image.load(path).convert()
                _bg_img = pygame.transform.smoothscale(raw, (C.SW, C.SH))
                print(f"[char_cutscene] Loaded background: {fname}")
            except pygame.error as e:
                print(f"[char_cutscene] Could not load {fname}: {e}")
            break

    if _bg_img is None:
        print("[char_cutscene] No background image found — using procedural starfield.")

    random.seed(77)
    _stars = [
        (random.randint(0, C.SW - 1),
         random.randint(0, C.SH - 1),
         random.randint(1, 3),
         random.randint(140, 255))
        for _ in range(280)
    ]
    random.seed()

    _phase       = 0
    _bg_alpha    = 0
    _seg_idx     = 0
    _text_alpha  = 255
    done         = False

    _prepare_segment(0)


def advance() -> None:
    """Called on any key press during the cutscene."""
    global _phase, _char_idx, _pause_timer, _text_alpha, _seg_idx, done

    if _phase == 1:
        _char_idx    = len(_flat_text)
        _pause_timer = 0
        _phase       = 2
    elif _phase == 2:
        _phase = 3
    elif _phase == 3:
        _text_alpha = 0
        _seg_idx   += 1
        if _seg_idx >= len(_segments):
            done = True
        else:
            _prepare_segment(_seg_idx)
            _text_alpha = 255
            _phase      = 1


def skip() -> None:
    global done
    done = True


def update() -> bool:
    global _phase, _bg_alpha, _seg_idx
    global _char_idx, _type_timer, _pause_timer, _text_alpha, done

    if done:
        return True

    if _phase == 0:
        _bg_alpha = min(255, _bg_alpha + _BG_FADE_SPEED)
        if _bg_alpha >= 255:
            _phase = 1

    elif _phase == 1:
        _type_timer += 1
        if _type_timer >= _TYPE_DELAY:
            _type_timer = 0
            if _char_idx < len(_flat_text):
                _char_idx += 1
            else:
                _pause_timer = 0
                _phase       = 2

    elif _phase == 2:
        _pause_timer += 1
        if _pause_timer >= _PAUSE_FRAMES:
            _phase = 3

    elif _phase == 3:
        _text_alpha = max(0, _text_alpha - _TEXT_FADE_SPEED)
        if _text_alpha <= 0:
            _seg_idx += 1
            if _seg_idx >= len(_segments):
                done = True
            else:
                _prepare_segment(_seg_idx)
                _text_alpha = 255
                _phase      = 1

    return done


def draw() -> None:
    scr = display.screen
    scr.fill((0, 0, 0))

    if _bg_alpha > 0:
        if _bg_img is not None:
            scr.blit(_bg_img, (0, 0))
            overlay = pygame.Surface((C.SW, C.SH))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - _bg_alpha)
            scr.blit(overlay, (0, 0))
        else:
            _draw_stars(scr, _bg_alpha)

    if _phase >= 1 and _text_alpha > 0 and _flat_text:
        _draw_textbox(scr, _text_alpha)

    if _bg_alpha > 120:
        hint_alpha = min(160, _bg_alpha - 120)
        hint = display.f_xs.render("Press any key to advance", True, (160, 160, 160))
        hint.set_alpha(hint_alpha)
        scr.blit(hint, (C.SW - hint.get_width() - 14, C.SH - 18))


# ── Internal helpers ───────────────────────────────────────────────────────────

def _prepare_segment(idx: int) -> None:
    global _wrapped, _flat_text, _char_idx, _type_timer
    font       = display.f_med
    pad        = 24
    box_x      = 40
    text_w     = C.SW - (box_x * 2) - (pad * 2)
    _wrapped   = _word_wrap(_segments[idx], font, text_w)
    _flat_text = "\n".join(_wrapped)
    _char_idx  = 0
    _type_timer = 0


def _word_wrap(text: str, font, max_w: int) -> list:
    lines = []
    for paragraph in text.split("\n"):
        if paragraph == "":
            lines.append("")
            continue
        words, current = paragraph.split(" "), ""
        for word in words:
            test = (current + " " + word).strip()
            if font.size(test)[0] <= max_w:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def _draw_stars(scr: pygame.Surface, alpha: int) -> None:
    factor = alpha / 255
    for x, y, r, brightness in _stars:
        c = int(brightness * factor)
        pygame.draw.circle(scr, (c, c, c), (x, y), r)


def _draw_textbox(scr: pygame.Surface, alpha: int) -> None:
    font  = display.f_med
    pad   = 24
    box_x = 40
    box_w = C.SW - (box_x * 2)
    lh    = font.get_linesize() + 4

    vis_lines = _flat_text[:_char_idx].split("\n")
    box_h = pad * 2 + lh * len(_wrapped)
    box_y = C.SH - box_h - 34

    panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    panel.fill((0, 0, 15, int(210 * alpha / 255)))
    pygame.draw.rect(
        panel,
        (80, 140, 255, int(200 * alpha / 255)),
        panel.get_rect(), 2, border_radius=8,
    )
    scr.blit(panel, (box_x, box_y))

    ty = box_y + pad
    for line in vis_lines:
        if line == "":
            ty += lh
            continue
        surf = font.render(line, True, (220, 230, 255))
        surf.set_alpha(alpha)
        scr.blit(surf, (box_x + pad, ty))
        ty += lh
