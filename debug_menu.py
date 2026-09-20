"""
debug_menu.py – Secret developer console.

Unlock sequence: LEFT LEFT LEFT RIGHT RIGHT RIGHT (any game state)

Once unlocked a small panel appears in the lower-right corner during gameplay.
Click it to open the command input, type a command, press ENTER to run it.
ESC closes the input without running anything.

Commands
────────
    b1 … b6   – jump straight to the boss fight for that world
    w1 … w6   – jump to world 1-6 (full reset, keeps grade)
    win       – instantly win the current boss fight (if in BOSS_FIGHT)
    heal      – restore hero HP to full (if in BOSS_FIGHT)

Public API
──────────
    check_seq(key)          – feed every KEYDOWN key here; unlocks on correct sequence
    handle_keydown(ev)      – feed KEYDOWN events when input is open
    handle_click(mx, my)    – feed MOUSEBUTTONDOWN canvas coords; returns True if consumed
    get_command() -> str    – returns pending command and clears it; "" if none
    is_capturing() -> bool  – True while the text input field is open
    draw(screen)            – render panel onto screen
    unlocked -> bool        – True once the cheat sequence has been entered
"""

import pygame
import constants as C

# ── Unlock sequence ───────────────────────────────────────────────────────────
_SEQ = [
    pygame.K_LEFT, pygame.K_LEFT, pygame.K_LEFT,
    pygame.K_RIGHT, pygame.K_RIGHT, pygame.K_RIGHT,
]
_seq_pos  = 0   # next expected index in _SEQ
unlocked  = False

# ── UI state ──────────────────────────────────────────────────────────────────
_input_open  = False
_input_text  = ""
_pending_cmd = ""
_blink_timer = 0   # cursor blink (frames)

# Panel and input rects (canvas-space)
_BTN_RECT   = pygame.Rect(C.SW - 116, C.SH - 30, 106, 22)
_INPUT_RECT = pygame.Rect(C.SW - 220, C.SH - 60, 210, 26)

# Colors
_COL_BG      = (14,  16,  32, 210)
_COL_BORDER  = (90, 100, 200, 220)
_COL_TEXT    = (180, 190, 255)
_COL_CURSOR  = (200, 210, 255)
_COL_HINT    = (90,  95, 140)


# ── Public ────────────────────────────────────────────────────────────────────

def check_seq(key: int) -> None:
    """Call with every KEYDOWN key. Unlocks the menu on the correct sequence."""
    global _seq_pos, unlocked
    if unlocked:
        return
    if key == _SEQ[_seq_pos]:
        _seq_pos += 1
        if _seq_pos >= len(_SEQ):
            unlocked  = True
            _seq_pos  = 0
            print("[debug] Debug menu unlocked.")
    else:
        # Partial reset: restart from 1 if the key restarts the sequence
        _seq_pos = 1 if key == _SEQ[0] else 0


def handle_keydown(ev: pygame.event.Event) -> None:
    """Feed KEYDOWN events while the input field is open."""
    global _input_text, _input_open, _pending_cmd

    if not _input_open:
        return

    if ev.key == pygame.K_RETURN:
        _pending_cmd = _input_text.strip().lower()
        _input_text  = ""
        _input_open  = False

    elif ev.key == pygame.K_ESCAPE:
        _input_text = ""
        _input_open = False

    elif ev.key == pygame.K_BACKSPACE:
        _input_text = _input_text[:-1]

    elif ev.unicode and ev.unicode.isprintable():
        if len(_input_text) < 20:
            _input_text += ev.unicode


def handle_click(mx: int, my: int) -> bool:
    """
    Process a left-click at canvas coords (mx, my).
    Returns True if the click was consumed by the debug menu.
    """
    global _input_open
    if not unlocked:
        return False
    if _BTN_RECT.collidepoint(mx, my):
        _input_open = not _input_open
        return True
    if _input_open and _INPUT_RECT.collidepoint(mx, my):
        return True   # absorb clicks inside the input field
    return False


def get_command() -> str:
    """Return the pending command string and clear it. Returns '' if none."""
    global _pending_cmd
    cmd, _pending_cmd = _pending_cmd, ""
    return cmd


def is_capturing() -> bool:
    """True while the text input field is open (suppresses normal key handling)."""
    return _input_open


def draw(screen: pygame.Surface) -> None:
    """Render the debug panel onto screen."""
    global _blink_timer
    if not unlocked:
        return

    _blink_timer += 1

    # ── Toggle button ─────────────────────────────────────────────────────────
    _draw_panel(screen, _BTN_RECT)
    try:
        font = pygame.font.SysFont("Consolas", 11)
    except Exception:
        font = pygame.font.SysFont(None, 14)

    lbl = font.render("[ DEBUG ]", True, _COL_TEXT)
    screen.blit(lbl, (_BTN_RECT.x + (_BTN_RECT.w - lbl.get_width()) // 2,
                      _BTN_RECT.y + (_BTN_RECT.h - lbl.get_height()) // 2))

    # ── Input field ───────────────────────────────────────────────────────────
    if _input_open:
        _draw_panel(screen, _INPUT_RECT)

        # Prompt + text
        display_text = "> " + _input_text
        cursor = "|" if (_blink_timer // 30) % 2 == 0 else " "
        full   = display_text + cursor

        txt_surf = font.render(full, True, _COL_CURSOR)
        tx = _INPUT_RECT.x + 6
        ty = _INPUT_RECT.y + (_INPUT_RECT.h - txt_surf.get_height()) // 2
        screen.blit(txt_surf, (tx, ty))

        # Hint line above the field
        hint = font.render("b1-b6  w1-w6  win  heal", True, _COL_HINT)
        screen.blit(hint, (_INPUT_RECT.x,
                            _INPUT_RECT.y - hint.get_height() - 3))


# ── Internal ──────────────────────────────────────────────────────────────────

def _draw_panel(screen: pygame.Surface, rect: pygame.Rect) -> None:
    surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    surf.fill(_COL_BG)
    pygame.draw.rect(surf, _COL_BORDER, surf.get_rect(), 1, border_radius=4)
    screen.blit(surf, (rect.x, rect.y))
