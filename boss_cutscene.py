"""
boss_cutscene.py – Pre-boss cinematic shown after all 5 stages are cleared.

Three typewriter text boxes play over a background image.
On the third box the boss sprite slides in from the right side of the screen.

Assets (all optional — fall back through the list in order):
    assets/boss_bg{lvl}.png   world-specific background
    assets/boss_bg.png        fallback background
    assets/boss{lvl}.png      world-specific boss sprite
    assets/boss.png           fallback boss sprite

Public API
──────────
    reset(lvl)       – init for world number lvl (1-6)
    advance()        – key-press: finish typing / skip pause / next box
    skip()           – jump straight to done
    update() -> bool – advance one frame; True when finished
    draw()           – render onto display.screen
    get_boss_img()   – returns the loaded boss Surface (for use in boss_fight)
    done             – True once all three boxes have played
"""

import os
import sys
import random
import pygame

import display
import constants as C

# ── Timing ─────────────────────────────────────────────────────────────────────
_BG_FADE_SPEED   = 3     # alpha per frame  (≈1.4 s fade)
_TYPE_DELAY      = 2     # frames between characters
_PAUSE_FRAMES    = 220   # hold on fully-typed text (≈3.7 s)
_TEXT_FADE_SPEED = 6     # alpha removed per frame
_BOSS_SLIDE_SPD  = 14    # pixels per frame for slide-in

# ── Script ─────────────────────────────────────────────────────────────────────
_SEGMENTS = [
    "Deep within the ancient ruins our heroes discovered crumbling scrolls — "
    "covered in symbols no living eye had read in a thousand years.\n\n"
    "The words were fragmented... barely legible... but the meaning was unmistakable.\n\n"
    "Something immensely powerful had once called this place home.",

    "A low vibration rumbled through the stone floor.\n\n"
    "The torches flickered. The air turned cold and heavy — like the breath "
    "of something vast and ancient stirring from a very long sleep.\n\n"
    "There was a rustling in the darkness. Then silence. Then... a sound.",

    "From the depths emerged an Earth Spirit — "
    "a towering guardian of ancient rock and forgotten fury.\n\n"
    "It had protected this knowledge for a thousand years "
    "and would not yield it without a fight.\n\n"
    "Our heroes steadied themselves... and got ready for combat.",
]

# ── State ──────────────────────────────────────────────────────────────────────
_bg_img        = None
_boss_img      = None
_boss_x        = 0
_boss_target_x = 0
_boss_sliding  = False
_stars: list   = []

_phase         = 0
_bg_alpha      = 0
_seg_idx       = 0
_char_idx      = 0
_type_timer    = 0
_pause_timer   = 0
_text_alpha    = 255
_wrapped: list = []
_flat_text     = ""

done = False

_BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


# ── Public ─────────────────────────────────────────────────────────────────────

def reset(lvl: int) -> None:
    global _bg_img, _boss_img, _boss_x, _boss_target_x, _boss_sliding
    global _stars, _phase, _bg_alpha, _seg_idx, _char_idx
    global _type_timer, _pause_timer, _text_alpha, _wrapped, _flat_text, done

    # Background
    _bg_img = None
    for fname in (f"boss_bg{lvl}.png", "boss_bg.png",
                  f"boss_bg{lvl}.jpg", "boss_bg.jpg"):
        path = os.path.join(_BASE_DIR, "assets", fname)
        if os.path.isfile(path):
            try:
                raw     = pygame.image.load(path).convert()
                _bg_img = pygame.transform.smoothscale(raw, (C.SW, C.SH))
                print(f"[boss_cutscene] Background: {fname}")
            except pygame.error:
                pass
            break

    if _bg_img is None:
        print("[boss_cutscene] No background found — using procedural starfield.")

    # Boss sprite — scale to ≈70 % of screen height, preserve aspect
    _boss_img = None
    boss_h    = int(C.SH * 0.72)
    for fname in (f"boss{lvl}.png", "boss.png"):
        path = os.path.join(_BASE_DIR, "assets", fname)
        if os.path.isfile(path):
            try:
                raw  = pygame.image.load(path).convert_alpha()
                ow, oh = raw.get_size()
                bw   = max(1, int(ow * boss_h / oh))
                _boss_img = pygame.transform.smoothscale(raw, (bw, boss_h))
                print(f"[boss_cutscene] Boss sprite: {fname}")
            except pygame.error:
                pass
            break

    bw             = _boss_img.get_width() if _boss_img else 200
    _boss_target_x = C.SW - bw - 20
    _boss_x        = C.SW           # start fully off-screen right
    _boss_sliding  = False

    random.seed(55)
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
        if _seg_idx >= len(_SEGMENTS):
            done = True
        else:
            _prepare_segment(_seg_idx)
            _text_alpha = 255
            _phase      = 1


