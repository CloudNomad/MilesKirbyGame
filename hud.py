"""
hud.py – Semi-transparent HUD overlay.
Drawn on top of the stage every frame.

Layout
──────
  Top bar  (always visible):
      left   – Level / Lives / Score / Keys held
      right  – music track name + mute indicator + volume bar

  Save indicator (top-right corner, temporary):
      Spinning gold arc + "Saved" label shown for ~2 s after an autosave.
"""
import math
import pygame
import display
import constants as C
import music
from utils import txt


# ── Volume bar helper ──────────────────────────────────────────────────────────
def _draw_volume_bar(x: int, y: int, w: int = 60, h: int = 8):
    filled = int(w * music.volume())
    pygame.draw.rect(display.screen, C.DKGRAY, (x, y, w, h), border_radius=3)
    if not music.is_muted() and filled:
        pygame.draw.rect(display.screen, C.CYAN, (x, y, filled, h), border_radius=3)
    pygame.draw.rect(display.screen, C.GRAY, (x, y, w, h), border_radius=3, width=1)


# ── Main HUD draw ──────────────────────────────────────────────────────────────
def _draw_star(x: int, y: int, size: int, filled: bool) -> None:
    """Draw a single 5-pointed star centred at (x, y)."""
    import math
    R = size          # outer radius
    r = size * 0.42   # inner radius
    pts = []
    for i in range(10):
        angle  = math.pi / 5 * i - math.pi / 2
        radius = R if i % 2 == 0 else r
        pts.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
    col = C.GOLD if filled else (50, 50, 70)
    pygame.draw.polygon(display.screen, col, pts)
    if filled:
        pygame.draw.polygon(display.screen, (255, 240, 120), pts, 1)


def draw_hud(lvl: int, lives: int, score: int,
             keys_held: list, doors_completed: set, total_stars: int = 0,
             stage: int = 1, save_timer: int = 0):
    """
    lvl             – current world number (1-6)
    lives           – remaining lives
    score           – current score
    keys_held       – list of door numbers for which the player holds a key
    doors_completed – set of door nums answered correctly (e.g. {1, 3})
    total_stars     – accumulated stars earned across all answered questions
    stage           – current stage within the world (1-5)
    """
    # ── Stats bar ─────────────────────────────────────────────────────────────
    bar = pygame.Surface((C.SW, C.HUD_H), pygame.SRCALPHA)
    bar.fill((15, 40, 120, 210))
    display.screen.blit(bar, (0, 0))
    pygame.draw.line(display.screen, C.GOLD, (0, C.HUD_H), (C.SW, C.HUD_H), 2)

    # Left side: game stats
    txt(f"World {lvl}/{C.TOTAL}", display.f_sm, C.GOLD,   12,  12)
    txt(f"Stage {stage}/5",       display.f_sm, C.CYAN,   148,  12)
    txt(f"Lives: {lives}",        display.f_sm, C.RED,    250,  12)
    txt(f"Score: {score}",        display.f_sm, C.YELLOW, 366,  12)
    if keys_held:
        txt("Keys: " + "  ".join(f"D{k}" for k in keys_held),
            display.f_sm, C.GOLD, 500, 12)

    # Stars tally
    if total_stars > 0:
        lbl = display.f_xs.render(f"★ {total_stars}", True, C.GOLD)
        display.screen.blit(lbl, (C.SW // 2 - lbl.get_width() // 2, 9))

    # Right side: music section
    _draw_music_section()

    # Save indicator (drawn last so it sits on top)
    if save_timer > 0:
        _draw_save_indicator(save_timer)


# ── Save indicator ─────────────────────────────────────────────────────────────
_SAVE_TOTAL = 120   # frames the indicator stays visible (= 2 s at 60 fps)

def _draw_save_indicator(timer: int) -> None:
    """Spinning gold arc + 'Saved' label in the top-right corner of the HUD bar."""
    cx = C.SW - 20          # spinner centre x (inside HUD, clear of right edge)
    cy = C.HUD_H // 2       # vertically centred in the HUD bar
    R  = 9                  # outer radius of the arc track

    # Fade out in the last 24 frames
    alpha = 255 if timer > 24 else int(255 * timer / 24)

    # ── Spinner surface (SRCALPHA so we can fade) ──────────────────────────────
    sz   = (R + 3) * 2
    surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
    sc   = R + 3          # centre within the surface
    rect = pygame.Rect(3, 3, R * 2, R * 2)

    # Dim track circle
    pygame.draw.circle(surf, (60, 60, 90, alpha), (sc, sc), R, 2)

    # Spinning arc – 270° gap (leaves a 90° gap so it looks like a spinner)
    speed  = 4.5            # radians per second
    t_sec  = pygame.time.get_ticks() / 1000.0
    start  = (t_sec * speed) % (2 * math.pi)
    span   = math.pi * 1.5  # 270°
    end    = start + span

    gold = (255, 215, 0, alpha)
    # Draw arc; handle 2π wrap with two segments if needed
    if end <= 2 * math.pi:
        pygame.draw.arc(surf, gold, rect, start, end, 3)
    else:
        pygame.draw.arc(surf, gold, rect, start, 2 * math.pi, 3)
        pygame.draw.arc(surf, gold, rect, 0.0, end - 2 * math.pi, 3)

    display.screen.blit(surf, (cx - sc, cy - sc))

    # "Saved" label to the left of the spinner
    lbl  = display.f_xs.render("Saved", True, C.GOLD)
    lbl.set_alpha(alpha)
    display.screen.blit(lbl, (cx - sc - lbl.get_width() - 3, cy - lbl.get_height() // 2))


# ── Music section (top-right of HUD bar) ──────────────────────────────────────
def _draw_music_section():
    right_edge = C.SW - 10

    if not music.has_music():
        txt("No music", display.f_xs, C.GRAY, right_edge, 8, center=False)
        return

    # Key hints
    hints     = "[/] vol   M mute   N/B track"
    hint_surf = display.f_xs.render(hints, True, C.GRAY)
    hx        = right_edge - hint_surf.get_width()
    display.screen.blit(hint_surf, (hx, C.HUD_H - 14))

    # Mute icon + track name
    icon   = "[MUTED]" if music.is_muted() else "~"
    icon_c = C.RED    if music.is_muted() else C.CYAN

    name = music.track_name()
    max_name_px = 260
    while name and display.f_xs.size(name)[0] > max_name_px:
        name = name[:-1]
    if name != music.track_name():
        name += "..."

    track_info = f"{icon}  {music.track_index()+1}/{music.track_count()}  {name}"
    info_surf  = display.f_xs.render(track_info, True, icon_c)
    ix = right_edge - info_surf.get_width()
    display.screen.blit(info_surf, (ix, 8))

    # Volume bar
    bar_w = 60
    bx    = right_edge - bar_w
    _draw_volume_bar(bx, 24, w=bar_w, h=7)

    vol_label = display.f_xs.render(f"{int(music.volume()*100)}%", True, C.LGRAY)
    display.screen.blit(vol_label, (bx - vol_label.get_width() - 4, 22))
