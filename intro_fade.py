"""
intro_fade.py – Two-phase pre-opening sequence.

  Phase 1 — text  : five phrases fade in one-by-one on a nature background.
  Phase 2 — video : assets/intro.mp4 plays inside the pygame window via VLC,
                    with full audio and native frame rate.

Requirements for video phase
─────────────────────────────
  1.  pip install python-vlc
  2.  Install VLC media player  →  https://www.videolan.org/vlc/

  VLC embeds a child window inside pygame's window, so rendering never
  conflicts.  Audio is handled entirely by VLC – no separate codec needed.

Public API
──────────
  reset()          – initialise; call once before C.INTRO_FADE
  advance()        – advance text one step, or skip video on key-press
  update() → bool  – drive state machine; returns True when done
  draw()           – render onto display.screen
  done             – True once both phases are complete
"""

import os
import sys
import math
import random
import pygame

import display
import constants as C

# ── VLC ──────────────────────────────────────────────────────────────────────────
try:
    import vlc as _vlc
    _VLC = True
except (ImportError, OSError):
    _vlc  = None
    _VLC  = False

# ── Text content ────────────────────────────────────────────────────────────────
_PHRASES = [
    "It was a lovely and peaceful day....",
    "It seemed humanity achieved world peace...",
    "The animals played together and the flowers bloomed...",
    "Nature and all life living in harmony...",
    "When suddenly...",
]

# ── Text timing (ms) ─────────────────────────────────────────────────────────────
_FADE_IN_MS   = 1000
_HOLD_MS      = 2500
_FADE_OUT_MS  = 800
_LAST_HOLD_MS = 3200
_FLASH_MS     = 700

# ── Internal state ───────────────────────────────────────────────────────────────
_mode            = "text"      # "text"  |  "video"

# — text phase —
_phrase_idx      = 0
_phrase_start_ms = 0
_phase           = "fade_in"   # fade_in | hold | fade_out | flash

# — video phase (VLC) —
_vlc_instance    = None
_vlc_player      = None
_vlc_started     = False       # True once VLC reports State.Playing
_video_path      = ""

# — pre-baked drawing resources —
_bg_surf         = None
_particle_surfs  = []
_particles       = []

done             = False


# ── Public ───────────────────────────────────────────────────────────────────────

def reset() -> None:
    global _mode, _phrase_idx, _phrase_start_ms, _phase
    global _vlc_instance, _vlc_player, _vlc_started
    global _bg_surf, _particle_surfs, _particles, done, _video_path

    _stop_vlc()

    _mode            = "text"
    _phrase_idx      = 0
    _phrase_start_ms = pygame.time.get_ticks()
    _phase           = "fade_in"
    _vlc_started     = False
    done             = False

    _video_path = os.path.join(os.path.dirname(__file__), "assets", "intro.mp4")

    if not _VLC:
        print("[intro_fade] python-vlc not found.  Run:  pip install python-vlc")
        print("[intro_fade] Also ensure VLC media player is installed.")
    elif not os.path.isfile(_video_path):
        print(f"[intro_fade] intro.mp4 not found at: {_video_path}")

    _prebake_bg()
    _build_particles()


def advance() -> None:
    """Step forward one phase on key-press."""
    global _mode, _phase, _phrase_idx, _phrase_start_ms, done

    if _mode == "video":
        _stop_vlc()
        done = True
        return

    now     = pygame.time.get_ticks()
    is_last = (_phrase_idx == len(_PHRASES) - 1)

    if _phase == "fade_in":
        _phrase_start_ms = now - _FADE_IN_MS
        _phase = "hold"
    elif _phase == "hold":
        hold = _LAST_HOLD_MS if is_last else _HOLD_MS
        _phrase_start_ms = now - _FADE_IN_MS - hold
        _phase = "flash" if is_last else "fade_out"
    elif _phase == "fade_out":
        _phrase_idx += 1
        if _phrase_idx >= len(_PHRASES):
            _begin_video()
        else:
            _phrase_start_ms = now
            _phase = "fade_in"
    elif _phase == "flash":
        _begin_video()


def update() -> bool:
    global _phase, _phrase_idx, _phrase_start_ms, _vlc_started, done

    if done:
        return True

    now     = pygame.time.get_ticks()
    t       = now - _phrase_start_ms
    is_last = (_phrase_idx == len(_PHRASES) - 1)

    # ── Text phase ────────────────────────────────────────────────────────────
    if _mode == "text":
        if _phase == "fade_in":
            if t >= _FADE_IN_MS:
                _phase = "hold"
        elif _phase == "hold":
            hold = _LAST_HOLD_MS if is_last else _HOLD_MS
            if t >= _FADE_IN_MS + hold:
                _phase = "flash" if is_last else "fade_out"
        elif _phase == "fade_out":
            if t >= _FADE_IN_MS + _HOLD_MS + _FADE_OUT_MS:
                _phrase_idx += 1
                if _phrase_idx >= len(_PHRASES):
                    _begin_video()
                else:
                    _phrase_start_ms = now
                    _phase = "fade_in"
        elif _phase == "flash":
            if t - _FADE_IN_MS - _LAST_HOLD_MS >= _FLASH_MS:
                _begin_video()

    # ── Video phase ───────────────────────────────────────────────────────────
    elif _mode == "video":
        if _vlc_player is not None:
            state = _vlc_player.get_state()
            if state == _vlc.State.Playing:
                _vlc_started = True
            # Only mark done once playback has actually started and then ended
            if _vlc_started and state in (
                    _vlc.State.Ended, _vlc.State.Error, _vlc.State.Stopped):
                _stop_vlc()
                done = True
        else:
            # VLC unavailable or failed to open
            done = True

    return done


