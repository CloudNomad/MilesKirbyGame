"""
cutscene2.py – Transition cinematic shown between Level 1 and Level 2.

Assets
──────
    assets/cutscene2_bg.png  (or .jpg / .jpeg)  – city / skyline background.
    Falls back to a procedural city-light starfield if no image is found.

Timing
──────
    Background fade-in  :  ~1.0 s
    Typing speed        :  ~30 chars / s
    Pause after typing  :  ~3 s per segment
    Text fade-out       :  ~0.7 s per segment

    Press any key to advance one step; any key during "Press any key" prompt
    moves to the next segment immediately.

Public API
──────────
    reset()             – initialise / re-initialise; call before C.TRANSIT_12
    advance()           – step forward on key/click (same logic as cutscene.py)
    update() -> bool    – advance one frame; returns True when finished
    draw()              – render to display.screen
    done                – True once all segments have played
"""

import os
import random
import math
import pygame

import display
import constants as C

# ── Timing ─────────────────────────────────────────────────────────────────────
_BG_FADE_SPEED   = 4     # bg alpha per frame  (255/4 ≈ 64 f ≈ 1.1 s)
_TYPE_DELAY      = 2     # frames between characters  (30 chars/s at 60 fps)
_PAUSE_FRAMES    = 180   # frames to hold a fully-typed box  (3 s at 60 fps)
_TEXT_FADE_SPEED = 6     # alpha removed per frame during fade-out  (~0.7 s)

# ── Story segments per world transition ─────────────────────────────────────────
_WORLD_SEGMENTS = {
    2: [
        "After their first victory, our heroes pressed onward.\n\n"
        "They had proven themselves worthy — "
        "but the journey was only just beginning.\n\n"
        "Somewhere ahead, a great city was waiting.",

        "They wandered into a sprawling metropolis — tall towers of glass "
        "and steel reaching toward the clouds.\n\n"
        "The streets buzzed with life, color, and mystery.\n\n"
        "This city held secrets that no one had ever uncovered.",

        "Rumor spoke of a hidden artifact — a legendary item said to "
        "hold the knowledge of the stars themselves.\n\n"
        "The adventure continues…",
    ],
    3: [
        "The city faded behind them as our heroes climbed higher.\n\n"
        "Before them rose ancient mountain peaks — snow-capped and silent.\n\n"
        "The air was thin, but their determination was stronger.",

        "Legend told of a wise elder who lived at the summit.\n\n"
        "Only those who could prove their knowledge could seek an audience.\n\n"
        "The climb would test everything they had learned.",

        "Step by step, word by word, they ascended.\n\n"
        "The mountains would reveal their secrets — but only to the worthy.\n\n"
        "The adventure continues…",
    ],
    4: [
        "Beyond the mountains, the land gave way to a glittering coastline.\n\n"
        "Beneath the waves lay a sunken kingdom — ancient and forgotten.\n\n"
        "Our heroes dove deep into the shimmering blue.",

        "Strange creatures swam alongside them in the deep.\n\n"
        "Ruins of a lost civilization stretched across the ocean floor.\n\n"
        "Knowledge had been preserved here for thousands of years.",

        "The ocean held mysteries that the surface world had forgotten.\n\n"
        "But our heroes were ready to learn every one of them.\n\n"
        "The adventure continues…",
    ],
    5: [
        "Rising from the depths, our heroes found themselves lifted skyward.\n\n"
        "Floating islands drifted through golden clouds above the world.\n\n"
        "The sky was alive with color, light, and wonder.",

        "Ancient sky temples floated among the clouds.\n\n"
        "The wind carried whispers of riddles and ancient songs.\n\n"
        "Every step forward unlocked a new layer of understanding.",

        "Above the clouds, all things seemed possible.\n\n"
        "Our heroes soared — armed with knowledge and courage.\n\n"
        "The adventure continues…",
    ],
    6: [
        "At last, the final frontier lay before them — the cosmos itself.\n\n"
        "Stars stretched in every direction, infinite and magnificent.\n\n"
        "One last challenge awaited among the stars.",

        "A great guardian stood at the edge of the galaxy.\n\n"
        "Only those with mastery of language and knowledge could pass.\n\n"
        "Everything had led to this moment.",

        "This was it — the final test of all they had learned.\n\n"
        "With courage in their hearts and words on their lips, they stepped forward.\n\n"
        "The adventure reaches its end…",
    ],
}

_SEGMENTS = _WORLD_SEGMENTS[2]   # active list, set by reset()

# ── Internal state ──────────────────────────────────────────────────────────────
_bg_img      = None   # pygame.Surface or None
_city_lights = []     # procedural fallback: list of (x, y, w, h, col, alpha)
_stars_fall  = []     # small drifting stars for depth

