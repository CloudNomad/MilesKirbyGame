"""
screens.py – Full-screen overlay states: intro, bonus round, level complete,
             game over, and game win.
"""
import math
import pygame
import display
import constants as C
import assets
from utils import txt, wrap_text


def _star_points(cx: float, cy: float, R: float, r: float):
    """Return 10-point polygon for a 5-pointed star centred at (cx, cy)."""
    pts = []
    for i in range(10):
        angle  = math.pi / 5 * i - math.pi / 2
        radius = R if i % 2 == 0 else r
        pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return pts


def _draw_stars(cx: int, cy: int, filled: int, total: int = 5, size: int = 18) -> None:
    """
    Draw a row of *total* stars centred at (cx, cy).
    The first *filled* are gold; the rest are dark grey.
    """
    gap   = size * 2 + 4
    start = cx - (total - 1) * gap // 2
    for i in range(total):
        sx  = start + i * gap
        pts = _star_points(sx, cy, size, size * 0.42)
        col = C.GOLD if i < filled else (45, 45, 65)
        pygame.draw.polygon(display.screen, col, pts)
        if i < filled:
            pygame.draw.polygon(display.screen, (255, 240, 120), pts, 1)


def _overlay(r: int = 0, g: int = 0, b: int = 15, a: int = 200):
    """Draw a semi-transparent full-screen colour rectangle."""
    s = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
    s.fill((r, g, b, a))
    display.screen.blit(s, (0, 0))


