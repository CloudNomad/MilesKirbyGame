"""
boss_fight.py – Turn-based RPG boss combat screen.

Layout (1100 × 650)
────────────────────
  Top strip  : HP bars for hero (left) and boss (right)
  Middle     : hero sprite (left), boss sprite (right)
  Log panel  : last two battle messages
  Action menu: 2 × 2 grid — Attack / Magic / Item / Defend

Turn order
──────────
  Player picks an action → result resolves → boss decides whether to attack.
  Boss attacks every 2-3 turns normally, every 1-2 turns when HP < 33 %.

Public API
──────────
    reset(char, lvl, boss_img)  – init the fight
    handle_key(key)             – call from KEYDOWN handler (game.py)
    update()                    – call every frame
    draw()                      – render onto display.screen
    done                        – True when combat is over
    result                      – "win" or "lose"
"""

import os
import sys
import random
import pygame

import display
import constants as C
import assets

# ── Combat parameters ──────────────────────────────────────────────────────────
_HERO_MAX_HP    = 100
_BOSS_MAX_HP    = 150
_MAGIC_USES     = 5
_ITEM_USES      = 3

_ATK_DMG        = (15, 25)   # (min, max) player attack
_MAGIC_DMG      = (30, 45)   # player magic
_ITEM_HEAL      = (25, 35)   # potion heal
_BOSS_DMG_NORM  = (12, 25)   # boss attack, normal
_BOSS_DMG_RAGE  = (20, 38)   # boss attack, enraged (< 33 % HP)

_ANIM_FRAMES    = 90         # pause between actions (1.5 s at 60 fps)
_RESULT_FRAMES  = 180        # hold win/lose overlay before allowing continue

# ── Layout ─────────────────────────────────────────────────────────────────────
_HERO_CX  = 210
_BOSS_CX  = 870
_SPRITE_Y = 220
_LOG_X    = 60;  _LOG_Y = 370;  _LOG_W = C.SW - 120;  _LOG_H = 78
_MENU_X   = (C.SW - (2 * 210 + 24)) // 2    # centre the 2×2 grid
_MENU_Y   = 468
_BTN_W    = 210;  _BTN_H = 56;  _BTN_GAP = 24

# ── State ──────────────────────────────────────────────────────────────────────
_phase          = "select"   # "select" | "player_anim" | "boss_anim" | "win" | "lose"
_cursor_row     = 0
_cursor_col     = 0

_hero_hp        = _HERO_MAX_HP
_boss_hp        = _BOSS_MAX_HP
_magic_left     = _MAGIC_USES
_item_left      = _ITEM_USES
_defending      = False       # True if player chose Defend last turn

_boss_cd        = 0           # turns until boss next attacks
_boss_threshold = 2           # chosen each time boss attacks

_log: list      = []
_anim_timer     = 0
_result_timer   = 0

_hero_surf      = None        # scaled hero Surface
_boss_surf      = None        # scaled boss Surface
_bg_surf        = None

done   = False
result = "win"

_BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

_ACTIONS = [["Attack", "Magic"], ["Item", "Defend"]]


# ── Public ─────────────────────────────────────────────────────────────────────