_phase       = 0      # 0=bg_fade  1=typing  2=pause  3=text_fade
_bg_alpha    = 0
_seg_idx     = 0
_char_idx    = 0
_type_timer  = 0
_pause_timer = 0
_text_alpha  = 255
_wrapped     = []
_flat_text   = ""

done         = False


# ── Public ──────────────────────────────────────────────────────────────────────

def reset(to_world: int = 2) -> None:
    """Initialise state.  Call once before entering C.TRANSIT with the destination world (2-6)."""
    global _bg_img, _city_lights, _stars_fall, _SEGMENTS
    global _phase, _bg_alpha, _seg_idx, _char_idx
    global _type_timer, _pause_timer, _text_alpha, _wrapped, _flat_text, done

    # Select story text for this transition
    _SEGMENTS = _WORLD_SEGMENTS.get(to_world, _WORLD_SEGMENTS[2])

    # Try to load a world-specific background image: cutscene{N}_bg.png
    _bg_img = None
    for name in (f"cutscene{to_world}_bg", "cutscene2_bg"):
        for ext in ("png", "jpg", "jpeg"):
            path = os.path.join(os.path.dirname(__file__), "assets", f"{name}.{ext}")
            if os.path.isfile(path):
                try:
                    raw     = pygame.image.load(path).convert()
                    _bg_img = pygame.transform.smoothscale(raw, (C.SW, C.SH))
                    print(f"[cutscene2] Loaded background: {name}.{ext}")
                except pygame.error as e:
                    print(f"[cutscene2] Could not load {name}.{ext}: {e}")
                break
        if _bg_img is not None:
            break

    if _bg_img is None:
        print(f"[cutscene2] No background for world {to_world} — using procedural city skyline.")

    # Procedural city-light fallback
    rng = random.Random(99)

    # Building silhouettes (dark rectangles)
    _city_lights = []
    x = 0
    while x < C.SW:
        bw = rng.randint(40, 110)
        bh = rng.randint(140, 420)
        by = C.SH - bh
        darkness = rng.randint(12, 35)
        _city_lights.append(("building", x, by, bw, bh, (darkness, darkness, darkness + 8)))
        # Windows on each building
        wx = x + 8
        while wx < x + bw - 12:
            wy = by + 16
            while wy < C.SH - 20:
                if rng.random() < 0.55:
                    wc = rng.choice([
                        (255, 240, 160),  # warm yellow
                        (200, 220, 255),  # cool blue-white
                        (255, 180, 80),   # amber
                    ])
                    _city_lights.append(("window", wx, wy, 8, 10, wc))
                wy += 18
            wx += 16
        x += bw + rng.randint(2, 8)

    # Drifting stars / city haze particles
    _stars_fall = [
        (rng.randint(0, C.SW - 1),
         rng.randint(0, C.SH - 1),
         rng.uniform(0.2, 1.2),    # drift speed
         rng.randint(100, 200))    # brightness
        for _ in range(120)
    ]

    _phase        = 0
    _bg_alpha     = 0
    _seg_idx      = 0
    _text_alpha   = 255
    done          = False

    _prepare_segment(0)


def advance() -> None:
    """Step forward on key-press — same logic as the opening cutscene."""
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


def update() -> bool:
    """Advance one frame.  Returns True when finished."""
    global _phase, _bg_alpha, _seg_idx
    global _char_idx, _type_timer, _pause_timer, _text_alpha, done

    if done:
        return True

    # Phase 0 — fade the background in
    if _phase == 0:
        _bg_alpha = min(255, _bg_alpha + _BG_FADE_SPEED)
        if _bg_alpha >= 255:
            _phase = 1

    # Phase 1 — typewriter
    elif _phase == 1:
        _type_timer += 1
        if _type_timer >= _TYPE_DELAY:
            _type_timer = 0
            if _char_idx < len(_flat_text):
                _char_idx += 1
            else:
                _pause_timer = 0
                _phase = 2

    # Phase 2 — hold
    elif _phase == 2:
        _pause_timer += 1
        if _pause_timer >= _PAUSE_FRAMES:
            _phase = 3

    # Phase 3 — fade text out
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

    return done


