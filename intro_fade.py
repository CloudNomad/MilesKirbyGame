"""
intro_fade.py – Two-phase pre-opening sequence.

  Phase 1 — text  : five sentences fade in one at a time on a black screen,
                    stacking like a poem.  Each sentence fades from black to
                    white slowly.  Once all are visible the screen fades to
                    black before the video begins.

  Phase 2 — video : assets/intro.mp4 plays inside the pygame window via VLC
                    vmem callbacks.  Audio handled natively by VLC.

Requirements
────────────
  pip install python-vlc
  VLC media player must be installed → https://www.videolan.org/vlc/

Public API
──────────
  reset()          – initialise; call once before C.INTRO_FADE
  advance()        – skip to next sentence, or skip video
  update() → bool  – drive state machine; returns True when done
  draw()           – render onto display.screen
  done             – True once both phases are complete
"""

import os
import ctypes
import threading
import pygame

import display
import constants as C

# ── VLC ──────────────────────────────────────────────────────────────────────────
try:
    import vlc as _vlc
    _VLC = True
except (ImportError, OSError):
    _vlc = None
    _VLC = False

# ── Text content ────────────────────────────────────────────────────────────────
_PHRASES = [
    "It was a lovely and peaceful day...",
    "It seemed humanity achieved world peace...",
    "Everyone was happy and the flowers bloomed...",
    "Nature and all life living in harmony...",
    "Then the clouds became dark",
]

# ── Text-phase timing (ms) ────────────────────────────────────────────────────────
_SENTENCE_FADE_MS      = 2400   # how long each sentence fades in from black
_SENTENCE_GAP_MS       = 600    # pause after each sentence finishes fading in
_HOLD_MS               = 2000   # hold all text visible before fading to black
_BLACK_FADE_MS         = 1500   # screen-to-black duration

# ── "dark" fade-out ──────────────────────────────────────────────────────────────
# After the black overlay completes, "dark" remains and fades out on its own.
_DARK_LINGER_MS        = 3000   # "dark" fades from white → invisible over this duration

# ── Video fade-in ────────────────────────────────────────────────────────────────
_VIDEO_FADE_MS    = 2000

# ── Mode ─────────────────────────────────────────────────────────────────────────
_mode             = "text"   # "text" | "video"

# ── Text-phase state ──────────────────────────────────────────────────────────────
_text_phase       = "reveal"   # "reveal" | "hold" | "fade_black" | "dark_fade"
_show_idx         = 0          # index of sentence currently fading in
_sentence_start   = 0          # ticks when _show_idx sentence began fading
_hold_start       = 0
_black_start      = 0
_dark_fade_start  = 0

# Pre-rendered sentence surfaces (built once in reset)
_surfs            = []   # one white Surface per phrase
_dark_surf        = None  # "dark" rendered separately for the linger fade-out
_dark_x_offset    = 0    # pixel x-offset of "dark" within the last sentence surface
_line_height      = 0

# ── Video-phase state ─────────────────────────────────────────────────────────────
_vlc_instance     = None
_vlc_player       = None
_vlc_started      = False
_video_path       = ""
_video_fade_start = 0

_raw_buf          = (ctypes.c_uint8 * (C.SW * C.SH * 4))()
_frame_lock       = threading.Lock()
_frame_ready      = False
_cb_lock          = None
_cb_unlock        = None
_cb_display       = None

done              = False


# ── Public ───────────────────────────────────────────────────────────────────────

def reset() -> None:
    global _mode, _text_phase, _show_idx, _sentence_start
    global _hold_start, _black_start, _dark_fade_start
    global _surfs, _line_height
    global _vlc_instance, _vlc_player, _vlc_started
    global _frame_ready, _video_fade_start, done, _video_path

    _stop_vlc()

    _mode             = "text"
    _text_phase       = "reveal"
    _show_idx         = 0
    _sentence_start   = pygame.time.get_ticks()
    _hold_start       = 0
    _black_start      = 0
    _dark_fade_start  = 0
    _vlc_started      = False
    _frame_ready      = False
    _video_fade_start = 0
    done              = False

    _video_path = os.path.join(os.path.dirname(__file__), "assets", "intro.mp4")
    if not _VLC:
        print("[intro_fade] python-vlc not found.  Run:  pip install python-vlc")
    elif not os.path.isfile(_video_path):
        print(f"[intro_fade] intro.mp4 not found at: {_video_path}")

    _build_surfs()