def reset(char: str, lvl: int, boss_img: pygame.Surface | None = None) -> None:
    global _phase, _cursor_row, _cursor_col
    global _hero_hp, _boss_hp, _magic_left, _item_left, _defending
    global _boss_cd, _boss_threshold, _log, _anim_timer, _result_timer
    global _hero_surf, _boss_surf, _bg_surf, done, result

    _phase         = "select"
    _cursor_row    = 0
    _cursor_col    = 0
    _hero_hp       = _HERO_MAX_HP
    _boss_hp       = _BOSS_MAX_HP
    _magic_left    = _MAGIC_USES
    _item_left     = _ITEM_USES
    _defending     = False
    _boss_cd       = random.randint(2, 3)
    _boss_threshold = _boss_cd
    _log           = ["The ancient spirit stirs... prepare yourself!"]
    _anim_timer    = 0
    _result_timer  = 0
    done           = False
    result         = "win"

    # ── Hero sprite ───────────────────────────────────────────────────────────
    base = assets.miles_img if char == "miles" else assets.player_img
    if base:
        _hero_surf = pygame.transform.smoothscale(base, (150, 150))
    else:
        _hero_surf = None

    # ── Boss sprite ───────────────────────────────────────────────────────────
    bi = boss_img
    if bi is None:
        for fname in (f"boss{lvl}.png", "boss.png"):
            path = os.path.join(_BASE_DIR, "assets", fname)
            if os.path.isfile(path):
                try:
                    raw  = pygame.image.load(path).convert_alpha()
                    ow, oh = raw.get_size()
                    bh   = 220
                    bw   = max(1, int(ow * bh / oh))
                    bi   = pygame.transform.smoothscale(raw, (bw, bh))
                except pygame.error:
                    pass
                break

    if bi is not None:
        # Fit inside 280 × 260 box
        mw, mh = 280, 260
        ow, oh = bi.get_size()
        scale  = min(mw / ow, mh / oh)
        _boss_surf = pygame.transform.smoothscale(
            bi, (max(1, int(ow * scale)), max(1, int(oh * scale)))
        )
    else:
        _boss_surf = None

    # ── Dark-tinted background ────────────────────────────────────────────────
    _bg_surf = None
    for fname in (f"boss_bg{lvl}.png", "boss_bg.png"):
        path = os.path.join(_BASE_DIR, "assets", fname)
        if os.path.isfile(path):
            try:
                raw      = pygame.image.load(path).convert()
                _bg_surf = pygame.transform.smoothscale(raw, (C.SW, C.SH))
            except pygame.error:
                pass
            break


def handle_key(key: int) -> None:
    global _cursor_row, _cursor_col

    if _phase == "select":
        if key in (pygame.K_LEFT,  pygame.K_a):
            _cursor_col = 1 - _cursor_col
        elif key in (pygame.K_RIGHT, pygame.K_d):
            _cursor_col = 1 - _cursor_col
        elif key in (pygame.K_UP,   pygame.K_w):
            _cursor_row = 1 - _cursor_row
        elif key in (pygame.K_DOWN, pygame.K_s):
            _cursor_row = 1 - _cursor_row
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            _confirm_action()


def update() -> None:
    global _phase, _anim_timer, _result_timer, _boss_cd, _boss_threshold
    global done, result

    if _phase == "player_anim":
        _anim_timer += 1
        if _anim_timer >= _ANIM_FRAMES:
            _anim_timer = 0
            _boss_cd   -= 1
            if _boss_cd <= 0:
                enraged       = _boss_hp < _BOSS_MAX_HP * 0.33
                _boss_threshold = random.randint(1, 2) if enraged else random.randint(2, 3)
                _boss_cd      = _boss_threshold
                _do_boss_attack()
            else:
                _phase = "select"

    elif _phase == "boss_anim":
        _anim_timer += 1
        if _anim_timer >= _ANIM_FRAMES:
            _anim_timer = 0
            if _hero_hp <= 0:
                done   = True
                result = "lose"
                _phase = "lose"
            else:
                _phase = "select"

    elif _phase in ("win", "lose"):
        _result_timer += 1