def draw() -> None:
    """Render the transition cutscene onto display.screen."""
    scr   = display.screen
    ticks = pygame.time.get_ticks()

    scr.fill((5, 8, 20))   # night-sky base

    # ── Background ──────────────────────────────────────────────────────────
    if _bg_alpha > 0:
        if _bg_img is not None:
            scr.blit(_bg_img, (0, 0))
            ov = pygame.Surface((C.SW, C.SH))
            ov.fill((0, 0, 0))
            ov.set_alpha(255 - _bg_alpha)
            scr.blit(ov, (0, 0))
        else:
            _draw_city(scr, ticks)

    # ── Text box ─────────────────────────────────────────────────────────────
    if _phase >= 1 and _text_alpha > 0 and _flat_text:
        _draw_textbox(scr, _text_alpha)

    # ── Skip hint ─────────────────────────────────────────────────────────────
    if _bg_alpha > 100:
        hint_alpha = min(150, _bg_alpha - 100)
        hint = display.f_xs.render("Press any key to advance", True, (160, 160, 160))
        hint.set_alpha(hint_alpha)
        scr.blit(hint, (C.SW - hint.get_width() - 14, C.SH - 18))


# ── Internal helpers ────────────────────────────────────────────────────────────

def _prepare_segment(idx: int) -> None:
    global _wrapped, _flat_text, _char_idx, _type_timer
    font      = display.f_med
    box_pad   = 24
    box_x     = 40
    text_w    = C.SW - (box_x * 2) - (box_pad * 2)
    _wrapped  = _word_wrap(_SEGMENTS[idx], font, text_w)
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


def _draw_city(scr: pygame.Surface, ticks: int) -> None:
    """Draw the procedural night-city skyline scaled to _bg_alpha."""
    factor = _bg_alpha / 255

    # Sky gradient — deep indigo at top, dark blue at horizon
    for y in range(C.SH):
        t  = y / C.SH
        r  = int((8  + t * 12)  * factor)
        g  = int((10 + t * 18)  * factor)
        b  = int((35 + t * 25)  * factor)
        pygame.draw.line(scr, (r, g, b), (0, y), (C.SW, y))

    # Moon — soft white circle upper-right
    mx, my = int(C.SW * 0.82), int(C.SH * 0.18)
    mr = 38
    moon_surf = pygame.Surface((mr * 2, mr * 2), pygame.SRCALPHA)
    pygame.draw.circle(moon_surf, (240, 240, 220, int(220 * factor)),
                       (mr, mr), mr)
    pygame.draw.circle(moon_surf, (255, 255, 240, int(80 * factor)),
                       (mr, mr), mr + 10)
    scr.blit(moon_surf, (mx - mr, my - mr))

    # Atmosphere glow around moon
    glow = pygame.Surface((mr * 6, mr * 6), pygame.SRCALPHA)
    pygame.draw.circle(glow, (180, 180, 220, int(18 * factor)),
                       (mr * 3, mr * 3), mr * 3)
    scr.blit(glow, (mx - mr * 3, my - mr * 3))

    # Buildings and windows
    win_pulse = 0.85 + 0.15 * math.sin(ticks * 0.001)   # subtle window flicker
    for item in _city_lights:
        kind = item[0]
        if kind == "building":
            _, x, y, w, h, col = item
            c = tuple(int(v * factor) for v in col)
            pygame.draw.rect(scr, c, (x, y, w, h))
        else:
            _, x, y, w, h, col = item
            a = int(min(255, col[0] * win_pulse) * factor)
            ws = pygame.Surface((w, h), pygame.SRCALPHA)
            ws.fill((col[0], col[1], col[2], a))
            scr.blit(ws, (x, y))

    # Drifting haze particles (slow vertical drift)
    t_sec = ticks / 1000.0
    for i, (px, py, spd, bright) in enumerate(_stars_fall):
        ny  = int((py + t_sec * spd * 8) % C.SH)
        c   = int(bright * factor)
        if ny < int(C.SH * 0.55):   # only in the sky portion
            pygame.draw.circle(scr, (c, c, c + 20), (px, ny), 1)


def _draw_textbox(scr: pygame.Surface, alpha: int) -> None:
    font   = display.f_med
    pad    = 24
    box_x  = 40
    box_w  = C.SW - (box_x * 2)
    lh     = font.get_linesize() + 4

    vis_lines = _flat_text[:_char_idx].split("\n")

    box_h = pad * 2 + lh * len(_wrapped)
    box_y = C.SH - box_h - 34

    # Panel — warmer tint than the opening (amber/brown accent for the city)
    panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    panel.fill((15, 8, 0, int(215 * alpha / 255)))
    pygame.draw.rect(
        panel,
        (220, 160, 60, int(200 * alpha / 255)),
        panel.get_rect(), 2, border_radius=8,
    )
    scr.blit(panel, (box_x, box_y))

    ty = box_y + pad
    for line in vis_lines:
        if line == "":
            ty += lh
            continue
        surf = font.render(line, True, (255, 235, 190))
        surf.set_alpha(alpha)
        scr.blit(surf, (box_x + pad, ty))
        ty += lh