def skip() -> None:
    global done
    done = True


def update() -> bool:
    global _phase, _bg_alpha, _boss_x, _boss_sliding
    global _char_idx, _type_timer, _pause_timer, _text_alpha, _seg_idx, done

    if done:
        return True

    if _phase == 0:
        _bg_alpha = min(255, _bg_alpha + _BG_FADE_SPEED)
        if _bg_alpha >= 255:
            _phase = 1

    elif _phase == 1:
        if _seg_idx == 2 and not _boss_sliding:
            _boss_sliding = True

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
            if _seg_idx >= len(_SEGMENTS):
                done = True
            else:
                _prepare_segment(_seg_idx)
                _text_alpha = 255
                _phase      = 1

    if _boss_sliding and _boss_x > _boss_target_x:
        _boss_x = max(_boss_target_x, _boss_x - _BOSS_SLIDE_SPD)

    return done


def draw() -> None:
    scr = display.screen
    scr.fill((0, 0, 0))

    if _bg_alpha > 0:
        if _bg_img is not None:
            scr.blit(_bg_img, (0, 0))
            ov = pygame.Surface((C.SW, C.SH))
            ov.fill((0, 0, 0))
            ov.set_alpha(255 - _bg_alpha)
            scr.blit(ov, (0, 0))
        else:
            _draw_stars(scr, _bg_alpha)

    if _boss_sliding and _boss_img:
        by = C.SH - _boss_img.get_height()
        scr.blit(_boss_img, (_boss_x, by))

    if _phase >= 1 and _text_alpha > 0 and _flat_text:
        _draw_textbox(scr, _text_alpha)

    if _bg_alpha > 120:
        hint_alpha = min(160, _bg_alpha - 120)
        hint = display.f_xs.render("Press any key to advance", True, (160, 160, 160))
        hint.set_alpha(hint_alpha)
        scr.blit(hint, (C.SW - hint.get_width() - 14, C.SH - 18))


def get_boss_img() -> pygame.Surface | None:
    """Return the loaded+scaled boss Surface so boss_fight can reuse it."""
    return _boss_img


# ── Internal ───────────────────────────────────────────────────────────────────

def _prepare_segment(idx: int) -> None:
    global _wrapped, _flat_text, _char_idx, _type_timer
    font       = display.f_med
    pad        = 24
    box_x      = 40
    text_w     = C.SW - (box_x * 2) - (pad * 2)
    _wrapped   = _word_wrap(_SEGMENTS[idx], font, text_w)
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
    panel.fill((10, 0, 20, int(220 * alpha / 255)))
    pygame.draw.rect(
        panel,
        (180, 60, 255, int(220 * alpha / 255)),
        panel.get_rect(), 2, border_radius=8,
    )
    scr.blit(panel, (box_x, box_y))

    ty = box_y + pad
    for line in vis_lines:
        if line == "":
            ty += lh
            continue
        surf = font.render(line, True, (235, 215, 255))
        surf.set_alpha(alpha)
        scr.blit(surf, (box_x + pad, ty))
        ty += lh