def advance() -> None:
    """Skip current sentence (or skip video)."""
    global _show_idx, _sentence_start, _text_phase, _hold_start

    if _mode == "video":
        _stop_vlc()
        global done
        done = True
        return

    now = pygame.time.get_ticks()
    if _text_phase == "reveal":
        _show_idx       += 1
        _sentence_start  = now
        if _show_idx >= len(_PHRASES):
            _text_phase  = "hold"
            _hold_start  = now
    elif _text_phase == "dark_fade":
        _begin_video()


def update() -> bool:
    if done:
        return True
    if _mode == "text":
        _update_text()
    elif _mode == "video":
        _update_video()
    return done


def draw() -> None:
    scr = display.screen
    now = pygame.time.get_ticks()

    # ── Video phase ───────────────────────────────────────────────────────────
    if _mode == "video":
        if _frame_ready:
            with _frame_lock:
                try:
                    surf = pygame.image.frombuffer(_raw_buf, (C.SW, C.SH), "RGBA")
                    scr.blit(surf, (0, 0))
                except Exception:
                    scr.fill((0, 0, 0))
        else:
            scr.fill((0, 0, 0))

        if _video_fade_start:
            elapsed = now - _video_fade_start
            fade_a  = max(0, int(255 * (1.0 - elapsed / _VIDEO_FADE_MS)))
            if fade_a > 0:
                ov = pygame.Surface((C.SW, C.SH))
                ov.fill((0, 0, 0))
                ov.set_alpha(fade_a)
                scr.blit(ov, (0, 0))
        return

    # ── Text phase ────────────────────────────────────────────────────────────
    scr.fill((0, 0, 0))

    if not _surfs:
        return

    last_idx = len(_PHRASES) - 1
    total_h  = len(_PHRASES) * _line_height
    start_y  = C.SH // 2 - total_h // 2
    last_y   = start_y + last_idx * _line_height
    # Absolute x where "dark" sits within the centered last sentence
    dark_x   = C.SW // 2 - _surfs[last_idx].get_width() // 2 + _dark_x_offset

    # "dark_fade": screen is black; only the word "dark" remains, fading out.
    if _text_phase == "dark_fade":
        if _dark_surf is not None:
            elapsed    = now - _dark_fade_start
            dark_alpha = max(0, int(255 * (1.0 - elapsed / max(1, _DARK_LINGER_MS))))
            if dark_alpha > 0:
                _dark_surf.set_alpha(dark_alpha)
                scr.blit(_dark_surf, (dark_x, last_y))
        return

    # Normal reveal / hold / fade_black rendering
    for i, surf in enumerate(_surfs):
        y = start_y + i * _line_height

        if i < _show_idx:
            alpha = 255
        elif i == _show_idx and _text_phase == "reveal":
            elapsed = now - _sentence_start
            alpha   = min(255, int(255 * elapsed / max(1, _SENTENCE_FADE_MS)))
        else:
            alpha = 0

        if alpha > 0:
            surf.set_alpha(alpha)
            x = C.SW // 2 - surf.get_width() // 2
            scr.blit(surf, (x, y))

    # Fade-to-black overlay; "dark" is blitted after so it stays on top.
    if _text_phase == "fade_black":
        elapsed = now - _black_start
        black_a = min(255, int(255 * elapsed / max(1, _BLACK_FADE_MS)))
        if black_a > 0:
            ov = pygame.Surface((C.SW, C.SH))
            ov.fill((0, 0, 0))
            ov.set_alpha(black_a)
            scr.blit(ov, (0, 0))
        if _dark_surf is not None:
            _dark_surf.set_alpha(255)
            scr.blit(_dark_surf, (dark_x, last_y))


# ── Internal – text ───────────────────────────────────────────────────────────────

