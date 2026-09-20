"""
stage_transition.py – Dramatic inter-stage wipe + text animation.

Sequence (total ≈ 2.3 s at 60 fps)
────────────────────────────────────
  Phase 0 – wipe_in   (22 f): 8 horizontal strips slide in alternating left / right
  Phase 1 – text_in   (22 f): "Stage N / 5" swings in from off-screen left with rotation
  Phase 2 – hold      (62 f): text rests centre-screen with slow scale pulse
  Phase 3 – text_out  (18 f): text swings off to the right with fade
  Phase 4 – wipe_out  (22 f): strips slide back out revealing the new stage layout

Public API
──────────
  reset(new_stage)  – initialise; call right after _advance_stage() with the NEW stage number
  update() -> bool  – advance one frame; returns True when finished
  draw()            – render overlay onto display.screen (call after drawing stage content)
  done              – True once complete
"""
import math
import pygame

import display
import constants as C

# ── Timing ────────────────────────────────────────────────────────────────────
_WIPE_IN_F  = 22
_TEXT_IN_F  = 22
_HOLD_F     = 62
_TEXT_OUT_F = 18
_WIPE_OUT_F = 22

_PHASE_LIMITS = (_WIPE_IN_F, _TEXT_IN_F, _HOLD_F, _TEXT_OUT_F, _WIPE_OUT_F)

# ── Visual ────────────────────────────────────────────────────────────────────
_N_STRIPS   = 8
_STRIP_COL  = (18,  12,  58)       # deep indigo fill
_EDGE_COL   = (160, 100, 255)      # purple glow on leading edge
_SEAM_COL   = (55,  30, 110)       # faint line between strips while closed
_TEXT_COL   = (255, 220,  50)      # gold
_SHADOW_COL = (90,  40,   0)       # dark amber shadow

# ── State ─────────────────────────────────────────────────────────────────────
_phase     = 0
_timer     = 0
_stage_num = 1
_font      = None   # loaded lazily

done       = False


# ── Public ────────────────────────────────────────────────────────────────────

def reset(new_stage: int) -> None:
    """Initialise the animation for new_stage (the stage number to display)."""
    global _phase, _timer, _stage_num, done
    _phase     = 0
    _timer     = 0
    _stage_num = new_stage
    done       = False
    _ensure_font()


def update() -> bool:
    """Advance one frame. Returns True when the animation is finished."""
    global _phase, _timer, done

    if done:
        return True

    _timer += 1
    if _timer >= _PHASE_LIMITS[_phase]:
        _timer  = 0
        _phase += 1
        if _phase >= len(_PHASE_LIMITS):
            done = True

    return done


def draw() -> None:
    """Render the transition overlay on top of the already-drawn stage."""
    _draw_strips()
    if 1 <= _phase <= 3:
        _draw_text()


# ── Internals ─────────────────────────────────────────────────────────────────

def _ensure_font() -> None:
    global _font
    if _font is None:
        _font = pygame.font.SysFont("Arial", 76, bold=True)


def _ease_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 2


def _ease_in(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t


def _ease_out_back(t: float) -> float:
    """Slight overshoot, then settles — gives the 'swing in' feel."""
    c1 = 1.70158
    c3 = c1 + 1
    t  = max(0.0, min(1.0, t))
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def _draw_strips() -> None:
    scr     = display.screen
    sw, sh  = C.SW, C.SH
    strip_h = sh // _N_STRIPS

    for i in range(_N_STRIPS):
        sy       = i * strip_h
        sh_strip = strip_h if i < _N_STRIPS - 1 else sh - sy
        from_left = (i % 2 == 0)   # alternate directions

        if _phase == 0:
            t   = _ease_out(_timer / _WIPE_IN_F)
            off = int(sw * t)
            x   = off - sw if from_left else sw - off
        elif _phase == 4:
            t   = _ease_in(_timer / _WIPE_OUT_F)
            off = int(sw * t)
            x   = -off if from_left else off
        else:
            x = 0   # screen fully covered

        pygame.draw.rect(scr, _STRIP_COL, (x, sy, sw, sh_strip))

        # Leading-edge glow (bright line at the advancing front)
        if _phase == 0 and t > 0:
            ex = (x + sw - 5) if from_left else x
            pygame.draw.rect(scr, _EDGE_COL, (ex, sy, 6, sh_strip))
        elif _phase == 4 and t > 0:
            ex = x if from_left else (x + sw - 5)
            pygame.draw.rect(scr, _EDGE_COL, (ex, sy, 6, sh_strip))

    # Subtle seam lines between strips while fully closed
    if _phase in (1, 2, 3):
        for i in range(1, _N_STRIPS):
            y = i * strip_h
            pygame.draw.line(scr, _SEAM_COL, (0, y), (sw, y), 2)


def _draw_text() -> None:
    scr  = display.screen
    sw, sh = C.SW, C.SH

    label     = f"Stage  {_stage_num} / 5"
    base_surf = _font.render(label, True, _TEXT_COL)
    tw, th    = base_surf.get_size()
    cx, cy    = sw // 2, sh // 2

    if _phase == 1:
        raw_t = _timer / _TEXT_IN_F
        t     = _ease_out_back(raw_t)
        # Slide in from left of screen (starts fully off-screen left)
        x_off = int((t - 1.0) * (cx + tw // 2 + 40))
        angle = 22.0 * (1.0 - min(1.0, raw_t * 1.5))
        scale = 0.55 + 0.45 * min(1.0, raw_t * 1.4)
        alpha = int(255 * min(1.0, raw_t * 2.5))

    elif _phase == 2:
        # Gentle heartbeat pulse
        pulse = math.sin(_timer / _HOLD_F * math.pi)
        x_off = 0
        angle = 0.0
        scale = 1.0 + 0.032 * pulse
        alpha = 255

    else:  # phase 3 — swing out to the right
        t     = _ease_in(_timer / _TEXT_OUT_F)
        x_off = int(t * (sw // 2 + tw // 2 + 60))
        angle = -20.0 * t
        scale = 1.0 - 0.15 * t
        alpha = int(255 * (1.0 - t ** 1.5))

    # Build the text surface (scale then rotate)
    surf = base_surf
    if scale != 1.0:
        nsw = max(1, int(tw * scale))
        nsh = max(1, int(th * scale))
        surf = pygame.transform.smoothscale(surf, (nsw, nsh))
    if angle != 0.0:
        surf = pygame.transform.rotate(surf, angle)
    surf.set_alpha(max(0, min(255, alpha)))

    fw, fh = surf.get_size()
    dx = cx - fw // 2 + x_off
    dy = cy - fh // 2

    # Shadow (reuse scaled+rotated shape, shifted 5 px)
    shad = _font.render(label, True, _SHADOW_COL)
    if scale != 1.0:
        shad = pygame.transform.smoothscale(shad,
               (max(1, int(tw * scale)), max(1, int(th * scale))))
    if angle != 0.0:
        shad = pygame.transform.rotate(shad, angle)
    shad.set_alpha(max(0, min(180, alpha - 30)))

    scr.blit(shad, (dx + 5, dy + 5))
    scr.blit(surf,  (dx, dy))