def draw() -> None:
    scr = display.screen
    now = pygame.time.get_ticks()

    # ── Video phase ───────────────────────────────────────────────────────────
    # VLC renders into a child window it creates inside pygame's HWND.
    # We fill black so nothing from the text phase bleeds through.
    if _mode == "video":
        scr.fill((0, 0, 0))
        return

    # ── Text phase ────────────────────────────────────────────────────────────
    t       = now - _phrase_start_ms
    is_last = (_phrase_idx == len(_PHRASES) - 1)

    if _bg_surf is not None:
        scr.blit(_bg_surf, (0, 0))
    else:
        scr.fill((18, 38, 18))

    _draw_particles(scr, now)

    # Compute phrase alpha
    if _phase == "fade_in":
        alpha = min(255, int(255 * t / max(1, _FADE_IN_MS)))
    elif _phase == "hold":
        alpha = 255
    elif _phase == "fade_out":
        elapsed = t - _FADE_IN_MS - _HOLD_MS
        alpha   = max(0, int(255 * (1 - elapsed / max(1, _FADE_OUT_MS))))
    else:
        alpha = 255   # flash

    if 0 <= _phrase_idx < len(_PHRASES) and alpha > 0:
        phrase = _PHRASES[_phrase_idx]
        if is_last:
            font, tcol, scol = display.f_title, (255, 80, 80), (80, 0, 0)
        else:
            font, tcol, scol = display.f_big, (235, 255, 210), (20, 50, 10)

        shad = font.render(phrase, True, scol)
        surf = font.render(phrase, True, tcol)
        tx   = C.SW // 2 - surf.get_width()  // 2
        ty   = C.SH // 2 - surf.get_height() // 2
        shad.set_alpha(alpha)
        surf.set_alpha(alpha)
        scr.blit(shad, (tx + 3, ty + 3))
        scr.blit(surf, (tx, ty))

    # White flash overlay
    if _phase == "flash":
        raw_t       = t - _FADE_IN_MS - _LAST_HOLD_MS
        flash_alpha = min(255, max(0, int(255 * raw_t / max(1, _FLASH_MS))))
        fl = pygame.Surface((C.SW, C.SH))
        fl.fill((255, 255, 255))
        fl.set_alpha(flash_alpha)
        scr.blit(fl, (0, 0))


# ── Internal ─────────────────────────────────────────────────────────────────────

def _begin_video() -> None:
    """Switch from text phase to VLC video phase."""
    global _mode, _vlc_instance, _vlc_player, _vlc_started, done

    if not _VLC:
        print("[intro_fade] Skipping video – python-vlc not available.")
        done = True
        return

    if not os.path.isfile(_video_path):
        print(f"[intro_fade] Skipping video – file not found: {_video_path}")
        done = True
        return

    try:
        _vlc_instance = _vlc.Instance("--quiet", "--no-video-title-show")
        _vlc_player   = _vlc_instance.media_player_new()
        media         = _vlc_instance.media_new(_video_path)
        _vlc_player.set_media(media)

        # Embed VLC inside the pygame window
        wm = pygame.display.get_wm_info()
        if sys.platform == "win32":
            _vlc_player.set_hwnd(wm["window"])
        elif sys.platform == "darwin":
            _vlc_player.set_nsobject(int(wm.get("nswindow", wm.get("window", 0))))
        else:
            _vlc_player.set_xwindow(wm["window"])

        _vlc_player.play()
        _vlc_started = False
        _mode = "video"
        print("[intro_fade] VLC video started.")

    except Exception as e:
        print(f"[intro_fade] VLC failed to start: {e}")
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


def _prebake_bg() -> None:
    global _bg_surf
    _bg_surf = pygame.Surface((C.SW, C.SH))
    for y in range(C.SH):
        frac = y / C.SH
        r    = int(18 + frac * 30)
        g    = int(38 + frac * 68)
        b    = int(18 + frac * 25)
        pygame.draw.line(_bg_surf, (r, g, b), (0, y), (C.SW, y))
    pygame.draw.rect(_bg_surf, (15, 55, 12),
                     (0, int(C.SH * 0.72), C.SW, C.SH))


def _build_particles() -> None:
    global _particles, _particle_surfs
    rng = random.Random(77)
    _particles      = []
    _particle_surfs = []
    for _ in range(80):
        col = rng.choice([
            (180, 255, 120),
            (255, 240, 140),
            (200, 255, 200),
        ])
        r = rng.randint(2, 5)
        _particles.append({
            "x":     rng.uniform(0, C.SW),
            "y":     rng.uniform(0, C.SH),
            "vx":    rng.uniform(-0.3, 0.3),
            "vy":    rng.uniform(-0.5, -0.1),
            "r":     r,
            "phase": rng.uniform(0, math.tau),
            "col":   col,
        })
        s = pygame.Surface((r * 2, r * 2))
        s.fill((0, 0, 0))
        pygame.draw.circle(s, col, (r, r), r)
        s.set_colorkey((0, 0, 0))
        _particle_surfs.append(s)


def _draw_particles(scr: pygame.Surface, now: int) -> None:
    t_sec = now / 1000.0
    for i, p in enumerate(_particles):
        p["x"] = (p["x"] + p["vx"]) % C.SW
        p["y"] = (p["y"] + p["vy"]) % C.SH
        pulse   = 0.5 + 0.5 * math.sin(t_sec * 2.5 + p["phase"])
        alpha   = int(60 + pulse * 160)
        surf    = _particle_surfs[i]
        surf.set_alpha(alpha)
        scr.blit(surf, (int(p["x"]) - p["r"], int(p["y"]) - p["r"]))
