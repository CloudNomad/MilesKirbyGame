"""
cutscene.py – Opening cinematic cutscene shown before the title screen.

Assets
──────
    assets/cutscene_bg.png  (or .jpg / .jpeg)  – galaxy / space background
    If no image is found a procedural deep-space starfield is drawn instead.

Timing (approximate at 60 fps)
──────────────────────────────
    Background fade-in  :  ~1.5 s
    Music fade-in       :  ~2.0 s  (overlaps with bg fade)
    Typing speed        :  ~20 chars / s
    Pause after typing  :  ~4 s per segment
    Text fade-out       :  ~0.7 s per segment
    Total (11 segments) :  ~2 min  (press any key to skip)

Public API
──────────
    reset()             – initialise / re-initialise; call before C.CUTSCENE
    skip()              – end immediately (key-press handler calls this)
    update() -> bool    – advance one frame; returns True when finished
    draw()              – render to display.screen
    done                – True when the cutscene has ended
"""

import os
import random
import pygame

import display
import constants as C
import music

# ── Timing ─────────────────────────────────────────────────────────────────────
_BG_FADE_SPEED    = 3    # bg alpha added per frame  (255/3 ≈ 85 f ≈ 1.4 s)
_MUSIC_FADE_FRAMES= 120  # frames over which music fades in  (2 s)
_MUSIC_TARGET_VOL = 0.7
_TYPE_DELAY       = 2    # frames between characters  (30 chars/s at 60 fps)
_PAUSE_FRAMES     = 180  # frames to hold fully-typed text  (3 s at 60 fps)
_TEXT_FADE_SPEED  = 6    # text-box alpha removed per frame  (255/6 ≈ 0.7 s)

# ── Story ───────────────────────────────────────────────────────────────────────
_SEGMENTS = [
    "The universe holds so many mysteries.\n\n"
    "Stars and other galaxies expand beyond our imagination, "
    "stretching across distances so vast that the human mind "
    "cannot truly comprehend them.\n\n"
    "Secrets that have never — and perhaps could never — be conceived.",

    "For centuries, we gazed at the night sky in silence.\n\n"
    "We searched. We listened. We sent signals into the dark and "
    "heard nothing in return.\n\n"
    "We began to believe we were alone.",

    "Until recently.\n\n"
    "Mysterious energy waves have begun passing through our galaxy — "
    "moving faster than light, threading through planets and stars "
    "as if the cosmos itself were nothing but air.\n\n"
    "They were not random. They were not natural.\n\n"
    "They were a message.",

    "Initiating contact.\n\n"
    "Every screen on Earth flickered with the same symbol — "
    "a spiral of light against a field of stars.\n\n"
    "Then, in every language at once:\n\n"
    "\"We have watched you grow.  The time has come to learn.\"",

    "Life as we know it is about to change.\n\n"
    "Two heroes have answered the call — Kirby and Miles Morales.\n\n"
    "Armed with courage and curiosity, they will journey through "
    "six worlds to prove that humanity is ready.\n\n"
    "The stars are watching.  Are you ready to learn?",
]

# ── Internal state ──────────────────────────────────────────────────────────────
_bg_img        = None   # pygame.Surface or None
_stars         = []     # list of (x, y, radius, brightness) for fallback

_phase         = 0      # 0=bg_fade  1=typing  2=pause  3=text_fade
_bg_alpha      = 0      # 0=black → 255=fully visible
_music_frame   = 0      # counts up during music fade-in
_seg_idx       = 0      # current segment index
_char_idx      = 0      # characters revealed so far in _flat_text
_type_timer    = 0      # frame counter for _TYPE_DELAY
_pause_timer   = 0      # frame counter for _PAUSE_FRAMES
_text_alpha    = 255    # opacity of text box (255=opaque → 0=gone)
_wrapped       = []     # pre-wrapped lines for current segment
_flat_text     = ""     # '\n'.join(_wrapped); typed character by character

done           = False


# ── Public ──────────────────────────────────────────────────────────────────────

def reset() -> None:
    """Initialise cutscene state.  Call once before entering C.CUTSCENE."""
    global _bg_img, _stars, _phase, _bg_alpha, _music_frame
    global _seg_idx, _char_idx, _type_timer, _pause_timer
    global _text_alpha, _wrapped, _flat_text, done

    # Try to load a galaxy background image
    _bg_img = None
    for ext in ("png", "jpg", "jpeg"):
        path = os.path.join(os.path.dirname(__file__), "assets",
                            f"cutscene_bg.{ext}")
        if os.path.isfile(path):
            try:
                raw     = pygame.image.load(path).convert()
                _bg_img = pygame.transform.smoothscale(raw, (C.SW, C.SH))
                print(f"[cutscene] Loaded background: cutscene_bg.{ext}")
            except pygame.error as e:
                print(f"[cutscene] Could not load cutscene_bg.{ext}: {e}")
            break

    if _bg_img is None:
        print("[cutscene] No cutscene_bg image found — using procedural starfield.")

    # Build a procedural deep-space starfield as fallback
    random.seed(42)
    _stars = [
        (random.randint(0, C.SW - 1),
         random.randint(0, C.SH - 1),
         random.randint(1, 3),
         random.randint(140, 255))
        for _ in range(280)
    ]
    random.seed()

    _phase        = 0
    _bg_alpha     = 0
    _music_frame  = 0
    _seg_idx      = 0
    _text_alpha   = 255
    done          = False

    # Music already started at volume 0 in game.py before assets loaded.
    # Just ensure the volume is reset to 0 in case reset() is called again.
    music.set_volume(0.0)

    _prepare_segment(0)


