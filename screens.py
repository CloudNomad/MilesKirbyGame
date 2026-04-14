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


def draw_title(sel: int, save_exists: bool) -> None:
    """
    Main title / menu screen.

    sel         – currently highlighted item (0=New Game, 1=Load Game,
                  2=Options, 3=Credits)
    save_exists – if False, Load Game is greyed out
    """
    _overlay(0, 4, 22, 210)

    # ── Logo ──────────────────────────────────────────────────────────────────
    txt("KIRBY  ×  MILES MORALES", display.f_title, C.HOTPNK,
        C.SW // 2, 96, center=True, shadow=True)
    txt("ESL  Adventure", display.f_big, C.GOLD,
        C.SW // 2, 152, center=True, shadow=True)

    # Thin gold divider
    pygame.draw.line(display.screen, C.GOLD,
                     (C.SW // 2 - 260, 184), (C.SW // 2 + 260, 184), 2)

    # ── Menu box ──────────────────────────────────────────────────────────────
    mw, mh = 380, 248
    mx     = (C.SW - mw) // 2
    my     = 202
    pygame.draw.rect(display.screen, (10, 22, 70), (mx, my, mw, mh), border_radius=14)
    pygame.draw.rect(display.screen, C.GOLD,       (mx, my, mw, mh), border_radius=14, width=2)

    ITEMS = [
        ("NEW GAME",  True),
        ("LOAD GAME", save_exists),
        ("OPTIONS",   True),
        ("CREDITS",   True),
    ]

    item_h = 52
    for i, (label, enabled) in enumerate(ITEMS):
        iy     = my + 18 + i * item_h
        is_sel = (i == sel)

        if is_sel and enabled:
            # Highlight pill
            hcol = (40, 80, 200)
            pygame.draw.rect(display.screen, hcol,
                             (mx + 18, iy, mw - 36, 42), border_radius=8)
            pygame.draw.rect(display.screen, C.GOLD,
                             (mx + 18, iy, mw - 36, 42), border_radius=8, width=1)

        if not enabled:
            col = C.DKGRAY
        elif is_sel:
            col = C.GOLD
        else:
            col = C.WHITE

        txt(label, display.f_med, col, C.SW // 2, iy + 11, center=True)

    # ── Navigation hint ────────────────────────────────────────────────────────
    txt("W / S  or  ↑ ↓  to navigate    ENTER to select",
        display.f_xs, C.GRAY, C.SW // 2, C.SH - 30, center=True)


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

    cw, ch = 540, 200
    cx     = (C.SW - cw) // 2
    cy     = 168
    pygame.draw.rect(display.screen, (10, 22, 70), (cx, cy, cw, ch), border_radius=14)
    pygame.draw.rect(display.screen, C.GOLD,       (cx, cy, cw, ch), border_radius=14, width=2)

    txt("Developer", display.f_sm,  C.LGRAY, C.SW // 2, cy + 50,  center=True)
    txt("Mr. Joshua",  display.f_big,  C.GOLD,  C.SW // 2, cy + 84,  center=True, shadow=True)

    pygame.draw.line(display.screen, C.DKGRAY,
                     (cx + 40, cy + 126), (cx + cw - 40, cy + 126), 1)

    txt("Made with Python & Pygame", display.f_xs, C.GRAY, C.SW // 2, cy + 146, center=True)

    pulse = abs(math.sin(pygame.time.get_ticks() * 0.003))
    cv    = int(160 + pulse * 95)
    txt("Press  ESC  to go back", display.f_sm, (cv, cv, cv),
        C.SW // 2, cy + ch + 28, center=True)


def draw_grade_select(hover: int = 0):
    """
    Grade-selection screen.  hover = 1–6 highlights that card (use 0 for none).
    The player presses 1–6 to pick their grade.
    """
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


def draw_char_select(sel: int) -> None:
    """
    Character selection screen.
    sel: 0 = Kirby,  1 = Miles Morales
    """
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
    ]

    card_w, card_h = 360, 430
    gap    = 60
    total  = card_w * 2 + gap
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
        prev_cy = card_y + 160

        if i == 0:                        # Kirby
            _preview_kirby(prev_cx, prev_cy, assets.player_img)
        else:                             # Miles
            _preview_miles(prev_cx, prev_cy, assets.miles_img)

        # ── Name ────────────────────────────────────────────────────────────
        txt(ch["name"], display.f_big, ch["col"],
            mid, card_y + 300, center=True, shadow=True)

        # ── Description ─────────────────────────────────────────────────────
        for j, line in enumerate(ch["lines"]):
            col = C.WHITE if is_sel else C.GRAY
            txt(line, display.f_sm, col, mid, card_y + 338 + j * 22, center=True)

        # ── Key hint ─────────────────────────────────────────────────────────
        hint_col = C.GOLD if is_sel else (100, 100, 120)
        txt(ch["key"], display.f_sm, hint_col,
            mid, card_y + card_h - 26, center=True)

    # Bottom instruction
    txt("◄ ►  or  1 / 2  to choose        Enter to confirm",
        display.f_sm, (160, 160, 200), C.SW // 2, C.SH - 24, center=True)


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


def draw_lvl_done(lvl: int, score: int):
    _overlay(0, 20, 0, 185)
    txt(f"Level {lvl} Complete!", display.f_title, C.GREEN,
        C.SW // 2, 195, center=True, shadow=True)
    txt(f"Score: {score}", display.f_big, C.GOLD,
        C.SW // 2, 275, center=True)
    if lvl < C.TOTAL:
        txt(f"Next: Level {lvl + 1}  –  Grade {lvl + 1} challenges!",
            display.f_med, C.CYAN, C.SW // 2, 345, center=True)
    txt("Press ENTER or SPACE to continue", display.f_sm, C.YELLOW,
        C.SW // 2, 425, center=True)


def draw_gameover(score: int):
    _overlay(38, 0, 0, 200)
    txt("Game Over", display.f_title, C.RED,
        C.SW // 2, 215, center=True, shadow=True)
    txt(f"Final Score: {score}", display.f_big, C.GOLD,
        C.SW // 2, 305, center=True)
    txt("Press ENTER or R to try again", display.f_med, C.YELLOW,
        C.SW // 2, 395, center=True)


def draw_door_question(q: dict, subject_name: str, subject_color: tuple,
                       lives: int, flash_msg: str = "", flash_col=None):
    """
    Full-screen question screen with magical floating blue circles.

    q            – question dict {q, opts, ans, cat}  (opts has 4 entries)
    subject_name – e.g. "Grammar"
    subject_color– (R, G, B) tint matching the door
    lives        – remaining lives
    flash_msg    – optional wrong-answer message
    flash_col    – colour for flash_msg
    """
    if flash_col is None:
        flash_col = C.RED

    scr = display.screen

    # ── Deep-space background ─────────────────────────────────────────────────
    scr.fill((2, 4, 20))

    # ── Floating magical circles ──────────────────────────────────────────────
    t = pygame.time.get_ticks() / 1000.0

    # (x_base, y_frac, radius, rise_speed, wobble_amp, wobble_freq, phase, (r,g,b,a))
    _CIRCLES = [
        (80,   0.85, 48, 55, 35, 0.6,  0.0,  (20,  80, 255, 55)),
        (200,  0.70, 30, 75, 22, 0.9,  1.3,  (60, 140, 255, 45)),
        (360,  0.92, 62, 40, 45, 0.45, 2.5,  (10,  55, 200, 50)),
        (500,  0.78, 36, 65, 28, 0.75, 0.9,  (80, 180, 255, 40)),
        (640,  0.88, 54, 45, 38, 0.55, 3.2,  (30,  90, 220, 52)),
        (780,  0.75, 40, 60, 32, 0.80, 1.7,  (90, 200, 255, 42)),
        (920,  0.90, 58, 35, 50, 0.40, 2.1,  (15,  60, 190, 48)),
        (150,  0.50, 26, 80, 18, 1.10, 4.0,  (50, 120, 240, 38)),
        (1000, 0.60, 44, 50, 30, 0.65, 0.4,  (25,  85, 215, 46)),
        (450,  0.40, 33, 70, 24, 0.95, 3.8,  (70, 160, 255, 40)),
        (700,  0.55, 20, 90, 15, 1.20, 1.0,  (100,210, 255, 35)),
        (300,  0.30, 50, 38, 40, 0.50, 2.9,  (10,  50, 180, 44)),
    ]

    for (bx, bfy, r, spd, wamp, wfreq, ph, col) in _CIRCLES:
        total_h = C.SH + r * 4
        drift   = (t * spd + ph * (C.SH / 60)) % total_h
        cy      = int(bfy * C.SH - drift + total_h) % total_h - r * 2
        cx      = int(bx + math.sin(t * wfreq + ph) * wamp)

        # Outer glow (large, very transparent)
        glow_r = r + 14
        glow   = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        glow_a = max(0, col[3] - 30)
        pygame.draw.circle(glow, (col[0], col[1], col[2], glow_a),
                           (glow_r, glow_r), glow_r)
        scr.blit(glow, (cx - glow_r, cy - glow_r))

        # Main circle
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, col, (r, r), r)
        # Inner highlight
        hi_r = max(4, r // 3)
        pygame.draw.circle(surf, (200, 230, 255, min(255, col[3] + 60)),
                           (r - hi_r // 2, r - hi_r // 2), hi_r)
        scr.blit(surf, (cx - r, cy - r))

    # ── Dark vignette overlay so text is readable ─────────────────────────────
    _overlay(0, 2, 18, 170)

    # ── Subject title banner ──────────────────────────────────────────────────
    bw, bh = 420, 54
    bx, by = (C.SW - bw) // 2, 34
    pygame.draw.rect(scr, subject_color, (bx, by, bw, bh), border_radius=12)
    pygame.draw.rect(scr, C.GOLD,        (bx, by, bw, bh), border_radius=12, width=2)
    txt(subject_name.upper(), display.f_big, C.WHITE,
        C.SW // 2, by + bh // 2 - 10, center=True, shadow=True)

    txt(f"Lives: {lives}", display.f_xs, C.YELLOW,
        C.SW // 2, by + bh + 10, center=True)

    # ── Question panel ────────────────────────────────────────────────────────
    pw, ph = 860, 106
    px     = (C.SW - pw) // 2
    py     = 118

    pygame.draw.rect(scr, (10, 18, 58, 230), (px, py, pw, ph), border_radius=12)
    pygame.draw.rect(scr, C.GOLD,             (px, py, pw, ph), border_radius=12, width=2)

    lines = wrap_text(q["q"], display.f_med, pw - 48)
    line_h = 30
    total_txt_h = len(lines) * line_h
    txt_y = py + (ph - total_txt_h) // 2 + 2
    for line in lines:
        txt(line, display.f_med, C.WHITE, C.SW // 2, txt_y, center=True)
        txt_y += line_h

    # ── 2 × 2 answer button grid ──────────────────────────────────────────────
    BTN_COLS = [
        (160,  40,  40),   # A – deep red
        ( 40,  80, 200),   # B – blue
        ( 25, 120,  60),   # C – green
        (130,  45, 180),   # D – purple
    ]
    LABELS = ["A", "B", "C", "D"]

    btn_w  = 420
    btn_h  = 68
    gap_x  = 16
    gap_y  = 12
    grid_w = btn_w * 2 + gap_x
    grid_x = (C.SW - grid_w) // 2
    grid_y = py + ph + 18

    for i, opt in enumerate(q["opts"]):
        col  = i % 2          # 0 = left,  1 = right
        row  = i // 2         # 0 = top,   1 = bottom
        bx2  = grid_x + col * (btn_w + gap_x)
        by2  = grid_y + row * (btn_h + gap_y)

        pygame.draw.rect(scr, BTN_COLS[i], (bx2, by2, btn_w, btn_h), border_radius=10)
        pygame.draw.rect(scr, C.WHITE,     (bx2, by2, btn_w, btn_h), border_radius=10, width=2)

        # Key badge on left edge
        badge_r = 16
        pygame.draw.circle(scr, (255, 255, 255, 80),
                           (bx2 + 26, by2 + btn_h // 2), badge_r)
        txt(LABELS[i], display.f_sm, C.WHITE,
            bx2 + 26, by2 + btn_h // 2 - 10, center=True, shadow=True)

        # Option text (truncate long lines to fit)
        max_opt_w = btn_w - 62
        opt_lines = wrap_text(opt, display.f_sm, max_opt_w)
        opt_y = by2 + btn_h // 2 - (len(opt_lines) * 20) // 2
        for ol in opt_lines:
            txt(ol, display.f_sm, C.WHITE, bx2 + 54 + max_opt_w // 2,
                opt_y, center=True)
            opt_y += 20

    # ── Flash message ─────────────────────────────────────────────────────────
    flash_y = grid_y + btn_h * 2 + gap_y + 10
    if flash_msg:
        txt(flash_msg, display.f_big, flash_col,
            C.SW // 2, flash_y, center=True, shadow=True)

    # ── Prompt ───────────────────────────────────────────────────────────────
    prompt_y = flash_y + (40 if flash_msg else 0)
    txt("Press  A , B , C  or  D  to answer", display.f_sm, C.YELLOW,
        C.SW // 2, prompt_y + 12, center=True)


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