def _update_text() -> None:
    global _text_phase, _show_idx, _sentence_start
    global _hold_start, _black_start, _dark_fade_start

    now = pygame.time.get_ticks()

    if _text_phase == "reveal":
        elapsed = now - _sentence_start
        if elapsed >= _SENTENCE_FADE_MS + _SENTENCE_GAP_MS:
            _show_idx      += 1
            _sentence_start = now
            if _show_idx >= len(_PHRASES):
                _text_phase = "hold"
                _hold_start = now

    elif _text_phase == "hold":
        if now - _hold_start >= _HOLD_MS:
            _text_phase  = "fade_black"
            _black_start = now

    elif _text_phase == "fade_black":
        if now - _black_start >= _BLACK_FADE_MS:
            _text_phase      = "dark_fade"
            _dark_fade_start = now

    elif _text_phase == "dark_fade":
        if now - _dark_fade_start >= _DARK_LINGER_MS:
            _begin_video()


def _build_surfs() -> None:
    global _surfs, _dark_surf, _dark_x_offset, _line_height
    font           = display.f_big
    _line_height   = font.get_linesize() + 12
    _surfs         = [font.render(p, True, (255, 255, 255)) for p in _PHRASES]
    _dark_surf     = font.render("dark", True, (255, 255, 255))
    # Measure where "dark" starts within the last sentence so we can blit it precisely
    prefix         = _PHRASES[-1][: _PHRASES[-1].rfind("dark")]
    _dark_x_offset = font.size(prefix)[0]


# ── Internal – video ──────────────────────────────────────────────────────────────

def _begin_video() -> None:
    global _mode, _vlc_instance, _vlc_player, _vlc_started, done
    global _frame_ready, _video_fade_start
    global _cb_lock, _cb_unlock, _cb_display

    if _mode == "video":
        return

    if not _VLC:
        print("[intro_fade] Skipping video – python-vlc not available.")
        done = True
        return

    if not os.path.isfile(_video_path):
        print(f"[intro_fade] Skipping video – file not found: {_video_path}")
        done = True
        return

    try:
        @_vlc.CallbackDecorators.VideoLockCb
        def lock_cb(_op, planes):
            _frame_lock.acquire()
            planes[0] = ctypes.cast(_raw_buf, ctypes.c_void_p)
            return None

        @_vlc.CallbackDecorators.VideoUnlockCb
        def unlock_cb(_op, _pic, _pl):
            global _frame_ready
            _frame_ready = True
            _frame_lock.release()

        @_vlc.CallbackDecorators.VideoDisplayCb
        def display_cb(_op, _pic):
            pass

        _cb_lock    = lock_cb
        _cb_unlock  = unlock_cb
        _cb_display = display_cb

        _vlc_instance = _vlc.Instance("--quiet", "--no-video-title-show",
                                      "--no-xlib")
        _vlc_player   = _vlc_instance.media_player_new()
        _vlc_player.video_set_callbacks(_cb_lock, _cb_unlock, _cb_display, None)
        _vlc_player.video_set_format("RGBA", C.SW, C.SH, C.SW * 4)

        media = _vlc_instance.media_new(_video_path)
        _vlc_player.set_media(media)
        _vlc_player.play()

        _vlc_started      = False
        _frame_ready      = False
        _video_fade_start = pygame.time.get_ticks()
        _mode             = "video"
        print("[intro_fade] VLC vmem video started.")

    except Exception as e:
        print(f"[intro_fade] VLC failed to start: {e}")
        done = True


def _update_video() -> None:
    global _vlc_started, done
    if _vlc_player is not None:
        state = _vlc_player.get_state()
        if state == _vlc.State.Playing:
            _vlc_started = True
        if _vlc_started and state in (
                _vlc.State.Ended, _vlc.State.Error, _vlc.State.Stopped):
            _stop_vlc()
            done = True
    else:
        done = True


def _stop_vlc() -> None:
    global _vlc_player, _vlc_instance
    if _vlc_player is not None:
        try:
            _vlc_player.stop()
            _vlc_player.release()
        except Exception:
            pass
        _vlc_player = None
    if _vlc_instance is not None:
        try:
            _vlc_instance.release()
        except Exception:
            pass
        _vlc_instance = None