def draw_splash() -> None:
    """
    Animated splash / logo screen shown at startup.
    Uses pygame.time.get_ticks() for time-based animation.
    Player presses any key to advance to the main menu.
    """
    ticks = pygame.time.get_ticks()

    # ── Animated dark background ───────────────────────────────────────────────
    bg_pulse = abs(math.sin(ticks * 0.00025))
    bg_r     = int(4  + bg_pulse * 8)
    bg_g     = int(6  + bg_pulse * 10)
    bg_b     = int(28 + bg_pulse * 18)
    display.screen.fill((bg_r, bg_g, bg_b))

    # Subtle animated diagonal scan-lines
    offset = (ticks // 18) % 48
    for i in range(-C.SH, C.SW + C.SH, 48):
        x1 = i + offset
        pygame.draw.line(display.screen, (12, 20, 52),
                         (x1, 0), (x1 + C.SH, C.SH), 1)

    # ── Glow ring behind the title ─────────────────────────────────────────────
    glow_alpha = int(40 + abs(math.sin(ticks * 0.0008)) * 35)
    glow_surf  = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
    pygame.draw.ellipse(glow_surf, (255, 80, 160, glow_alpha),
                        (C.SW // 2 - 420, C.SH // 2 - 120, 840, 240))
    display.screen.blit(glow_surf, (0, 0))

    # ── Title text — layered for a shiny embossed look ─────────────────────────
    title_str = "KIRBY  ×  MILES MORALES"
    cy        = C.SH // 2 - 60

    layers = [
        (( 60,  0,  35), 4, 4),   # deep shadow
        ((150,  0,  80), 2, 2),   # mid shadow
        ((255, 105, 180), 0, 0),  # main (hot pink)
        ((255, 220, 240),-1,-1),  # specular highlight
    ]
    for col, ox, oy in layers:
        surf = display.f_title.render(title_str, True, col)
        display.screen.blit(surf,
                            (C.SW // 2 - surf.get_width() // 2 + ox, cy + oy))

    # ── Subtitle ───────────────────────────────────────────────────────────────
    sub_layers = [
        ((100, 80,  0), 2, 2),
        ((255, 215, 0), 0, 0),
        ((255, 255,180),-1,-1),
    ]
    for col, ox, oy in sub_layers:
        surf = display.f_big.render("ESL  Adventure", True, col)
        display.screen.blit(surf,
                            (C.SW // 2 - surf.get_width() // 2 + ox, cy + 65 + oy))

    # ── Thin gold divider ──────────────────────────────────────────────────────
    pygame.draw.line(display.screen, C.GOLD,
                     (C.SW // 2 - 280, cy + 112), (C.SW // 2 + 280, cy + 112), 1)

    # ── "Press any key" (appears after 1.5 s, then pulses) ────────────────────
    if ticks >= 1500:
        pulse = abs(math.sin((ticks - 1500) * 0.0028))
        r     = int(200 + pulse * 55)
        g     = int(200 + pulse * 55)
        b     = int(30  + pulse * 20)
        txt("PRESS  ANY  KEY  TO  CONTINUE", display.f_med, (r, g, b),
            C.SW // 2, cy + 148, center=True, shadow=True)

    # ── Small credit line ──────────────────────────────────────────────────────
    txt("A game by  Mr. Joshua", display.f_xs, (70, 70, 100),
        C.SW // 2, C.SH - 26, center=True)


def draw_title(sel: int, save_exists: bool, enter_ms: int = 0) -> None:
    """
    Main title / menu screen.

    sel         – currently highlighted item (0=New Game, 1=Load Game,
                  2=Options, 3=Credits)
    save_exists – if False, Load Game is greyed out
    enter_ms    – pygame.time.get_ticks() when TITLE was entered (drives flash-in)
    """
    scr = display.screen
    now = pygame.time.get_ticks()

    # ── Background ────────────────────────────────────────────────────────────
    if assets.main_menu_img:
        scr.blit(assets.main_menu_img, (0, 0))
    else:
        _overlay(0, 4, 22, 210)

    # ── Logo ──────────────────────────────────────────────────────────────────
    txt("KIRBY  ×  MILES MORALES", display.f_title, C.HOTPNK,
        C.SW // 2, 96, center=True, shadow=True)
    txt("ESL  Adventure", display.f_big, C.GOLD,
        C.SW // 2, 152, center=True, shadow=True)

    # ── Menu items (no box — selected item pulses) ────────────────────────────
    ITEMS = [
        ("NEW GAME",  True),
        ("LOAD GAME", save_exists),
        ("OPTIONS",   True),
        ("CREDITS",   True),
    ]

    menu_top = 230   # centre-y of first item
    item_h   = 60

    # Slow sine pulse: alpha oscillates between 60 and 255 (~1.4 s period)
    pulse_alpha = int(60 + 195 * (math.sin(now * math.pi / 700) * 0.5 + 0.5))

    for i, (label, enabled) in enumerate(ITEMS):
        cy     = menu_top + i * item_h
        is_sel = (i == sel)

        if not enabled:
            txt(label, display.f_med, C.DKGRAY, C.SW // 2, cy, center=True)
        elif is_sel:
            surf = display.f_med.render(label, True, C.GOLD)
            surf.set_alpha(pulse_alpha)
            scr.blit(surf, surf.get_rect(center=(C.SW // 2, cy)))
        else:
            txt(label, display.f_med, C.WHITE, C.SW // 2, cy, center=True)

    # ── Navigation hint ────────────────────────────────────────────────────────
    txt("W / S  or  ↑ ↓  to navigate    ENTER to select",
        display.f_xs, C.GRAY, C.SW // 2, C.SH - 30, center=True)

    # ── Epic flash-in (white overlay decaying on entry) ───────────────────────
    if enter_ms > 0:
        elapsed  = now - enter_ms
        _FLASH_MS = 900
        if elapsed < _FLASH_MS:
            flash_a = max(0, int(255 * (1.0 - elapsed / _FLASH_MS) ** 2))
            if flash_a:
                ov = pygame.Surface((C.SW, C.SH))
                ov.fill((255, 255, 255))
                ov.set_alpha(flash_a)
                scr.blit(ov, (0, 0))


def draw_title_options(sel: int, vol: float, sfx_vol: float,
                       track_name: str, mode_name: str) -> None:
    """
    Options submenu.

    sel        – highlighted row (0=Music Vol, 1=Sound Vol, 2=Music Track,
                                  3=Display Mode, 4=Back)
    vol        – current music volume 0.0–1.0
    sfx_vol    – current sound-effect volume 0.0–1.0
    track_name – current music track filename (no extension)
    mode_name  – current display mode label string
    """
    _overlay(0, 4, 22, 220)

    txt("OPTIONS", display.f_title, C.GOLD,
        C.SW // 2, 62, center=True, shadow=True)
    pygame.draw.line(display.screen, C.GOLD,
                     (C.SW // 2 - 200, 112), (C.SW // 2 + 200, 112), 2)

    pw, ph = 700, 426
    px     = (C.SW - pw) // 2
    py     = 108
    pygame.draw.rect(display.screen, (10, 22, 70), (px, py, pw, ph), border_radius=14)
    pygame.draw.rect(display.screen, C.GOLD,       (px, py, pw, ph), border_radius=14, width=2)

    ROWS = [
        ("Music Volume",  f"{int(vol     * 100)} %", vol),
        ("Sound Volume",  f"{int(sfx_vol * 100)} %", sfx_vol),
        ("Music Track",   track_name,                 None),
        ("Display Mode",  mode_name,                  None),
        ("Back",          "",                          None),
    ]

    row_h = 72
    bar_w = pw - 160
    bar_h = 13

    for i, (label, value, bar_val) in enumerate(ROWS):
        ry     = py + 16 + i * row_h
        is_sel = (i == sel)

        if is_sel:
            pygame.draw.rect(display.screen, (40, 80, 200),
                             (px + 16, ry, pw - 32, 58), border_radius=8)
            pygame.draw.rect(display.screen, C.GOLD,
                             (px + 16, ry, pw - 32, 58), border_radius=8, width=1)

        label_col = C.GOLD if is_sel else C.WHITE
        value_col = C.CYAN if is_sel else C.LGRAY

        if label == "Back":
            txt("Back", display.f_med, label_col, C.SW // 2, ry + 16, center=True)

        elif bar_val is not None:
            # Volume rows with slider bar
            txt(label, display.f_sm, label_col, px + 40, ry + 6)
            bar_x  = px + 40
            bar_y  = ry + 34
            filled = int(bar_w * bar_val)
            pygame.draw.rect(display.screen, C.DKGRAY,
                             (bar_x, bar_y, bar_w, bar_h), border_radius=4)
            if filled:
                bar_col = C.CYAN if label == "Music Volume" else C.ORANGE
                pygame.draw.rect(display.screen, bar_col,
                                 (bar_x, bar_y, filled, bar_h), border_radius=4)
            pygame.draw.rect(display.screen, C.GRAY,
                             (bar_x, bar_y, bar_w, bar_h), border_radius=4, width=1)
            txt(value, display.f_sm, value_col, bar_x + bar_w + 14, ry + 30)

        else:
            # Text rows with arrows (Music Track, Display Mode)
            txt(label,             display.f_sm, label_col, px + 40, ry + 6)
            txt(f"◄  {value}  ►", display.f_sm, value_col, px + 40, ry + 32)

    txt("↑ ↓  navigate     ← →  adjust     ESC  back",
        display.f_xs, C.GRAY, C.SW // 2, py + ph + 18, center=True)


def draw_title_credits() -> None:
    """Credits screen."""
    _overlay(0, 4, 22, 225)

    txt("CREDITS", display.f_title, C.GOLD,
        C.SW // 2, 90, center=True, shadow=True)
    pygame.draw.line(display.screen, C.GOLD,
                     (C.SW // 2 - 200, 140), (C.SW // 2 + 200, 140), 2)

    cw, ch = 540, 340
    cx     = (C.SW - cw) // 2
    cy     = 158
    pygame.draw.rect(display.screen, (10, 22, 70), (cx, cy, cw, ch), border_radius=14)
    pygame.draw.rect(display.screen, C.GOLD,       (cx, cy, cw, ch), border_radius=14, width=2)

    txt("Developer", display.f_sm,  C.LGRAY, C.SW // 2, cy + 36,  center=True)
    txt("Mr. Joshua",  display.f_big,  C.GOLD,  C.SW // 2, cy + 66,  center=True, shadow=True)

    pygame.draw.line(display.screen, C.DKGRAY,
                     (cx + 40, cy + 104), (cx + cw - 40, cy + 104), 1)

    CONTRIBUTORS = [
        ("Math Expert",       "Uhyun"),
        ("Character Artist",  "Alice"),
    ]
    for i, (role, name) in enumerate(CONTRIBUTORS):
        oy = cy + 124 + i * 72
        txt(role, display.f_sm,  C.LGRAY, C.SW // 2, oy,      center=True)
        txt(name, display.f_big, C.LPURPLE, C.SW // 2, oy + 30, center=True, shadow=True)

    pygame.draw.line(display.screen, C.DKGRAY,
                     (cx + 40, cy + 272), (cx + cw - 40, cy + 272), 1)

    txt("Made with Python & Pygame", display.f_xs, C.GRAY, C.SW // 2, cy + 292, center=True)

    pulse = abs(math.sin(pygame.time.get_ticks() * 0.003))
    cv    = int(160 + pulse * 95)
    txt("Press  any key  to go back", display.f_sm, (cv, cv, cv),
        C.SW // 2, cy + ch + 22, center=True)


def draw_grade_select(hover: int = 0):
    """
    Grade-selection screen.  hover = 1–6 highlights that card (use 0 for none).
    The player presses 1–6 to pick their grade.
    """
    if assets.main_menu_img:
        display.screen.blit(assets.main_menu_img, (0, 0))
        _overlay(0, 0, 0, 120)
    else:
        _overlay(5, 10, 35, 240)

    txt("Kirby  x  Miles Morales", display.f_title, C.HOTPNK,
        C.SW // 2, 38, center=True, shadow=True)
    txt("Choose Your Grade Level", display.f_big, C.GOLD,
        C.SW // 2, 90, center=True, shadow=True)

    GRADE_INFO = {
        1: {"desc": "Basic sentences & nature",         "col": ( 60, 200,  60)},
        2: {"desc": "Opposites, plurals & simple sci",  "col": ( 40, 190, 170)},
        3: {"desc": "Synonyms, past tense & Earth",     "col": ( 50, 110, 220)},
        4: {"desc": "Grammar rules & Earth science",    "col": (210, 160,  30)},
        5: {"desc": "Advanced vocab & biology",         "col": (190,  70, 190)},
        6: {"desc": "Literary terms & chemistry",       "col": (220,  50,  50)},
    }

    # 2 rows × 3 columns
    cw, ch  = 318, 118
    gap     = 16
    total_w = 3 * cw + 2 * gap
    sx      = (C.SW - total_w) // 2
    row_y   = [130, 130 + ch + gap]

    for i, (grade, info) in enumerate(GRADE_INFO.items()):
        col_i   = i % 3
        row_i   = i // 3
        x       = sx + col_i * (cw + gap)
        y       = row_y[row_i]
        col     = info["col"]
        is_hov  = (grade == hover)

        # Card background
        bg_col  = tuple(min(255, c + 30) for c in col) if is_hov else (18, 28, 60)
        pygame.draw.rect(display.screen, bg_col,   (x, y, cw, ch), border_radius=10)
        bord_w  = 4 if is_hov else 2
        pygame.draw.rect(display.screen, col,      (x, y, cw, ch), border_radius=10, width=bord_w)

        # Grade number (large)
        num_surf = display.f_title.render(str(grade), True, col)
        display.screen.blit(num_surf, (x + 18, y + ch // 2 - num_surf.get_height() // 2))

        # "GRADE" label + description
        txt(f"GRADE {grade}", display.f_sm, C.WHITE, x + 70, y + 26)
        txt(info["desc"],     display.f_xs, C.LGRAY,  x + 70, y + 54)

        # Key hint
        key_col = col if is_hov else C.GRAY
        txt(f"Press {grade}", display.f_xs, key_col, x + 70, y + 82)

    # Bottom prompt
    pulse = abs(math.sin(pygame.time.get_ticks() * 0.003))
    cv    = int(180 + pulse * 75)
    txt("Press  1 – 6  to select your grade", display.f_med,
        (cv, cv, 40), C.SW // 2, row_y[1] + ch + 28, center=True, shadow=True)


def draw_char_select(sel: int, secret_popup: bool = False,
                     secret_sel: int = 0) -> None:
    """
    Character selection screen.
    sel: 0 = Kirby,  1 = Miles Morales,  2 = Secret Characters
    secret_popup: show the secret character selection overlay
    secret_sel: 0-5 slot index highlighted in the popup
    """
    if assets.main_menu_img:
        display.screen.blit(assets.main_menu_img, (0, 0))
        _overlay(0, 0, 0, 120)
    else:
        _overlay(0, 5, 25, 230)

    txt("CHOOSE YOUR HERO", display.f_title, C.GOLD,
        C.SW // 2, 44, center=True, shadow=True)
    pygame.draw.line(display.screen, C.GOLD,
                     (C.SW // 2 - 220, 92), (C.SW // 2 + 220, 92), 2)

    CHARS = [
        {
            "id":    "kirby",
            "name":  "KIRBY",
            "col":   C.HOTPNK,
            "lines": ["Brave, kind, and full of heart.",
                      "Kirby faces every challenge",
                      "with a smile and a song."],
            "key":   "Press  1",
        },
        {
            "id":    "miles",
            "name":  "MILES MORALES",
            "col":   (80, 140, 255),
            "lines": ["Sharp, determined, and unstoppable.",
                      "Miles never backs down",
                      "from a challenge."],
            "key":   "Press  2",
        },
        {
            "id":    "secret",
            "name":  "SECRET CHARACTERS",
            "col":   (200, 160, 255),
            "lines": ["Hidden heroes shrouded in mystery.",
                      "Unlock their stories and",
                      "discover their power."],
            "key":   "Press  3",
        },
    ]

    card_w, card_h = 310, 430
    gap    = 30
    total  = card_w * 3 + gap * 2
    left_x = (C.SW - total) // 2
    card_y = 108

    for i, ch in enumerate(CHARS):
        cx     = left_x + i * (card_w + gap)
        is_sel = (i == sel)
        mid    = cx + card_w // 2

        # Card background + border
        bg_col     = (30, 50, 130) if is_sel else (12, 18, 50)
        border_col = ch["col"]     if is_sel else (50, 55, 80)
        bw         = 3             if is_sel else 1
        pygame.draw.rect(display.screen, bg_col,
                         (cx, card_y, card_w, card_h), border_radius=18)
        pygame.draw.rect(display.screen, border_col,
                         (cx, card_y, card_w, card_h), border_radius=18, width=bw)

        # Glow rim on selected card
        if is_sel:
            glow = pygame.Surface((card_w + 12, card_h + 12), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*ch["col"], 55),
                             (0, 0, card_w + 12, card_h + 12), border_radius=22)
            display.screen.blit(glow, (cx - 6, card_y - 6))

        # ── Character preview ────────────────────────────────────────────────
        prev_cx = mid
        prev_cy = card_y + 155

        if i == 0:
            _preview_kirby(prev_cx, prev_cy, assets.player_img)
        elif i == 1:
            _preview_miles(prev_cx, prev_cy, assets.miles_img)
        else:
            _preview_secret_card(prev_cx, prev_cy, is_sel)

        # ── Name ────────────────────────────────────────────────────────────
        txt(ch["name"], display.f_sm, ch["col"],
            mid, card_y + 292, center=True, shadow=True)

        # ── Description ─────────────────────────────────────────────────────
        for j, line in enumerate(ch["lines"]):
            col = C.WHITE if is_sel else C.GRAY
            txt(line, display.f_xs, col, mid, card_y + 326 + j * 20, center=True)

        # ── Key hint ─────────────────────────────────────────────────────────
        hint_col = C.GOLD if is_sel else (100, 100, 120)
        txt(ch["key"], display.f_xs, hint_col,
            mid, card_y + card_h - 24, center=True)

    # Bottom instruction
    txt("◄ ►  or  1 / 2 / 3  to choose        Enter to confirm",
        display.f_sm, (160, 160, 200), C.SW // 2, C.SH - 24, center=True)

    # Secret character popup
    if secret_popup:
        _draw_secret_char_popup(secret_sel)


# ── Character preview helpers ─────────────────────────────────────────────────

def _preview_kirby(cx: int, cy: int, img) -> None:
    """Draw a large Kirby preview centred on (cx, cy)."""
    R = 46
    if img:
        scaled = pygame.transform.smoothscale(img, (R * 2, R * 2))
        display.screen.blit(scaled, (cx - R, cy - R))
        return
    # Procedural
    pygame.draw.ellipse(display.screen, (100, 100, 100),
                        (cx - R + 4, cy + R - 10, R * 2 - 8, 14))
    pygame.draw.circle(display.screen, C.HOTPNK,  (cx, cy), R)
    pygame.draw.circle(display.screen, C.PINK,    (cx, cy), R, 3)
    pygame.draw.ellipse(display.screen, (255, 118, 142),
                        (cx - R + 6, cy + 8, 20, 12))
    pygame.draw.ellipse(display.screen, (255, 118, 142),
                        (cx + R - 26, cy + 8, 20, 12))
    for ex in (cx - 22, cx + 6):
        pygame.draw.ellipse(display.screen, (38, 14, 58), (ex, cy - 20, 17, 12))
        pygame.draw.circle(display.screen, C.WHITE, (ex + 4, cy - 17), 3)
    pygame.draw.ellipse(display.screen, (75, 12, 32),  (cx - 14, cy + 4, 28, 18))
    pygame.draw.ellipse(display.screen, (195, 45, 75), (cx - 11, cy + 6, 22, 14))
    pygame.draw.ellipse(display.screen, C.HOTPNK,
                        (cx - R + 4,  cy + R - 16, 25, 18))
    pygame.draw.ellipse(display.screen, C.HOTPNK,
                        (cx + R - 30, cy + R - 16, 25, 18))


def _preview_miles(cx: int, cy: int, img) -> None:
    """Draw a large Miles Morales preview centred on (cx, cy)."""
    if img:
        R = 46
        scaled = pygame.transform.smoothscale(img, (R * 2, R * 2))
        display.screen.blit(scaled, (cx - R, cy - R))
        return
    # Procedural
    BLACK = (10,  10,  10)
    RED   = (200, 20,  20)
    WHITE = (230, 230, 230)
    # Legs
    pygame.draw.rect(display.screen, BLACK, (cx - 18, cy + 10, 14, 28), border_radius=4)
    pygame.draw.rect(display.screen, BLACK, (cx + 4,  cy + 10, 14, 28), border_radius=4)
    # Boots
    pygame.draw.ellipse(display.screen, RED, (cx - 20, cy + 34, 18, 12))
    pygame.draw.ellipse(display.screen, RED, (cx + 2,  cy + 34, 18, 12))
    # Torso
    pygame.draw.rect(display.screen, BLACK, (cx - 20, cy - 12, 40, 26), border_radius=6)
    pygame.draw.rect(display.screen, RED,   (cx - 20, cy - 1,  40,  8), border_radius=3)
    # Spider symbol
    pygame.draw.line(display.screen, WHITE, (cx, cy - 11), (cx, cy + 2), 3)
    pygame.draw.line(display.screen, WHITE, (cx - 8, cy - 5), (cx + 8, cy - 5), 3)
    # Arms
    pygame.draw.rect(display.screen, BLACK, (cx - 34, cy - 12, 14, 20), border_radius=4)
    pygame.draw.rect(display.screen, BLACK, (cx + 20, cy - 12, 14, 20), border_radius=4)
    # Head
    pygame.draw.circle(display.screen, BLACK, (cx, cy - 30), 20)
    # Eyes
    pygame.draw.ellipse(display.screen, WHITE, (cx - 18, cy - 38, 14, 10))
    pygame.draw.ellipse(display.screen, WHITE, (cx + 4,  cy - 38, 14, 10))
    pygame.draw.line(display.screen, RED,
                     (cx - 16, cy - 41), (cx + 16, cy - 41), 3)


def _preview_secret_card(cx: int, cy: int, is_sel: bool) -> None:
    """Draw a '?' placeholder preview for the secret characters card."""
    R = 46
    pulse_col = (160, 80, 255) if is_sel else (80, 40, 130)
    pygame.draw.circle(display.screen, (30, 10, 60),  (cx, cy), R)
    pygame.draw.circle(display.screen, pulse_col, (cx, cy), R, 3)
    font = pygame.font.SysFont("arial", R + 10, bold=True)
    surf = font.render("?", True, (200, 160, 255) if is_sel else (120, 80, 180))
    display.screen.blit(surf, surf.get_rect(center=(cx, cy)))


def _draw_secret_char_popup(sel: int) -> None:
    """
    Centered 720×400 popup with 6 character slots (3 cols × 2 rows).
    Slots 0-1 are playable; slots 2-5 are locked '???'.
    sel: 0-5 currently highlighted slot.
    """
    pw, ph = 720, 420
    px = (C.SW - pw) // 2
    py = (C.SH - ph) // 2

    # Dimmed backdrop
    dim = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 160))
    display.screen.blit(dim, (0, 0))

    # Panel
    pygame.draw.rect(display.screen, (18, 8, 45), (px, py, pw, ph), border_radius=20)
    pygame.draw.rect(display.screen, (200, 160, 255), (px, py, pw, ph), border_radius=20, width=3)

    txt("SECRET CHARACTERS", display.f_big, (200, 160, 255),
        C.SW // 2, py + 28, center=True, shadow=True)
    pygame.draw.line(display.screen, (100, 60, 160),
                     (px + 30, py + 56), (px + pw - 30, py + 56), 1)

    slot_w, slot_h = 190, 120
    cols, rows = 3, 2
    gap_x = (pw - slot_w * cols) // (cols + 1)
    gap_y = 18
    grid_top = py + 72

    SECRET_CHARS = [
        {"name": "???", "col": (200, 160, 255), "locked": False},
        {"name": "???", "col": (200, 160, 255), "locked": False},
        {"name": "???", "col": (80, 60, 100),   "locked": True},
        {"name": "???", "col": (80, 60, 100),   "locked": True},
        {"name": "???", "col": (80, 60, 100),   "locked": True},
        {"name": "???", "col": (80, 60, 100),   "locked": True},
    ]

    for idx, sc in enumerate(SECRET_CHARS):
        col_i = idx % cols
        row_i = idx // cols
        sx = px + gap_x + col_i * (slot_w + gap_x)
        sy = grid_top + row_i * (slot_h + gap_y)
        is_sel = (idx == sel)

        bg_c  = (50, 20, 90)  if (is_sel and not sc["locked"]) else (22, 10, 40)
        bdr_c = sc["col"]     if is_sel else (60, 40, 90)
        bdr_w = 3             if is_sel else 1
        pygame.draw.rect(display.screen, bg_c,  (sx, sy, slot_w, slot_h), border_radius=12)
        pygame.draw.rect(display.screen, bdr_c, (sx, sy, slot_w, slot_h), border_radius=12, width=bdr_w)

        mid_x = sx + slot_w // 2
        mid_y = sy + slot_h // 2

        if sc["locked"]:
            # Lock icon (simple procedural)
            lx, ly = mid_x, mid_y - 8
            pygame.draw.rect(display.screen, (80, 60, 100),
                             (lx - 12, ly,     24, 18), border_radius=4)
            pygame.draw.arc(display.screen, (80, 60, 100),
                            (lx - 10, ly - 16, 20, 20),
                            0, 3.14159, 3)
            txt("LOCKED", display.f_xs, (80, 60, 100), mid_x, sy + slot_h - 18, center=True)
        else:
            # Sprite or '?' placeholder
            img = assets.secret1_img if idx == 0 else assets.secret2_img
            if img:
                scaled = pygame.transform.smoothscale(img, (60, 60))
                display.screen.blit(scaled, scaled.get_rect(center=(mid_x, mid_y - 10)))
            else:
                font = pygame.font.SysFont("arial", 38, bold=True)
                surf = font.render("?", True, (200, 160, 255))
                display.screen.blit(surf, surf.get_rect(center=(mid_x, mid_y - 10)))
            name_col = (200, 160, 255) if is_sel else (150, 110, 200)
            txt(sc["name"], display.f_xs, name_col, mid_x, sy + slot_h - 18, center=True)

    txt("ESC to close   ◄ ► ▲ ▼ navigate   Enter to select",
        display.f_xs, (120, 100, 160), C.SW // 2, py + ph - 18, center=True)


def draw_intro(selected_grade: int = 0):
    _overlay(0, 0, 18, 215)

    txt("Kirby  x  Miles Morales", display.f_title, C.HOTPNK,
        C.SW // 2, 100, center=True, shadow=True)
    txt("ESL Adventure", display.f_big, C.GOLD,
        C.SW // 2, 152, center=True, shadow=True)

    # Grade badge
    if selected_grade:
        badge_col = {1:(60,200,60), 2:(40,190,170), 3:(50,110,220),
                     4:(210,160,30), 5:(190,70,190), 6:(220,50,50)}.get(selected_grade, C.GOLD)
        bw, bh = 220, 36
        bx = C.SW // 2 - bw // 2
        pygame.draw.rect(display.screen, badge_col, (bx, 192, bw, bh), border_radius=8)
        txt(f"Grade {selected_grade}  selected", display.f_sm, C.WHITE,
            C.SW // 2, 196, center=True)

    pw, ph = 650, 210
    px, py = (C.SW - pw) // 2, 240
    pygame.draw.rect(display.screen, C.DKBLUE, (px, py, pw, ph), border_radius=12)
    pygame.draw.rect(display.screen, C.GOLD,   (px, py, pw, ph), border_radius=12, width=3)

    hints = [
        ("Walk into a door to answer its question!",        C.WHITE),
        ("Grammar, Vocabulary, and Science per door.",      C.WHITE),
        ("Find KEYS to unlock locked doors.",               C.WHITE),
        ("You have 3 lives – choose wisely!",               C.WHITE),
        ("Arrow Keys or WASD  |  slide in all directions",  C.LPURPLE),
    ]
    for i, (h, col) in enumerate(hints):
        txt(h, display.f_sm, col, C.SW // 2, py + 22 + i * 36, center=True)

    pulse = abs(math.sin(pygame.time.get_ticks() * 0.003))
    cv = int(200 + pulse * 55)
    txt("Press ENTER or SPACE to Start!", display.f_med, (cv, cv, 40),
        C.SW // 2, py + ph + 26, center=True, shadow=True)


def draw_bonus_q(q: dict):
    _overlay(25, 0, 50, 215)

    txt("*  BONUS ROUND  *", display.f_title, C.GOLD,
        C.SW // 2, 102, center=True, shadow=True)
    txt("Answer correctly to SKIP the next level!", display.f_sm, C.CYAN,
        C.SW // 2, 155, center=True)

    pw, ph = 690, 285
    px, py = (C.SW - pw) // 2, 182
    pygame.draw.rect(display.screen, C.DKBLUE, (px, py, pw, ph), border_radius=12)
    pygame.draw.rect(display.screen, C.GOLD,   (px, py, pw, ph), border_radius=12, width=3)

    lines = wrap_text(q["q"], display.f_med, pw - 60)
    for i, line in enumerate(lines):
        txt(line, display.f_med, C.WHITE, C.SW // 2, py + 28 + i * 30, center=True)

    btn_colors = [C.RED, C.DKGRN, C.BLUE]
    for i, opt in enumerate(q["opts"]):
        by = py + 98 + i * 54
        pygame.draw.rect(display.screen, btn_colors[i], (px+32, by, pw-64, 44), border_radius=7)
        pygame.draw.rect(display.screen, C.WHITE,       (px+32, by, pw-64, 44), border_radius=7, width=2)
        txt(f"{i+1}.   {opt}", display.f_med, C.WHITE,
            C.SW // 2, by + 22, center=True)

    txt("Press  1 , 2  or  3  to answer", display.f_sm, C.YELLOW,
        C.SW // 2, py + ph - 22, center=True)


def draw_bonus_res(won: bool):
    _overlay(0, 0, 0, 170)
    if won:
        txt("CORRECT!  Level Skipped!", display.f_title, C.GOLD,
            C.SW // 2, C.SH // 2 - 28, center=True, shadow=True)
        txt("+300 bonus points!", display.f_big, C.GREEN,
            C.SW // 2, C.SH // 2 + 40, center=True)
    else:
        txt("Not quite! Keep going!", display.f_title, C.ORANGE,
            C.SW // 2, C.SH // 2 - 28, center=True, shadow=True)
        txt("Head to the correct door!", display.f_med, C.WHITE,
            C.SW // 2, C.SH // 2 + 40, center=True)


def draw_lvl_done(lvl: int, score: int, level_stars: int = 0, total_stars: int = 0):
    _overlay(0, 20, 0, 185)
    txt(f"World {lvl} Complete!", display.f_title, C.GREEN,
        C.SW // 2, 160, center=True, shadow=True)
    txt(f"Score: {score}", display.f_big, C.GOLD,
        C.SW // 2, 238, center=True)

    # ── Stars earned this world (max 75: 5 stages × 3 doors × 5 stars) ────────
    txt(f"Stars this world:  ★ {level_stars}", display.f_med, C.GOLD,
        C.SW // 2, 295, center=True)

    # ── Running total ─────────────────────────────────────────────────────────
    txt(f"Total stars:  ★ {total_stars}", display.f_med, C.YELLOW,
        C.SW // 2, 340, center=True)

    if lvl < C.TOTAL:
        txt(f"Next: World {lvl + 1}  –  Grade {lvl + 1} challenges!",
            display.f_med, C.CYAN, C.SW // 2, 400, center=True)
    txt("Press ENTER or SPACE to continue", display.f_sm, C.YELLOW,
        C.SW // 2, 450, center=True)


# ─── Tutorial ─────────────────────────────────────────────────────────────────

_TUTORIAL_TITLES = ["Welcome!", "Portals", "Items", "Need Help?"]

_TUTORIAL_TEXT = [
    "Hi my name is Gizmo, and I am here to help you on your quest to find all "
    "the ancient scrolls! The scrolls are scattered across 6 worlds! To get a "
    "scroll, you have to answer a question! If you answer a question quickly, "
    "you will receive stars! The faster you answer a question, the more stars "
    "you get! Earning many stars will give you special rewards like potions, "
    "armor, and other secrets! These will be useful for your journey!",

    "There are 3 portals in every stage. There are 5 stages in each world. "
    "Each portal will ask a different question. There are G, V, and S portals. "
    "These portals will test your knowledge! Also, be aware, as you continue, "
    "new portals may open!",

    "Health potions provide health points during boss battles. Magic potions "
    "deal damage to foes. Armor protects against attacks. Keys provide access "
    "to special portals.",

    "If you have questions, ask me or Mr. Joshua, and we can provide hints!",
]

_TUTORIAL_TITLE_COLORS = [
    (0, 150, 220),    # page 0 – blue
    (20, 160, 90),    # page 1 – green
    (160, 80, 220),   # page 2 – purple
    (210, 140, 0),    # page 3 – amber
]


def _draw_gizmo(cx: int, cy: int, scale: float = 1.0) -> None:
    """Draw the Gizmo tutorial guide robot centred at (cx, cy)."""
    scr   = display.screen
    bob   = int(math.sin(pygame.time.get_ticks() * 0.004) * 4)
    cy   += bob
    s     = scale
    R     = int(26 * s)
    TEAL  = (0,   200, 185)
    LTEAL = (90,  230, 215)
    DTEAL = (0,   140, 125)
    GOLD  = (255, 210,  40)
    EYE_W = (240, 245, 255)
    EYE_P = (25,   15,  55)

    # Antenna
    pygame.draw.line(scr, DTEAL, (cx, cy - R), (cx, cy - R - int(22*s)), 3)
    pygame.draw.circle(scr, GOLD,         (cx, cy - R - int(22*s)), int(6*s))
    pygame.draw.circle(scr, (255, 255, 160), (cx, cy - R - int(22*s)), int(3*s))

    # Head
    pygame.draw.circle(scr, TEAL,  (cx, cy), R)
    pygame.draw.circle(scr, LTEAL, (cx - R // 3, cy - R // 3), R // 3)
    pygame.draw.circle(scr, DTEAL, (cx, cy), R, 2)

    # Eyes
    ew, eh = int(11 * s), int(13 * s)
    for ex in (cx - int(9 * s), cx + int(1 * s)):
        pygame.draw.ellipse(scr, EYE_W, (ex, cy - int(14 * s), ew, eh))
        pygame.draw.circle(scr, EYE_P,  (ex + ew // 2, cy - int(8 * s)), int(4 * s))
        pygame.draw.circle(scr, EYE_W,  (ex + ew // 2 - 2, cy - int(10 * s)), 1)

    # Smile
    pygame.draw.arc(scr, EYE_W,
                    (cx - int(9 * s), cy + int(2 * s), int(18 * s), int(9 * s)),
                    math.pi, 0, 2)

    # Body
    bx, by = cx - int(20 * s), cy + R + 2
    bw, bh = int(40 * s), int(32 * s)
    pygame.draw.rect(scr, TEAL,  (bx, by, bw, bh), border_radius=int(6 * s))
    pygame.draw.rect(scr, DTEAL, (bx, by, bw, bh), border_radius=int(6 * s), width=2)
    pygame.draw.circle(scr, (50,  255, 100), (cx, by + bh // 2), int(5 * s))
    pygame.draw.circle(scr, (180, 255, 200), (cx, by + bh // 2), int(3 * s))

    # Arms
    ax_l, ax_r = bx - int(13 * s), bx + bw
    arm_y, aw, ah = by + int(6 * s), int(13 * s), int(19 * s)
    for ax in (ax_l, ax_r):
        pygame.draw.ellipse(scr, TEAL,  (ax, arm_y, aw, ah))
        pygame.draw.ellipse(scr, DTEAL, (ax, arm_y, aw, ah), 1)

    # Legs + feet
    for lx in (cx - int(14 * s), cx + int(4 * s)):
        pygame.draw.rect(scr, DTEAL, (lx, by + bh, int(10 * s), int(12 * s)), border_radius=3)
    for fx in (cx - int(18 * s), cx + int(2 * s)):
        pygame.draw.ellipse(scr, TEAL, (fx, by + bh + int(8 * s), int(16 * s), int(8 * s)))


def _draw_portal_badge(label: str, color: tuple, cx: int, cy: int) -> None:
    """Draw a colored portal indicator badge centred at (cx, cy)."""
    surf = display.f_sm.render(label, True, C.WHITE)
    bw   = surf.get_width() + 20
    bh   = surf.get_height() + 10
    lx   = max(4, min(C.SW - bw - 4, cx - bw // 2))
    ly   = max(4, min(C.SH - bh - 4, cy - bh // 2))
    bg   = pygame.Surface((bw, bh), pygame.SRCALPHA)
    bg.fill((color[0] // 2, color[1] // 2, color[2] // 2, 220))
    display.screen.blit(bg, (lx, ly))
    pygame.draw.rect(display.screen, color, (lx, ly, bw, bh), border_radius=6, width=2)
    display.screen.blit(surf, (lx + 10, ly + 5))


def _draw_portal_indicators() -> None:
    """Page-1 only: draw arrows near each door to identify Grammar/Vocab/Science."""
    # Grammar door: top-center (D1X=505, D1Y=0)
    _draw_portal_badge("↑  Grammar  (G)",  (30,  80, 200),
                        C.D1X + C.DW // 2, 152)
    # Vocab door: bottom-center (D2X=505, D2Y=520)
    _draw_portal_badge("↓  Vocab    (V)",  (20, 160,  80),
                        C.D2X + C.DW // 2, C.D2Y - 40)
    # Science door: right-center (D3X=1010, D3Y=260)
    _draw_portal_badge("Science  (S)  →",  (130, 50, 200),
                        C.D3X - 85, C.D3Y + C.DH // 2)


def draw_tutorial_prompt(sel: int = 0) -> None:
    """
    Y / N dialog asking if the player wants a tutorial.
    sel=0 → Yes highlighted; sel=1 → No highlighted.
    """
    _overlay(0, 10, 30, 180)

    dw, dh = 700, 340
    dx, dy = (C.SW - dw) // 2, (C.SH - dh) // 2 - 20

    panel = pygame.Surface((dw, dh), pygame.SRCALPHA)
    panel.fill((8, 25, 70, 240))
    display.screen.blit(panel, (dx, dy))
    pygame.draw.rect(display.screen, C.GOLD, (dx, dy, dw, dh), border_radius=18, width=3)

    _draw_gizmo(dx + 118, dy + 178, scale=1.2)

    txt("Would you like a tutorial?",
        display.f_big, C.WHITE, dx + 400, dy + 75, center=True, shadow=True)
    txt("Gizmo will guide you through", display.f_sm, C.CYAN,  dx + 400, dy + 128, center=True)
    txt("the basics of the game!",      display.f_sm, C.CYAN,  dx + 400, dy + 155, center=True)

    for i, (label, col_on, col_off) in enumerate([
        ("YES  (Y)", (35, 175, 75),  (15, 70, 35)),
        ("NO   (N)", (175, 55, 55),  (75, 25, 25)),
    ]):
        bw, bh = 190, 52
        bx = dx + 280 + i * (bw + 18)
        by = dy + 248
        col = col_on if sel == i else col_off
        btn = pygame.Surface((bw, bh), pygame.SRCALPHA)
        btn.fill((*col, 240))
        display.screen.blit(btn, (bx, by))
        border_col = C.GOLD if sel == i else C.GRAY
        pygame.draw.rect(display.screen, border_col, (bx, by, bw, bh), border_radius=10, width=3)
        txt(label, display.f_med, C.WHITE, bx + bw // 2, by + bh // 2, center=True, shadow=True)

    txt("← →  or  Y / N  to choose     ENTER to confirm",
        display.f_xs, C.LGRAY, C.SW // 2, dy + dh - 18, center=True)


def draw_tutorial(page: int) -> None:
    """
    Draw one of 4 tutorial pages (page 0–3).
    The stage is visible in the background through the semi-transparent overlay.
    """
    NPAGES = 4
    _overlay(0, 5, 20, 155)

    # Page 1: draw portal direction badges near each door
    if page == 1:
        _draw_portal_indicators()

    # Main panel
    px, py = 140, 285
    pw, ph = 820, 272
    panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
    panel.fill((6, 18, 54, 230))
    display.screen.blit(panel, (px, py))
    pygame.draw.rect(display.screen, C.GOLD, (px, py, pw, ph), border_radius=14, width=3)

    # Coloured title bar
    tc = _TUTORIAL_TITLE_COLORS[page]
    pygame.draw.rect(display.screen, tc, (px, py, pw, 40), border_radius=14)
    pygame.draw.rect(display.screen, tc, (px, py + 20, pw, 20))
    txt(_TUTORIAL_TITLES[page], display.f_med, C.WHITE,
        px + pw // 2, py + 20, center=True, shadow=True)

    # Gizmo — left of panel
    _draw_gizmo(75, 498, scale=1.1)

    # Speech-bubble triangle connector from Gizmo toward panel
    tri = [(140, 468), (120, 498), (140, 518)]
    pygame.draw.polygon(display.screen, (6, 18, 54), tri)
    pygame.draw.polygon(display.screen, C.GOLD, tri, 2)

    # Wrapped text content
    cx0 = px + 20
    cy0 = py + 52
    cw  = pw - 32
    lines = wrap_text(_TUTORIAL_TEXT[page], display.f_sm, cw)
    lh    = display.f_sm.get_linesize() + 3
    for i, line in enumerate(lines[:7]):
        txt(line, display.f_sm, C.WHITE, cx0, cy0 + i * lh)

    # Page dots
    dot_y  = py + ph + 16
    dot_cx = C.SW // 2
    for i in range(NPAGES):
        filled = (i == page)
        col    = C.GOLD if filled else (50, 50, 80)
        r      = 8 if filled else 5
        pygame.draw.circle(display.screen, col,
                           (dot_cx + (i - NPAGES // 2) * 24, dot_y), r)

    # Continue / finish hint
    pulse = abs(math.sin(pygame.time.get_ticks() * 0.003))
    cv    = int(180 + pulse * 75)
    hint  = "ENTER or SPACE  –  start playing!" if page == NPAGES - 1 else "ENTER or SPACE  –  continue"
    txt(hint, display.f_sm, (cv, cv, 60), C.SW // 2, dot_y + 26, center=True)
    txt("ESC – skip tutorial", display.f_xs, C.GRAY, C.SW // 2, dot_y + 50, center=True)


def draw_gameover(score: int):
    _overlay(38, 0, 0, 200)
    txt("Game Over", display.f_title, C.RED,
        C.SW // 2, 215, center=True, shadow=True)
    txt(f"Final Score: {score}", display.f_big, C.GOLD,
        C.SW // 2, 305, center=True)
    txt("Press ENTER or R to try again", display.f_med, C.YELLOW,
        C.SW // 2, 395, center=True)


def draw_door_question(q: dict, subject_name: str, subject_color: tuple,
                       lives: int, flash_msg: str = "", flash_col=None,
                       panel_img=None, elapsed_secs: float = 0.0):
    """
    Split-screen question layout.

    Left half  (x 0–548)  – magical deep-space bg + question + answer buttons.
    Right half (x 552–1100) – panel_img (question_panel.png) or a decorative fallback.

    q            – question dict {q, opts, ans, cat}  (opts has 4 entries)
    subject_name – e.g. "Grammar"
    subject_color– (R, G, B) tint matching the door
    lives        – remaining lives
    flash_msg    – optional wrong-answer message
    flash_col    – colour for flash_msg
    panel_img    – pygame.Surface for the right panel (None = procedural)
    elapsed_secs – seconds since question appeared (drives live star rating)
    """
    # ── Compute current star rating from elapsed time ─────────────────────────
    if elapsed_secs <=  5: current_stars = 5
    elif elapsed_secs <= 10: current_stars = 4
    elif elapsed_secs <= 15: current_stars = 3
    elif elapsed_secs <= 20: current_stars = 2
    else:                    current_stars = 1
    if flash_col is None:
        flash_col = C.RED

    scr  = display.screen
    HALF = 548        # left panel width
    DIV  = 552        # x where right panel starts (4 px divider gap)

    # Clear the entire canvas first so the game stage doesn't show through
    scr.set_clip(None)
    scr.fill((2, 4, 20))

    # ═══════════════════════════════════════════════════════════════════════════
    # LEFT HALF — deep-space + circles + question
    # ═══════════════════════════════════════════════════════════════════════════

    # Clip drawing to the left half
    left_clip = pygame.Rect(0, 0, HALF, C.SH)
    scr.set_clip(left_clip)

    # ── Floating magical circles (x_base capped within left half) ────────────
    t = pygame.time.get_ticks() / 1000.0

    # (x_base, y_frac, radius, rise_speed, wobble_amp, wobble_freq, phase, (r,g,b,a))
    _CIRCLES = [
        (60,   0.85, 40, 55, 28, 0.60, 0.0, (20,  80, 255, 55)),
        (180,  0.70, 26, 75, 18, 0.90, 1.3, (60, 140, 255, 45)),
        (300,  0.92, 50, 40, 36, 0.45, 2.5, (10,  55, 200, 50)),
        (420,  0.78, 30, 65, 22, 0.75, 0.9, (80, 180, 255, 40)),
        (100,  0.55, 46, 45, 32, 0.55, 3.2, (30,  90, 220, 52)),
        (490,  0.40, 34, 60, 26, 0.80, 1.7, (90, 200, 255, 42)),
        (250,  0.30, 22, 80, 16, 1.10, 4.0, (50, 120, 240, 38)),
        (380,  0.60, 38, 50, 28, 0.65, 0.4, (25,  85, 215, 46)),
        (140,  0.20, 28, 70, 20, 0.95, 3.8, (70, 160, 255, 40)),
    ]

    for (bx, bfy, r, spd, wamp, wfreq, ph, col) in _CIRCLES:
        total_h = C.SH + r * 4
        drift   = (t * spd + ph * (C.SH / 60)) % total_h
        cy      = int(bfy * C.SH - drift + total_h) % total_h - r * 2
        cx      = int(bx + math.sin(t * wfreq + ph) * wamp)

        glow_r = r + 14
        glow   = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        glow_a = max(0, col[3] - 30)
        pygame.draw.circle(glow, (col[0], col[1], col[2], glow_a),
                           (glow_r, glow_r), glow_r)
        scr.blit(glow, (cx - glow_r, cy - glow_r))

        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, col, (r, r), r)
        hi_r = max(4, r // 3)
        pygame.draw.circle(surf, (200, 230, 255, min(255, col[3] + 60)),
                           (r - hi_r // 2, r - hi_r // 2), hi_r)
        scr.blit(surf, (cx - r, cy - r))

    # ── Vignette ──────────────────────────────────────────────────────────────
    vig = pygame.Surface((HALF, C.SH), pygame.SRCALPHA)
    vig.fill((0, 2, 18, 160))
    scr.blit(vig, (0, 0))

    # ── Subject title banner ──────────────────────────────────────────────────
    bw, bh = 360, 48
    bx     = (HALF - bw) // 2
    by     = 28
    pygame.draw.rect(scr, subject_color, (bx, by, bw, bh), border_radius=12)
    pygame.draw.rect(scr, C.GOLD,        (bx, by, bw, bh), border_radius=12, width=2)
    txt(subject_name.upper(), display.f_big, C.WHITE,
        HALF // 2, by + bh // 2 - 10, center=True, shadow=True)

    # Lives on the left, live star rating on the right (within left half)
    txt(f"Lives: {lives}", display.f_xs, C.YELLOW, 60, by + bh + 8)
    # Stars shrink in real time as seconds tick past each threshold
    _draw_stars(HALF // 2 + 60, by + bh + 14, current_stars, total=5, size=10)

    # Timer bar — fills red→yellow as time runs out (0–20 s shown, caps at 20)
    bar_w   = HALF - 32
    bar_h   = 5
    bar_x   = 16
    bar_y   = by + bh + 28
    filled  = max(0, 1.0 - min(elapsed_secs, 20) / 20)
    r_col   = int(255 * (1 - filled))
    g_col   = int(220 * filled)
    pygame.draw.rect(scr, (30, 30, 50),           (bar_x, bar_y, bar_w, bar_h), border_radius=2)
    if filled > 0:
        pygame.draw.rect(scr, (r_col, g_col, 20), (bar_x, bar_y, int(bar_w * filled), bar_h), border_radius=2)

    # ── Question panel ────────────────────────────────────────────────────────
    pw, ph = HALF - 32, 90
    px     = 16
    py     = 140

    pygame.draw.rect(scr, (10, 18, 58, 230), (px, py, pw, ph), border_radius=10)
    pygame.draw.rect(scr, C.GOLD,             (px, py, pw, ph), border_radius=10, width=2)

    lines  = wrap_text(q["q"], display.f_med, pw - 32)
    line_h = 26
    total_txt_h = len(lines) * line_h
    txt_y  = py + (ph - total_txt_h) // 2 + 2
    for line in lines:
        txt(line, display.f_med, C.WHITE, HALF // 2, txt_y, center=True)
        txt_y += line_h

    # ── 2 × 2 answer button grid (fits inside left half) ─────────────────────
    BTN_COLS = [
        (160,  40,  40),   # A – deep red
        ( 40,  80, 200),   # B – blue
        ( 25, 120,  60),   # C – green
        (130,  45, 180),   # D – purple
    ]
    LABELS = ["A", "B", "C", "D"]

    btn_w  = 250
    btn_h  = 60
    gap_x  = 12
    gap_y  = 10
    grid_w = btn_w * 2 + gap_x
    grid_x = (HALF - grid_w) // 2
    grid_y = py + ph + 18

    for i, opt in enumerate(q["opts"]):
        col2  = i % 2
        row2  = i // 2
        bx2   = grid_x + col2 * (btn_w + gap_x)
        by2   = grid_y + row2 * (btn_h + gap_y)

        pygame.draw.rect(scr, BTN_COLS[i], (bx2, by2, btn_w, btn_h), border_radius=10)
        pygame.draw.rect(scr, C.WHITE,     (bx2, by2, btn_w, btn_h), border_radius=10, width=2)

        badge_r = 14
        pygame.draw.circle(scr, (255, 255, 255, 80),
                           (bx2 + 22, by2 + btn_h // 2), badge_r)
        txt(LABELS[i], display.f_sm, C.WHITE,
            bx2 + 22, by2 + btn_h // 2 - 10, center=True, shadow=True)

        max_opt_w = btn_w - 50
        opt_lines = wrap_text(opt, display.f_sm, max_opt_w)
        opt_y = by2 + btn_h // 2 - (len(opt_lines) * 20) // 2
        for ol in opt_lines:
            txt(ol, display.f_sm, C.WHITE, bx2 + 44 + max_opt_w // 2,
                opt_y, center=True)
            opt_y += 20

    # ── Flash message + prompt ────────────────────────────────────────────────
    flash_y = grid_y + btn_h * 2 + gap_y + 8
    if flash_msg:
        txt(flash_msg, display.f_med, flash_col,
            HALF // 2, flash_y, center=True, shadow=True)
    prompt_y = flash_y + (32 if flash_msg else 0)
    txt("Press  A , B , C  or  D", display.f_sm, C.YELLOW,
        HALF // 2, prompt_y + 8, center=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # DIVIDER LINE
    # ═══════════════════════════════════════════════════════════════════════════
    scr.set_clip(None)
    pygame.draw.line(scr, C.GOLD, (DIV - 2, 0), (DIV - 2, C.SH), 2)

    # ═══════════════════════════════════════════════════════════════════════════
    # RIGHT HALF — PNG panel
    # ═══════════════════════════════════════════════════════════════════════════
    right_w = C.SW - DIV   # 548 px

    if panel_img is not None:
        # Scale the image to fill the right panel, preserving aspect ratio
        img_w, img_h = panel_img.get_size()
        scale        = min(right_w / img_w, C.SH / img_h)
        new_w        = int(img_w * scale)
        new_h        = int(img_h * scale)
        off_x        = DIV + (right_w - new_w) // 2
        off_y        = (C.SH - new_h) // 2
        scaled_img   = pygame.transform.smoothscale(panel_img, (new_w, new_h))
        scr.blit(scaled_img, (off_x, off_y))
    else:
        # Procedural fallback: dark panel with a gentle star-field + label
        right_surf = pygame.Surface((right_w, C.SH))
        right_surf.fill((6, 8, 30))
        # Small static stars
        import random as _rnd
        _rnd.seed(42)
        for _ in range(120):
            sx = _rnd.randint(0, right_w - 1)
            sy = _rnd.randint(0, C.SH - 1)
            br = _rnd.randint(80, 220)
            right_surf.set_at((sx, sy), (br, br, br))
        scr.blit(right_surf, (DIV, 0))
        txt("Place  question_panel.png", display.f_sm, (80, 100, 160),
            DIV + right_w // 2, C.SH // 2 - 12, center=True)
        txt("in the  assets/  folder", display.f_sm, (80, 100, 160),
            DIV + right_w // 2, C.SH // 2 + 12, center=True)


def draw_star_reveal(earned: int, anim_ms: int) -> None:
    """
    Epic full-screen popup shown after a correct door answer.

    Phases driven by anim_ms (ms since the state started):
      0 – 280 ms  : blinding gold screen-flash
      180 – 650 ms : "CORRECT!" scales + bounces in
      500 – 1400 ms: stars pop in one-by-one (each 180 ms apart)
      900 ms+      : "+100 pts" fades in
      1100 ms+     : "+N stars" fades in
      1800 ms+     : "Press any key…" pulses
    """
    scr = display.screen
    cx, cy = C.SW // 2, C.SH // 2

    # ── 1. Dark base ──────────────────────────────────────────────────────────
    scr.fill((5, 5, 18))

    # ── 2. Radial burst rays from centre ─────────────────────────────────────
    ray_count = 24
    ray_len   = 700
    # Slowly rotate over time for a dynamic feel
    ray_angle_off = anim_ms * 0.04
    burst_surf = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
    for i in range(ray_count):
        angle  = math.radians(360 / ray_count * i + ray_angle_off)
        # Width of each ray alternates wide / narrow
        half_w = math.radians(3.5 if i % 2 == 0 else 1.5)
        a1, a2 = angle - half_w, angle + half_w
        tip_x  = cx + math.cos(angle) * ray_len
        tip_y  = cy + math.sin(angle) * ray_len
        l1x = cx + math.cos(a1) * 40;  l1y = cy + math.sin(a1) * 40
        l2x = cx + math.cos(a2) * 40;  l2y = cy + math.sin(a2) * 40
        # Fade rays in during first 400 ms
        alpha = min(55, int(55 * anim_ms / 400))
        pygame.draw.polygon(burst_surf, (255, 215, 0, alpha),
                            [(l1x, l1y), (tip_x, tip_y), (l2x, l2y)])
    scr.blit(burst_surf, (0, 0))

    # ── 3. Gold screen flash (0–280 ms) ──────────────────────────────────────
    if anim_ms < 280:
        # Spikes at ~60 ms then decays
        peak   = 60
        if anim_ms <= peak:
            raw = anim_ms / peak
        else:
            raw = max(0.0, 1.0 - (anim_ms - peak) / (280 - peak))
        flash_a = int(raw ** 0.5 * 210)
        fl = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
        fl.fill((255, 230, 80, flash_a))
        scr.blit(fl, (0, 0))

    # ── 4. "CORRECT!" – scales + bounces in (180–650 ms) ─────────────────────
    t_txt = anim_ms - 180
    if t_txt >= 0:
        if t_txt < 220:
            scale = t_txt / 220 * 1.28       # overshoot to 128%
        elif t_txt < 330:
            scale = 1.28 - (t_txt - 220) / 110 * 0.28   # settle to 100%
        else:
            scale = 1.0

        base_surf = display.f_title.render("CORRECT!", True, (255, 240, 60))
        # Shadow layer
        shad_surf = display.f_title.render("CORRECT!", True, (80, 50, 0))
        bw, bh    = base_surf.get_size()
        sw2       = int(bw * scale); sh2 = int(bh * scale)
        if sw2 > 0 and sh2 > 0:
            scaled_shad = pygame.transform.smoothscale(shad_surf, (sw2, sh2))
            scaled_base = pygame.transform.smoothscale(base_surf, (sw2, sh2))
            scr.blit(scaled_shad, (cx - sw2 // 2 + 4, cy - sh2 // 2 - 90 + 4))
            scr.blit(scaled_base, (cx - sw2 // 2,     cy - sh2 // 2 - 90))

    # ── 5. Stars pop in one-by-one (500 – 500+4*180 = 1220 ms) ───────────────
    STAR_SIZE  = 42
    star_gap   = STAR_SIZE * 2 + 16
    star_total = 5
    star_row_w = star_total * star_gap - 16
    star_row_x = cx - star_row_w // 2 + STAR_SIZE

    for i in range(star_total):
        t_s = anim_ms - (500 + i * 180)
        if t_s < 0:
            # Not yet appeared — draw dim placeholder
            pts = _star_points(star_row_x + i * star_gap, cy + 10,
                               STAR_SIZE, STAR_SIZE * 0.42)
            pygame.draw.polygon(scr, (35, 35, 55), pts)
            continue

        # Scale bounce
        if t_s < 160:
            sc = t_s / 160 * 1.35
        elif t_s < 260:
            sc = 1.35 - (t_s - 160) / 100 * 0.35
        else:
            sc = 1.0

        R2 = int(STAR_SIZE * sc)
        if R2 < 2:
            continue

        sx = star_row_x + i * star_gap
        sy = cy + 10

        # Filled or empty based on earned count
        if i < earned:
            # Glow ring behind filled stars
            glow_surf = pygame.Surface((R2 * 4, R2 * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 215, 0, 50),
                               (R2 * 2, R2 * 2), R2 * 2)
            scr.blit(glow_surf, (sx - R2 * 2, sy - R2 * 2))
            col_fill = C.GOLD
            col_edge = (255, 255, 160)
        else:
            col_fill = (40, 40, 60)
            col_edge = (70, 70, 90)

        pts = _star_points(sx, sy, R2, R2 * 0.42)
        pygame.draw.polygon(scr, col_fill, pts)
        pygame.draw.polygon(scr, col_edge, pts, 2)

    # ── 6. "+100 pts" (900 ms+) ───────────────────────────────────────────────
    if anim_ms >= 900:
        alpha = min(255, int((anim_ms - 900) / 200 * 255))
        s = display.f_big.render("+100 pts", True, C.YELLOW)
        s.set_alpha(alpha)
        scr.blit(s, (cx - s.get_width() // 2, cy + 80))

    # ── 7. "+N stars" (1100 ms+) ─────────────────────────────────────────────
    if anim_ms >= 1100:
        alpha = min(255, int((anim_ms - 1100) / 200 * 255))
        star_str = "★" * earned
        s = display.f_big.render(f"+{earned} {star_str}", True, C.GOLD)
        s.set_alpha(alpha)
        scr.blit(s, (cx - s.get_width() // 2, cy + 124))

    # ── 8. "Press any key…" pulse (1800 ms+) ─────────────────────────────────
    if anim_ms >= 1800:
        pulse = abs(math.sin((anim_ms - 1800) * 0.004))
        col   = (int(160 + pulse * 95), int(160 + pulse * 95), int(50 + pulse * 30))
        txt("Press any key to continue", display.f_sm, col,
            cx, C.SH - 52, center=True)


def draw_gamewin(score: int):
    _overlay(0, 10, 38, 200)
    txt("YOU WIN!", display.f_title, C.GOLD,
        C.SW // 2, 168, center=True, shadow=True)
    txt("You mastered all 6 ESL levels!", display.f_big, C.CYAN,
        C.SW // 2, 252, center=True)
    txt(f"Final Score: {score}", display.f_big, C.YELLOW,
        C.SW // 2, 322, center=True)
    txt("Amazing work!  Keep learning English!", display.f_med, C.GREEN,
        C.SW // 2, 390, center=True)
    txt("Press ENTER or R to play again", display.f_sm, C.WHITE,
        C.SW // 2, 458, center=True)