def draw() -> None:
    scr = display.screen
    scr.fill((8, 5, 22))

    # Background (darkened)
    if _bg_surf:
        veil = pygame.Surface((C.SW, C.SH))
        veil.fill((0, 0, 0))
        veil.set_alpha(155)
        scr.blit(_bg_surf, (0, 0))
        scr.blit(veil,     (0, 0))

    # ── HP bars ───────────────────────────────────────────────────────────────
    _draw_hp_bar(scr, 20,          14, 320, 20, _hero_hp, _HERO_MAX_HP,
                 (50, 210, 80),  "Hero",  right_align=False)
    _draw_hp_bar(scr, C.SW - 340, 14, 320, 20, _boss_hp, _BOSS_MAX_HP,
                 (200, 50, 50), "Boss",  right_align=True)

    # Resource counters
    ctr = display.f_xs.render(
        f"Magic: {_magic_left}/{_MAGIC_USES}    Items: {_item_left}/{_ITEM_USES}",
        True, (170, 185, 255))
    scr.blit(ctr, (C.SW // 2 - ctr.get_width() // 2, 38))

    # ── Sprites ───────────────────────────────────────────────────────────────
    if _hero_surf:
        hx = _HERO_CX - _hero_surf.get_width()  // 2
        hy = _SPRITE_Y - _hero_surf.get_height() // 2
        scr.blit(_hero_surf, (hx, hy))
    else:
        pygame.draw.circle(scr, (80, 140, 255), (_HERO_CX, _SPRITE_Y), 55)

    if _boss_surf:
        bx = _BOSS_CX - _boss_surf.get_width()  // 2
        by = _SPRITE_Y - _boss_surf.get_height() // 2
        scr.blit(_boss_surf, (bx, by))
    else:
        pygame.draw.circle(scr, (180, 50, 50), (_BOSS_CX, _SPRITE_Y), 75)

    # Defending indicator
    if _defending:
        sh = display.f_xs.render("[ DEFENDING ]", True, (100, 200, 255))
        scr.blit(sh, (_HERO_CX - sh.get_width() // 2,
                      _SPRITE_Y + 90))

    # ── Battle log ────────────────────────────────────────────────────────────
    log_panel = pygame.Surface((_LOG_W, _LOG_H), pygame.SRCALPHA)
    log_panel.fill((0, 0, 20, 210))
    pygame.draw.rect(log_panel, (90, 80, 180, 200),
                     log_panel.get_rect(), 1, border_radius=6)
    scr.blit(log_panel, (_LOG_X, _LOG_Y))
    lh = display.f_sm.get_linesize() + 2
    for i, line in enumerate(_log[-2:]):
        ls = display.f_sm.render(line, True, (220, 225, 255))
        scr.blit(ls, (_LOG_X + 14, _LOG_Y + 10 + i * lh))

    # ── Action menu ───────────────────────────────────────────────────────────
    if _phase == "select":
        labels = [
            [f"Attack",            f"Magic  ({_magic_left})"],
            [f"Item  ({_item_left})", f"Defend"],
        ]
        for row in range(2):
            for col in range(2):
                bx  = _MENU_X + col * (_BTN_W + _BTN_GAP)
                by  = _MENU_Y + row * (_BTN_H + _BTN_GAP)
                sel = (_cursor_row == row and _cursor_col == col)
                ok  = _is_available(_ACTIONS[row][col])

                if not ok:
                    fill = (18, 18, 30, 180);  border = (45, 45, 65, 160)
                elif sel:
                    fill = (50, 70, 175, 230);  border = (200, 220, 255, 255)
                else:
                    fill = (20, 25, 75, 210);   border = (85, 90, 170, 200)

                btn = pygame.Surface((_BTN_W, _BTN_H), pygame.SRCALPHA)
                btn.fill(fill)
                pygame.draw.rect(btn, border, btn.get_rect(), 2, border_radius=7)
                scr.blit(btn, (bx, by))

                txt_col = (255, 240, 80) if (sel and ok) else \
                          (185, 195, 230) if ok else (65, 65, 85)
                prefix  = ">> " if sel else "   "
                lbl = display.f_sm.render(prefix + labels[row][col], True, txt_col)
                scr.blit(lbl, (bx + 12, by + (_BTN_H - lbl.get_height()) // 2))

        hint = display.f_xs.render(
            "Arrow keys to choose   ENTER / SPACE to confirm", True, (110, 115, 155))
        scr.blit(hint, (C.SW // 2 - hint.get_width() // 2, _MENU_Y + 2 * _BTN_H + _BTN_GAP + 8))

    elif _phase in ("player_anim", "boss_anim"):
        wait = display.f_sm.render("...", True, (140, 145, 185))
        scr.blit(wait, (C.SW // 2 - wait.get_width() // 2, _MENU_Y + 40))

    # ── Win / Lose overlay ────────────────────────────────────────────────────
    if _phase in ("win", "lose"):
        ov = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 170))
        scr.blit(ov, (0, 0))

        font = pygame.font.SysFont("Arial", 72, bold=True)
        if _phase == "win":
            msg, col = "Victory!", (255, 215, 50)
        else:
            msg, col = "Defeated...", (210, 55, 55)

        ms = font.render(msg, True, col)
        scr.blit(ms, (C.SW // 2 - ms.get_width() // 2, C.SH // 2 - 60))

        if _result_timer > 90:
            sub = display.f_med.render("Press any key to continue", True, (190, 195, 220))
            scr.blit(sub, (C.SW // 2 - sub.get_width() // 2, C.SH // 2 + 30))


# ── Internal ───────────────────────────────────────────────────────────────────

def _is_available(action: str) -> bool:
    if action == "Magic": return _magic_left > 0
    if action == "Item":  return _item_left  > 0
    return True


def _confirm_action() -> None:
    global _phase, _anim_timer, _defending
    global _hero_hp, _boss_hp, _magic_left, _item_left
    global done, result

    action = _ACTIONS[_cursor_row][_cursor_col]
    if not _is_available(action):
        _log.append("Nothing left — choose another action!")
        return

    _defending  = False
    _anim_timer = 0

    if action == "Attack":
        dmg      = random.randint(*_ATK_DMG)
        _boss_hp = max(0, _boss_hp - dmg)
        _log.append(f"You strike hard! The boss takes {dmg} damage.")

    elif action == "Magic":
        _magic_left -= 1
        dmg          = random.randint(*_MAGIC_DMG)
        _boss_hp     = max(0, _boss_hp - dmg)
        _log.append(f"A powerful spell erupts! {dmg} damage!")

    elif action == "Item":
        _item_left -= 1
        heal        = random.randint(*_ITEM_HEAL)
        _hero_hp    = min(_HERO_MAX_HP, _hero_hp + heal)
        _log.append(f"You drink a potion and recover {heal} HP.")

    elif action == "Defend":
        _defending = True
        _log.append("You raise your guard! Incoming damage halved.")

    # Check boss defeat right away
    if _boss_hp <= 0:
        _log.append("The spirit crumbles... you have won!")
        done   = True
        result = "win"
        _phase = "win"
        return

    _phase = "player_anim"


def _do_boss_attack() -> None:
    global _hero_hp, _anim_timer, _phase, _defending

    enraged  = _boss_hp < _BOSS_MAX_HP * 0.33
    base_dmg = random.randint(*(_BOSS_DMG_RAGE if enraged else _BOSS_DMG_NORM))

    if _defending:
        dmg = max(1, int(base_dmg * 0.45))
        _log.append(f"The boss strikes! Your guard absorbs the blow — {dmg} damage.")
        _defending = False
    else:
        dmg    = base_dmg
        prefix = "The spirit RAGES! " if enraged else "The boss attacks! "
        _log.append(f"{prefix}You take {dmg} damage!")

    _hero_hp    = max(0, _hero_hp - dmg)
    _anim_timer = 0
    _phase      = "boss_anim"


def _draw_hp_bar(scr, x, y, w, h, hp, max_hp, color, label, right_align):
    filled = max(0, int(w * hp / max_hp))
    ratio  = hp / max_hp if max_hp else 0

    lbl = display.f_xs.render(f"{label}  {hp} / {max_hp}", True, (200, 210, 235))
    lbl_y = y - lbl.get_height() - 2
    if right_align:
        scr.blit(lbl, (x + w - lbl.get_width(), lbl_y))
    else:
        scr.blit(lbl, (x, lbl_y))

    pygame.draw.rect(scr, (28, 28, 48), (x, y, w, h), border_radius=4)
    if filled:
        bar_col = (220, 50, 50) if ratio < 0.3 else \
                  (200, 175, 30) if ratio < 0.6 else color
        pygame.draw.rect(scr, bar_col, (x, y, filled, h), border_radius=4)
    pygame.draw.rect(scr, (75, 80, 120), (x, y, w, h), 1, border_radius=4)