def skip() -> None:
    """Skip the cutscene entirely (called on ESC — but ESC already quits)."""
    global done
    music.set_volume(_MUSIC_TARGET_VOL)
    done = True


def advance() -> None:
    """
    Called when the player presses any key during the cutscene.
    - Still typing  → finish the current text box instantly.
    - Pausing       → dismiss this box and move to the next.
    - Fading out    → jump immediately to the next segment.
    """
    global _phase, _char_idx, _pause_timer, _text_alpha, _seg_idx, done

    if _phase == 1:
        # Complete typing instantly
        _char_idx   = len(_flat_text)
        _pause_timer = 0
        _phase      = 2

    elif _phase == 2:
        # Skip the pause, start fading out
        _phase = 3

    elif _phase == 3:
        # Jump straight to the next segment
        _text_alpha = 0
        _seg_idx   += 1
        if _seg_idx >= len(_SEGMENTS):
            music.set_volume(_MUSIC_TARGET_VOL)
            done = True
        else:
            _prepare_segment(_seg_idx)
            _text_alpha = 255
            _phase      = 1


def update() -> bool:
    """Advance state by one frame.  Returns True when the cutscene is done."""
    global _phase, _bg_alpha, _music_frame, _seg_idx
    global _char_idx, _type_timer, _pause_timer, _text_alpha, done

    if done:
        return True

    # Phase 0 ── fade background in + fade music in ───────────────────────────
    if _phase == 0:
        _bg_alpha    = min(255, _bg_alpha + _BG_FADE_SPEED)
        _music_frame = min(_MUSIC_FADE_FRAMES, _music_frame + 1)
        vol = _MUSIC_TARGET_VOL * _music_frame / _MUSIC_FADE_FRAMES
        music.set_volume(vol)
        if _bg_alpha >= 255:
            music.set_volume(_MUSIC_TARGET_VOL)
            _phase = 1

    # Phase 1 ── typewriter ───────────────────────────────────────────────────
    elif _phase == 1:
        _type_timer += 1
        if _type_timer >= _TYPE_DELAY:
            _type_timer = 0
            if _char_idx < len(_flat_text):
                _char_idx += 1
            else:
                _pause_timer = 0
                _phase = 2

    # Phase 2 ── hold after fully typed ─────────────────────────────────────
    elif _phase == 2:
        _pause_timer += 1
        if _pause_timer >= _PAUSE_FRAMES:
            _phase = 3

    # Phase 3 ── fade text box out ────────────────────────────────────────────
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
    """Render the cutscene onto display.screen."""
    scr = display.screen
    scr.fill((0, 0, 0))

    # Background
    if _bg_alpha > 0:
        if _bg_img is not None:
            scr.blit(_bg_img, (0, 0))
            # Overlay black to simulate fade-in
            overlay = pygame.Surface((C.SW, C.SH))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - _bg_alpha)
            scr.blit(overlay, (0, 0))
        else:
            _draw_stars(scr, _bg_alpha)

    # Text box
    if _phase >= 1 and _text_alpha > 0 and _flat_text:
        _draw_textbox(scr, _text_alpha)

    # Skip hint (fades in with the background)
    if _bg_alpha > 120:
        hint_alpha = min(160, _bg_alpha - 120)
        hint = display.f_xs.render("Press any key to skip", True, (160, 160, 160))
        hint.set_alpha(hint_alpha)
        scr.blit(hint, (C.SW - hint.get_width() - 14, C.SH - 18))


# ── Internal helpers ────────────────────────────────────────────────────────────

def _prepare_segment(idx: int) -> None:
    global _wrapped, _flat_text, _char_idx, _type_timer
    font       = display.f_med
    box_pad    = 24
    box_x      = 40
    text_w     = C.SW - (box_x * 2) - (box_pad * 2)
    _wrapped   = _word_wrap(_SEGMENTS[idx], font, text_w)
    _flat_text = "\n".join(_wrapped)
    _char_idx  = 0
    _type_timer = 0


def _word_wrap(text: str, font, max_w: int) -> list:
    """Wrap *text* to fit *max_w* pixels.  Explicit \\n creates new paragraphs."""
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
    """Draw the procedural starfield scaled by *alpha*."""
    factor = alpha / 255
    for x, y, r, brightness in _stars:
        c = int(brightness * factor)
        pygame.draw.circle(scr, (c, c, c), (x, y), r)


def _draw_textbox(scr: pygame.Surface, alpha: int) -> None:
    font   = display.f_med
    pad    = 24
    box_x  = 40
    box_w  = C.SW - (box_x * 2)
    lh     = font.get_linesize() + 4

    # Reveal only the typed portion
    vis_lines = _flat_text[:_char_idx].split("\n")

    # Size the box to fit all wrapped lines (stable height, no reflow jitter)
    box_h = pad * 2 + lh * len(_wrapped)
    box_y = C.SH - box_h - 34

    # Semi-transparent panel
    panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    panel.fill((0, 0, 15, int(210 * alpha / 255)))
    # Glowing border
    pygame.draw.rect(
        panel,
        (80, 140, 255, int(200 * alpha / 255)),
        panel.get_rect(), 2, border_radius=8,
    )
    scr.blit(panel, (box_x, box_y))

    # Render visible lines
    ty = box_y + pad
    for line in vis_lines:
        if line == "":
            ty += lh
            continue
        surf = font.render(line, True, (220, 230, 255))
        surf.set_alpha(alpha)
        scr.blit(surf, (box_x + pad, ty))
        ty += lh
