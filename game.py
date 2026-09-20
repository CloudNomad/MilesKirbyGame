"""
game.py – Main entry point and game loop.

Module map
──────────
constants.py   – colours, sizes, layout values, game-state IDs
display.py     – pygame init, screen surface, clock, fonts
questions.py   – question pools (Grammar / Vocabulary / Science) + bonus pool
utils.py       – txt(), wrap_text(), draw_hatch()
assets.py      – PNG loader  (put images in assets/ folder)
music.py       – background music  (put tracks in assets/music/)
player.py      – Player class
door.py        – Door class
key_item.py    – KeyItem class
background.py  – draw_bg()
hud.py         – draw_hud()
screens.py     – overlay screens (intro, door question, bonus, level done, …)
level.py       – new_level_data()
game.py        – this file: event loop + state machine

Door question flow
──────────────────
  Player walks into an unlocked, incomplete door:
    → FADE_OUT  (alpha 0 → 255 over ~28 frames)
    → DOOR_QUESTION  (split-screen question; level music continues)
      • correct  → door marked completed, +100 pts, FADE_IN
      • wrong    → lives -1, flash message, stay on DOOR_QUESTION
    → FADE_IN   (alpha 255 → 0 over ~28 frames)
    → PLAY  (or LVLDONE if all doors are completed)

Level complete: all 3 (non-locked at start, now unlocked) doors answered → LVLDONE

Music controls (work in any state)
────────────────────────────────────
  M  – mute / unmute
  N  – next track
  B  – previous track
  ]  – volume up  (+10 %)
  [  – volume down (−10 %)
"""
import sys
import math
import pygame

import display
import constants as C
import assets
import music
from background import draw_bg
from hud        import draw_hud
from screens    import (draw_splash, draw_title, draw_title_options,
                        draw_title_credits, draw_char_select, draw_grade_select,
                        draw_intro, draw_door_question, draw_star_reveal,
                        draw_bonus_q, draw_bonus_res, draw_lvl_done,
                        draw_gameover, draw_gamewin,
                        draw_tutorial_prompt, draw_tutorial)
import save     as savegame
import sounds   as sfx
import cutscene
import cutscene2
import intro_fade
import stage_transition
import char_cutscene
import boss_cutscene
import boss_fight
import debug_menu
import secret_stage
from player     import Player
from level      import new_level_data, random_bonus_question
from questions  import get_door_question, UHYUN_QS


# ─── Helpers ──────────────────────────────────────────────────────────────────
def _build_level(lvl, character="kirby"):
    doors, key_items = new_level_data(lvl)
    player = Player(60, C.SH // 2, character)
    return player, doors, key_items


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    display.init("Kirby x Miles: ESL Adventure", C.FPS)
    music.init()
    assets.load_all()
    sfx.init()

    lvl            = 1
    stage          = 1        # stage within current world (1-5); 5 → world done
    score          = 0
    selected_grade = 0        # set on grade-select screen; 0 = not yet chosen
    selected_char     = "kirby"  # set on char-select screen: "kirby", "miles", "secret1", "secret2"
    char_sel          = 0        # 0=Kirby  1=Miles  2=Secret (cursor on char-select screen)
    secret_char_popup = False    # True when secret characters sub-panel is open
    secret_char_sel   = 0        # 0-5 slot highlighted inside secret popup
    state          = C.INTRO_FADE
    # intro_fade.reset() is called just before the game loop (see below) so the
    # sentence timer starts at the first real frame, not during slow initialisation.

    # ── Title / options menu state ─────────────────────────────────────────────
    title_sel      = 0   # 0=New Game  1=Load Game  2=Options  3=Credits
    opts_sel       = 0   # 0=Music Vol  1=Sound Vol  2=Music Track  3=Display Mode  4=Back
    title_enter_ms = 0   # ticks when TITLE state was last entered (for flash-in)
    _prev_state    = None

    player, doors, key_items = _build_level(lvl, selected_char)

    # ── Per-level question + completion tracking ───────────────────────────────
    door_questions  = {}   # door_num → question dict (drawn on first touch)
    doors_completed = set()  # door nums answered correctly this level
    used_ids        = set()  # id()s of questions already seen this world (no-repeat)

    # ── Flash message ─────────────────────────────────────────────────────────
    flash_msg   = ""
    flash_timer = 0
    flash_col   = C.WHITE

    # ── Fade / door-question state ─────────────────────────────────────────────
    fade_alpha       = 0     # 0 = transparent, 255 = fully black
    active_door      = None  # Door object being questioned
    active_q         = None  # question dict for active door
    stage_track_idx  = 0     # music track index when we last entered PLAY
    q_start_time     = 0     # get_ticks() when DOOR_QUESTION screen first appeared

    # ── Star rank tracking ────────────────────────────────────────────────────
    level_stars        = 0   # stars earned answering doors this level
    total_stars        = 0   # accumulated across all levels (never reset mid-run)
    last_earned_stars  = 0   # stars from the most recent correct answer
    correct_anim_start = 0   # get_ticks() when DOOR_CORRECT began

    # ── Bonus round ────────────────────────────────────────────────────────────
    bonus_q   = None
    bonus_won = None
    b_timer   = 0

    # ── Tutorial ──────────────────────────────────────────────────────────────
    tutorial_page = 0   # current tutorial page (0-3)
    tutorial_sel  = 0   # Y/N selection on prompt screen (0=Yes, 1=No)

    # ── Secret stage ─────────────────────────────────────────────────────────
    secret_return_pos  = (C.SW // 2, C.SH // 2)   # player pos to restore on exit
    secret_q_idx       = 0                          # current question index (0-4)
    secret_answers     = []                          # True/False per question answered
    secret_q_sel       = -1                          # last chosen answer index (-1 = none)
    # fade routing: "secret_enter" | "secret_fadein" | "portal_enter" | None
    _fade_target       = None

    # ── Save indicator ────────────────────────────────────────────────────────
    save_timer    = 0   # counts down from 120 (2 s) after each autosave

    # ── Local helpers ─────────────────────────────────────────────────────────
    def flash(msg, col=C.WHITE, dur=110):
        nonlocal flash_msg, flash_timer, flash_col
        flash_msg = msg; flash_timer = dur; flash_col = col

    def _calc_stars(elapsed_ms: int) -> int:
        s = elapsed_ms / 1000.0
        if s <=  5: return 5
        if s <= 10: return 4
        if s <= 15: return 3
        if s <= 20: return 2
        return 1

    def full_reset(new_lvl, new_score, new_lives, keep_grade=True):
        nonlocal lvl, stage, score, state, player, doors, key_items
        nonlocal door_questions, doors_completed, used_ids, selected_grade
        nonlocal flash_msg, flash_timer, fade_alpha
        nonlocal active_door, active_q, stage_track_idx
        nonlocal bonus_q, bonus_won, title_sel
        nonlocal level_stars, total_stars, save_timer
        lvl   = new_lvl
        stage = 1
        score = new_score
        player, doors, key_items = _build_level(lvl, selected_char)
        player.lives     = new_lives
        door_questions   = {}
        doors_completed  = set()
        used_ids         = set()
        flash_msg        = ""
        flash_timer      = 0
        fade_alpha       = 0
        active_door      = None
        active_q         = None
        music.play(new_lvl - 1)          # world 1 = index 0, world 2 = index 1, …
        stage_track_idx  = new_lvl - 1
        bonus_q          = None
        bonus_won        = None
        title_sel        = 0
        level_stars      = 0             # fresh star count for each world
        save_timer       = 0
        if not keep_grade:
            total_stars  = 0            # full game restart — wipe total
        if keep_grade and selected_grade:
            state = C.PLAY
        else:
            selected_grade = 0
            state = C.TITLE

    def _advance_stage():
        """Reset doors/keys for the next stage within the same world."""
        nonlocal stage, doors, key_items, door_questions, doors_completed
        nonlocal flash_msg, flash_timer, state
        stage += 1
        doors, key_items = new_level_data(lvl)
        player.x  = 60.0
        player.y  = float(C.SH // 2)
        player.vx = player.vy = 0
        player.keys = []
        door_questions  = {}
        doors_completed = set()
        flash_msg  = ""
        flash_timer = 0
        state = C.PLAY

    def _draw_secret_overlay(cur_state, q_idx, answers):
        """Draw the SECRET_SELECT or SECRET_QUIZ panel over the secret stage."""
        scr = display.screen

        # Semi-transparent dark backdrop
        overlay = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        scr.blit(overlay, (0, 0))

        if cur_state == C.SECRET_SELECT:
            # ── Title ──────────────────────────────────────────────────────────
            title = display.f_big.render("SECRET  STAGE  SELECT", True, (210, 150, 255))
            scr.blit(title, (C.SW // 2 - title.get_width() // 2, 40))

            # ── 10 boxes (2 columns × 5 rows) ─────────────────────────────────
            bw, bh, gap = 380, 72, 16
            cols = 2
            total_w = cols * bw + (cols - 1) * gap
            total_h = 5 * bh + 4 * gap
            bx0 = (C.SW - total_w) // 2
            by0 = (C.SH - total_h) // 2 + 30

            for i in range(10):
                col = i % cols
                row = i // cols
                bx  = bx0 + col * (bw + gap)
                by  = by0 + row * (bh + gap)

                if i == 0:
                    box_col  = (70, 40, 110)
                    bdr_col  = (180, 100, 255)
                    txt_col  = (230, 180, 255)
                    label    = "Uhyun  Questions"
                    sub      = "Factorial Math  (5 Qs)"
                else:
                    box_col  = (30, 30, 50)
                    bdr_col  = (80, 80, 110)
                    txt_col  = (100, 100, 130)
                    label    = "???"
                    sub      = ""

                pygame.draw.rect(scr, box_col, (bx, by, bw, bh), border_radius=10)
                pygame.draw.rect(scr, bdr_col, (bx, by, bw, bh), 2, border_radius=10)

                lbl_surf = display.f_med.render(label, True, txt_col)
                scr.blit(lbl_surf, (bx + 16, by + 10))
                if sub:
                    sub_surf = display.f_xs.render(sub, True, (170, 130, 220))
                    scr.blit(sub_surf, (bx + 16, by + bh - sub_surf.get_height() - 8))

            hint = display.f_xs.render("ESC to return", True, (130, 130, 160))
            scr.blit(hint, (C.SW // 2 - hint.get_width() // 2, C.SH - 28))

        elif cur_state == C.SECRET_QUIZ:
            if q_idx >= len(UHYUN_QS):
                # ── Results screen ─────────────────────────────────────────────
                correct = sum(answers)
                title   = display.f_big.render(
                    f"Results:  {correct} / {len(UHYUN_QS)}", True, (220, 200, 255))
                scr.blit(title, (C.SW // 2 - title.get_width() // 2, 140))

                for i, q in enumerate(UHYUN_QS):
                    col = (100, 255, 140) if answers[i] else (255, 100, 100)
                    mark = "✓" if answers[i] else "✗"
                    line = display.f_sm.render(
                        f"{mark}  {q['q']}  →  {q['opts'][q['ans']]}", True, col)
                    scr.blit(line, (C.SW // 2 - line.get_width() // 2, 220 + i * 52))

                prompt = display.f_xs.render(
                    "Click or press ENTER / SPACE to continue", True, (160, 160, 200))
                scr.blit(prompt, (C.SW // 2 - prompt.get_width() // 2, C.SH - 50))
            else:
                # ── Question screen ────────────────────────────────────────────
                q = UHYUN_QS[q_idx]
                prog = display.f_xs.render(
                    f"Uhyun Questions   {q_idx + 1} / {len(UHYUN_QS)}", True, (180, 140, 255))
                scr.blit(prog, (C.SW // 2 - prog.get_width() // 2, 50))

                q_surf = display.f_big.render(q["q"], True, (230, 210, 255))
                scr.blit(q_surf, (C.SW // 2 - q_surf.get_width() // 2, 140))

                bw, bh = 260, 60
                gap    = 14
                grid_w = bw * 2 + gap
                gx     = (C.SW - grid_w) // 2
                gy     = C.SH // 2 + 20
                labels = ["A", "B", "C", "D"]
                for i, opt in enumerate(q["opts"]):
                    abx = gx + (i % 2) * (bw + gap)
                    aby = gy + (i // 2) * (bh + gap)
                    pygame.draw.rect(scr, (50, 30, 80), (abx, aby, bw, bh), border_radius=8)
                    pygame.draw.rect(scr, (160, 100, 255), (abx, aby, bw, bh), 2, border_radius=8)
                    opt_txt = display.f_sm.render(
                        f"{labels[i]}.  {opt}", True, (220, 200, 255))
                    scr.blit(opt_txt, (abx + 12, aby + bh // 2 - opt_txt.get_height() // 2))

                hint = display.f_xs.render(
                    "Click an answer or press A / B / C / D", True, (130, 130, 160))
                scr.blit(hint, (C.SW // 2 - hint.get_width() // 2, C.SH - 28))

    # ── Main loop ─────────────────────────────────────────────────────────────
    # Start the intro timer here (not during slow init) and flush any stale
    # events that accumulated while assets and music were loading.
    intro_fade.reset()
    pygame.event.clear()

    running = True
    while running:
        display.clock.tick(C.FPS)
        _prev_state = state

        # ── Events ───────────────────────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:

                # Always feed the sequence checker (works in any state)
                debug_menu.check_seq(ev.key)

                # When the debug input field is open it captures all keys
                if debug_menu.is_capturing():
                    debug_menu.handle_keydown(ev)
                    continue

                # ── Quit / back from secret stage ────────────────────────────
                if ev.key == pygame.K_ESCAPE:
                    if state in (C.SECRET_SELECT, C.SECRET_QUIZ):
                        # Back to the secret area (not the main game)
                        secret_q_idx   = 0
                        secret_answers = []
                        secret_q_sel   = -1
                        state = C.SECRET
                    elif state == C.SECRET:
                        # Exit secret area back to main game
                        player.x  = float(secret_return_pos[0])
                        player.y  = float(secret_return_pos[1])
                        player.vx = player.vy = 0
                        _fade_target = None
                        state = C.PLAY
                    else:
                        pygame.quit(); sys.exit()

                # ── Debug: 0 → main menu ─────────────────────────────────────
                elif ev.key == pygame.K_0:
                    full_reset(1, 0, player.lives, keep_grade=False)
                    music.play_main_menu_track()

                # ── Music controls (global) ───────────────────────────────────
                elif ev.key == pygame.K_m:
                    music.toggle_mute()
                elif ev.key == pygame.K_n:
                    music.next_track()
                elif ev.key == pygame.K_b:
                    music.prev_track()
                elif ev.key == pygame.K_RIGHTBRACKET:
                    music.volume_up()
                elif ev.key == pygame.K_LEFTBRACKET:
                    music.volume_down()

                # ── State-specific keys ───────────────────────────────────────
                elif state == C.INTRO_FADE:
                    intro_fade.advance()
                    if intro_fade.done:
                        music.play_cutscene_track()
                        cutscene.reset()
                        state = C.CUTSCENE

                elif state == C.CUTSCENE:
                    cutscene.advance()
                    if cutscene.done:
                        music.play_main_menu_track()
                        state = C.TITLE

                elif state == C.CHAR_CUTSCENE:
                    char_cutscene.advance()
                    if char_cutscene.done:
                        music.play(stage_track_idx)
                        state = C.TUTORIAL_PROMPT

                elif state == C.BOSS_CUTSCENE:
                    boss_cutscene.advance()
                    if boss_cutscene.done:
                        boss_fight.reset(selected_char, lvl, boss_cutscene.get_boss_img())
                        state = C.BOSS_FIGHT

                elif state == C.BOSS_FIGHT:
                    if boss_fight._phase in ("win", "lose") and boss_fight._result_timer > 90:
                        if boss_fight.result == "win":
                            state = C.LVLDONE
                        else:
                            savegame.delete()
                            full_reset(1, 0, 3, keep_grade=False)
                            music.play_main_menu_track()
                    else:
                        boss_fight.handle_key(ev.key)

                elif state == C.SPLASH:
                    # Any key (except the global ones already handled) advances
                    if pygame.time.get_ticks() >= 1500:
                        sfx.play_select()
                        music.play_main_menu_track()
                        state = C.TITLE

                elif state == C.TITLE:
                    if ev.key in (pygame.K_UP, pygame.K_w):
                        title_sel = (title_sel - 1) % 4
                        sfx.play_nav()
                    elif ev.key in (pygame.K_DOWN, pygame.K_s):
                        title_sel = (title_sel + 1) % 4
                        sfx.play_nav()
                    elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        sfx.play_select()
                        if title_sel == 0:          # New Game
                            selected_grade = 0
                            char_sel = 0
                            state = C.CHAR_SELECT
                        elif title_sel == 1:        # Load Game
                            data = savegame.load()
                            if data:
                                selected_grade = data["grade"]
                                full_reset(data["lvl"], data["score"],
                                           data["lives"], keep_grade=True)
                            else:
                                flash("No save data found!", C.RED)
                        elif title_sel == 2:        # Options
                            opts_sel = 0
                            state = C.TITLE_OPTIONS
                        elif title_sel == 3:        # Credits
                            state = C.TITLE_CREDITS

                elif state == C.CHAR_SELECT:
                    if secret_char_popup:
                        # Navigate the 6-slot secret popup (3 cols × 2 rows)
                        if ev.key == pygame.K_ESCAPE:
                            secret_char_popup = False
                            sfx.play_nav()
                        elif ev.key in (pygame.K_LEFT, pygame.K_a):
                            secret_char_sel = (secret_char_sel - 1) % 6
                            sfx.play_nav()
                        elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                            secret_char_sel = (secret_char_sel + 1) % 6
                            sfx.play_nav()
                        elif ev.key in (pygame.K_UP, pygame.K_w):
                            secret_char_sel = (secret_char_sel - 3) % 6
                            sfx.play_nav()
                        elif ev.key in (pygame.K_DOWN, pygame.K_s):
                            secret_char_sel = (secret_char_sel + 3) % 6
                            sfx.play_nav()
                        elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                            if secret_char_sel < 2:
                                sfx.play_select()
                                selected_char = f"secret{secret_char_sel + 1}"
                                secret_char_popup = False
                                player, doors, key_items = _build_level(lvl, selected_char)
                                state = C.GRADE_SELECT
                    else:
                        if ev.key in (pygame.K_LEFT, pygame.K_a):
                            char_sel = (char_sel - 1) % 3
                            sfx.play_nav()
                        elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                            char_sel = (char_sel + 1) % 3
                            sfx.play_nav()
                        elif ev.key == pygame.K_1:
                            char_sel = 0
                            sfx.play_nav()
                        elif ev.key == pygame.K_2:
                            char_sel = 1
                            sfx.play_nav()
                        elif ev.key == pygame.K_3:
                            char_sel = 2
                            sfx.play_nav()
                        elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                            sfx.play_select()
                            if char_sel == 0:
                                selected_char = "kirby"
                                player, doors, key_items = _build_level(lvl, selected_char)
                                state = C.GRADE_SELECT
                            elif char_sel == 1:
                                selected_char = "miles"
                                player, doors, key_items = _build_level(lvl, selected_char)
                                state = C.GRADE_SELECT
                            else:
                                secret_char_popup = True
                                secret_char_sel   = 0

                elif state == C.TITLE_OPTIONS:
                    if ev.key in (pygame.K_UP, pygame.K_w):
                        opts_sel = (opts_sel - 1) % 5
                        sfx.play_nav()
                    elif ev.key in (pygame.K_DOWN, pygame.K_s):
                        opts_sel = (opts_sel + 1) % 5
                        sfx.play_nav()
                    elif ev.key in (pygame.K_LEFT, pygame.K_a):
                        if opts_sel == 0:
                            music.volume_down();  sfx.play_nav()
                        elif opts_sel == 1:
                            sfx.volume_down();  sfx.play_nav()
                        elif opts_sel == 2:
                            music.prev_track();  sfx.play_nav()
                        elif opts_sel == 3:
                            display.set_mode_idx(display.current_mode_idx() - 1)
                            sfx.play_nav()
                    elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                        if opts_sel == 0:
                            music.volume_up();  sfx.play_nav()
                        elif opts_sel == 1:
                            sfx.volume_up();  sfx.play_nav()
                        elif opts_sel == 2:
                            music.next_track();  sfx.play_nav()
                        elif opts_sel == 3:
                            display.set_mode_idx(display.current_mode_idx() + 1)
                            sfx.play_nav()
                    elif ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        if opts_sel == 4 or ev.key == pygame.K_ESCAPE:
                            sfx.play_select()
                            state = C.TITLE

                elif state == C.TITLE_CREDITS:
                    sfx.play_select()
                    state = C.TITLE

                elif state == C.GRADE_SELECT:
                    grade_keys = {
                        pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
                        pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
                    }
                    chosen = grade_keys.get(ev.key)
                    if chosen:
                        sfx.play_grade_select()
                        selected_grade = chosen
                        stage_track_idx = 0
                        tutorial_sel = 0
                        char_cutscene.reset(selected_char)
                        music.play_char_cutscene_track(selected_char)
                        state = C.CHAR_CUTSCENE

                elif state == C.TUTORIAL_PROMPT:
                    if ev.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                        tutorial_sel = 1 - tutorial_sel
                        sfx.play_nav()
                    elif ev.key == pygame.K_y:
                        tutorial_page = 0
                        state = C.TUTORIAL
                        sfx.play_select()
                    elif ev.key in (pygame.K_n, pygame.K_ESCAPE):
                        state = C.INTRO
                        sfx.play_select()
                    elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        sfx.play_select()
                        if tutorial_sel == 0:
                            tutorial_page = 0
                            state = C.TUTORIAL
                        else:
                            state = C.INTRO

                elif state == C.TUTORIAL:
                    if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        sfx.play_select()
                        if tutorial_page < 3:
                            tutorial_page += 1
                        else:
                            state = C.PLAY
                    elif ev.key == pygame.K_ESCAPE:
                        sfx.play_select()
                        state = C.PLAY

                elif state == C.INTRO:
                    if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        state = C.PLAY

                elif state == C.SECRET:
                    pass  # movement via get_pressed(); ESC handled above

                elif state == C.SECRET_SELECT:
                    # Any key returns to the secret room
                    secret_q_idx   = 0
                    secret_answers = []
                    secret_q_sel   = -1
                    state = C.SECRET

                elif state == C.SECRET_QUIZ:
                    if secret_q_idx >= len(UHYUN_QS):
                        # Results screen — any key dismisses
                        secret_q_idx   = 0
                        secret_answers = []
                        secret_q_sel   = -1
                        state = C.SECRET
                    else:
                        # A/B/C/D answer shortcuts
                        idx = {pygame.K_a: 0, pygame.K_b: 1,
                               pygame.K_c: 2, pygame.K_d: 3}.get(ev.key)
                        if idx is not None:
                            q = UHYUN_QS[secret_q_idx]
                            secret_answers.append(idx == q["ans"])
                            secret_q_sel = idx
                            secret_q_idx += 1
                        elif ev.key == pygame.K_ESCAPE:
                            # ESC mid-quiz → back to select screen
                            secret_q_idx   = 0
                            secret_answers = []
                            secret_q_sel   = -1
                            state = C.SECRET_SELECT

                elif state == C.PLAY:
                    pass  # movement via get_pressed()

                elif state == C.DOOR_QUESTION:
                    idx = {pygame.K_a: 0, pygame.K_b: 1,
                           pygame.K_c: 2, pygame.K_d: 3}.get(ev.key)
                    if idx is not None and active_q is not None:
                        if idx == active_q["ans"]:
                            # ── Correct ───────────────────────────────────────
                            earned = _calc_stars(pygame.time.get_ticks() - q_start_time)
                            level_stars        += earned
                            total_stars        += earned
                            last_earned_stars   = earned
                            active_door.completed = True
                            doors_completed.add(active_door.num)
                            score               += 100
                            flash_msg            = ""
                            flash_timer          = 0
                            correct_anim_start   = pygame.time.get_ticks()
                            sfx.play_star_reveal()
                            state                = C.DOOR_CORRECT
                        else:
                            # ── Wrong ─────────────────────────────────────────
                            player.lives -= 1
                            flash("Wrong!  Try again!", C.RED, 120)
                            if player.lives <= 0:
                                state = C.GAMEOVER

                elif state == C.DOOR_CORRECT:
                    # Any key after 400 ms skips to FADE_IN
                    if pygame.time.get_ticks() - correct_anim_start >= 400:
                        state = C.FADE_IN

                elif state == C.BONUS_Q:
                    idx = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}.get(ev.key)
                    if idx is not None:
                        bonus_won = (idx == bonus_q["ans"])
                        if bonus_won:
                            score += 300
                        state   = C.BONUS_R
                        b_timer = 200

                elif state == C.LVLDONE:
                    if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if lvl >= C.TOTAL:
                            state = C.GAMEWIN
                        else:
                            cutscene2.reset(lvl + 1)
                            music.play_transition_track(lvl + 1)
                            state = C.TRANSIT

                elif state == C.TRANSIT:
                    cutscene2.advance()
                    if cutscene2.done:
                        full_reset(lvl + 1, score, player.lives)

                elif state in (C.GAMEOVER, C.GAMEWIN):
                    if ev.key in (pygame.K_RETURN, pygame.K_r):
                        savegame.delete()
                        full_reset(1, 0, 3, keep_grade=False)
                        music.play_main_menu_track()

            # ── Mouse click ──────────────────────────────────────────────────
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = display.to_canvas(ev.pos)

                if debug_menu.handle_click(mx, my):
                    continue   # consumed by debug panel

                if state == C.SPLASH:
                    if pygame.time.get_ticks() >= 1500:
                        sfx.play_select()
                        music.play_main_menu_track()
                        state = C.TITLE

                elif state == C.TITLE:
                    for i in range(4):
                        cy = 230 + i * 60   # centre y of each menu item (matches draw_title)
                        if abs(my - cy) <= 24 and abs(mx - C.SW // 2) <= 220:
                            title_sel = i
                            sfx.play_select()
                            if i == 0:
                                selected_grade = 0; char_sel = 0
                                state = C.CHAR_SELECT
                            elif i == 1:
                                data = savegame.load()
                                if data:
                                    selected_grade = data["grade"]
                                    full_reset(data["lvl"], data["score"],
                                               data["lives"], keep_grade=True)
                                else:
                                    flash("No save data found!", C.RED)
                            elif i == 2:
                                opts_sel = 0; state = C.TITLE_OPTIONS
                            elif i == 3:
                                state = C.TITLE_CREDITS
                            break

                elif state == C.TITLE_OPTIONS:
                    _pw, _px0, _py0, _rh = 700, (C.SW - 700) // 2, 108, 72
                    _mid = _px0 + _pw // 2
                    for i in range(5):
                        ry = _py0 + 16 + i * _rh
                        if _px0 + 16 <= mx <= _px0 + _pw - 16 and ry <= my <= ry + 58:
                            opts_sel = i
                            if i == 0:
                                if mx < _mid: music.volume_down()
                                else:         music.volume_up()
                                sfx.play_nav()
                            elif i == 1:
                                if mx < _mid: sfx.volume_down()
                                else:         sfx.volume_up()
                                sfx.play_nav()
                            elif i == 2:
                                if mx < _mid: music.prev_track()
                                else:         music.next_track()
                                sfx.play_nav()
                            elif i == 3:
                                if mx < _mid:
                                    display.set_mode_idx(display.current_mode_idx() - 1)
                                else:
                                    display.set_mode_idx(display.current_mode_idx() + 1)
                                sfx.play_nav()
                            elif i == 4:
                                sfx.play_select(); state = C.TITLE
                            break

                elif state == C.TITLE_CREDITS:
                    sfx.play_select(); state = C.TITLE

                elif state == C.CHAR_SELECT:
                    _cw, _ch, _gap = 310, 430, 30
                    _lx = (C.SW - (_cw * 3 + _gap * 2)) // 2
                    if secret_char_popup:
                        # Check popup slot clicks
                        _pw, _ph = 720, 420
                        _px = (C.SW - _pw) // 2
                        _py = (C.SH - _ph) // 2
                        _sw2, _sh2 = 190, 120
                        _cols2 = 3
                        _gx2 = (_pw - _sw2 * _cols2) // (_cols2 + 1)
                        _gy2 = 18
                        _gt  = _py + 72
                        for idx in range(6):
                            _ci = idx % _cols2
                            _ri = idx // _cols2
                            _sx2 = _px + _gx2 + _ci * (_sw2 + _gx2)
                            _sy2 = _gt + _ri * (_sh2 + _gy2)
                            if _sx2 <= mx <= _sx2 + _sw2 and _sy2 <= my <= _sy2 + _sh2:
                                if idx < 2:
                                    sfx.play_select()
                                    secret_char_sel   = idx
                                    selected_char     = f"secret{idx + 1}"
                                    secret_char_popup = False
                                    player, doors, key_items = _build_level(lvl, selected_char)
                                    state = C.GRADE_SELECT
                                break
                        # Click outside popup closes it
                        if not (_px <= mx <= _px + _pw and _py <= my <= _py + _ph):
                            secret_char_popup = False
                    else:
                        for i in range(3):
                            cx2 = _lx + i * (_cw + _gap)
                            if cx2 <= mx <= cx2 + _cw and 108 <= my <= 108 + _ch:
                                char_sel = i
                                sfx.play_select()
                                if i == 0:
                                    selected_char = "kirby"
                                    player, doors, key_items = _build_level(lvl, selected_char)
                                    state = C.GRADE_SELECT
                                elif i == 1:
                                    selected_char = "miles"
                                    player, doors, key_items = _build_level(lvl, selected_char)
                                    state = C.GRADE_SELECT
                                else:
                                    secret_char_popup = True
                                    secret_char_sel   = 0
                                break

                elif state == C.GRADE_SELECT:
                    _cw, _ch, _gap = 318, 118, 16
                    _sx = (C.SW - (3 * _cw + 2 * _gap)) // 2
                    _rows = [130, 130 + _ch + _gap]
                    for i in range(6):
                        gx = _sx + (i % 3) * (_cw + _gap)
                        gy = _rows[i // 3]
                        if gx <= mx <= gx + _cw and gy <= my <= gy + _ch:
                            sfx.play_grade_select()
                            selected_grade = i + 1
                            stage_track_idx = 0
                            tutorial_sel = 0
                            char_cutscene.reset(selected_char)
                            music.play_char_cutscene_track(selected_char)
                            state = C.CHAR_CUTSCENE
                            break

                elif state == C.TUTORIAL_PROMPT:
                    # Button layout mirrors draw_tutorial_prompt:
                    # dx=200, dy=135, bw=190, bh=52, by=dy+248=383
                    # YES bx=480, NO bx=688
                    _dw, _dh = 700, 340
                    _dx = (C.SW - _dw) // 2
                    _dy = (C.SH - _dh) // 2 - 20
                    _bw, _bh = 190, 52
                    _by = _dy + 248
                    for i in range(2):
                        _bx = _dx + 280 + i * (_bw + 18)
                        if _bx <= mx <= _bx + _bw and _by <= my <= _by + _bh:
                            tutorial_sel = i
                            sfx.play_select()
                            if i == 0:
                                tutorial_page = 0
                                state = C.TUTORIAL
                            else:
                                state = C.INTRO
                            break

                elif state == C.INTRO:
                    stage_track_idx = music.track_index()
                    state = C.PLAY

                elif state == C.DOOR_QUESTION:
                    # Left-half layout: half_w=548, btn_w=250, gap_x=12
                    _half = 548
                    _bw, _bh = 250, 60
                    _gx = (_half - (_bw * 2 + 12)) // 2
                    _gy = 130 + 90 + 18
                    for i in range(4):
                        bx2 = _gx + (i % 2) * (_bw + 12)
                        by2 = _gy + (i // 2) * (_bh + 10)
                        if bx2 <= mx <= bx2 + _bw and by2 <= my <= by2 + _bh:
                            if active_q is not None:
                                if i == active_q["ans"]:
                                    earned = _calc_stars(pygame.time.get_ticks() - q_start_time)
                                    level_stars        += earned
                                    total_stars        += earned
                                    last_earned_stars   = earned
                                    active_door.completed = True
                                    doors_completed.add(active_door.num)
                                    score              += 100
                                    flash_msg           = ""; flash_timer = 0
                                    correct_anim_start  = pygame.time.get_ticks()
                                    sfx.play_star_reveal()
                                    state               = C.DOOR_CORRECT
                                else:
                                    player.lives -= 1
                                    flash("Wrong!  Try again!", C.RED, 120)
                                    if player.lives <= 0:
                                        state = C.GAMEOVER
                            break

                elif state == C.DOOR_CORRECT:
                    if pygame.time.get_ticks() - correct_anim_start >= 400:
                        state = C.FADE_IN

                elif state == C.SECRET_SELECT:
                    # 10 boxes: 2 columns × 5 rows; only box 0 is selectable
                    _bw, _bh, _gap = 380, 72, 16
                    _cols = 2
                    _total_w = _cols * _bw + (_cols - 1) * _gap
                    _total_h = 5 * _bh + 4 * _gap
                    _bx0 = (C.SW - _total_w) // 2
                    _by0 = (C.SH - _total_h) // 2 + 30
                    for i in range(10):
                        col = i % _cols
                        row = i // _cols
                        bx  = _bx0 + col * (_bw + _gap)
                        by  = _by0 + row * (_bh + _gap)
                        if bx <= mx <= bx + _bw and by <= my <= by + _bh:
                            if i == 0:   # only Uhyun box is active
                                secret_q_idx   = 0
                                secret_answers = []
                                secret_q_sel   = -1
                                state = C.SECRET_QUIZ
                            break

                elif state == C.SECRET_QUIZ:
                    if secret_q_idx >= len(UHYUN_QS):
                        # Results screen — click anywhere to dismiss
                        secret_q_idx   = 0
                        secret_answers = []
                        secret_q_sel   = -1
                        state = C.SECRET
                    else:
                        # Answer buttons: 2 × 2 grid centred on screen
                        _bw, _bh = 260, 60
                        _gap = 14
                        _grid_w = _bw * 2 + _gap
                        _gx = (C.SW - _grid_w) // 2
                        _gy = C.SH // 2 + 20
                        for i in range(4):
                            abx = _gx + (i % 2) * (_bw + _gap)
                            aby = _gy + (i // 2) * (_bh + _gap)
                            if abx <= mx <= abx + _bw and aby <= my <= aby + _bh:
                                q = UHYUN_QS[secret_q_idx]
                                secret_answers.append(i == q["ans"])
                                secret_q_sel = i
                                secret_q_idx += 1
                                break

                elif state == C.PLAY:
                    for d in doors:
                        if d.r.collidepoint(mx, my):
                            if d.locked:
                                flash(f"Door {d.num} is locked!  Find the key!", C.RED)
                            elif not d.completed:
                                # Teleport player to the door entrance
                                if d.side == "top":
                                    player.x = float(d.r.centerx)
                                    player.y = float(d.r.bottom + C.PR + 4)
                                elif d.side == "bottom":
                                    player.x = float(d.r.centerx)
                                    player.y = float(d.r.top - C.PR - 4)
                                else:  # right
                                    player.x = float(d.r.left - C.PR - 4)
                                    player.y = float(d.r.centery)
                                player.vx = player.vy = 0
                                if d.num not in door_questions:
                                    door_questions[d.num] = get_door_question(
                                        d.num, selected_grade, stage, used_ids)
                                active_door = d
                                active_q    = door_questions[d.num]
                                flash_msg   = ""
                                flash_timer = 0
                                fade_alpha  = 0
                                state       = C.FADE_OUT
                            break

                elif state == C.LVLDONE:
                    if lvl >= C.TOTAL:
                        state = C.GAMEWIN
                    else:
                        cutscene2.reset(lvl + 1)
                        music.play_transition_track(lvl + 1)
                        state = C.TRANSIT

                elif state in (C.GAMEOVER, C.GAMEWIN):
                    savegame.delete()
                    full_reset(1, 0, 3, keep_grade=False)
                    music.play_main_menu_track()

        # ── Update ───────────────────────────────────────────────────────────
        if state in (C.TITLE, C.TITLE_OPTIONS, C.TITLE_CREDITS, C.CHAR_SELECT, C.GRADE_SELECT):
            music.update_main_menu()

        if state == C.INTRO_FADE:
            if intro_fade.update():
                music.play_cutscene_track()
                cutscene.reset()
                state = C.CUTSCENE

        elif state == C.CUTSCENE:
            if cutscene.update():
                music.play_main_menu_track()
                state = C.TITLE

        elif state == C.TRANSIT:
            if cutscene2.update():
                full_reset(lvl + 1, score, player.lives)

        elif state == C.STAGE_TRANSIT:
            if stage_transition.update():
                state = C.PLAY

        elif state == C.CHAR_CUTSCENE:
            if char_cutscene.update():
                music.play(stage_track_idx)
                state = C.TUTORIAL_PROMPT

        elif state == C.BOSS_CUTSCENE:
            if boss_cutscene.update():
                boss_fight.reset(selected_char, lvl, boss_cutscene.get_boss_img())
                state = C.BOSS_FIGHT

        elif state == C.BOSS_FIGHT:
            boss_fight.update()

        elif state == C.SECRET:
            # Player moves freely inside the secret room
            if player.push_cd == 0:
                kp = pygame.key.get_pressed()
                dx, dy = 0, 0
                if kp[pygame.K_LEFT]  or kp[pygame.K_a]: dx -= 1
                if kp[pygame.K_RIGHT] or kp[pygame.K_d]: dx += 1
                if kp[pygame.K_UP]    or kp[pygame.K_w]: dy -= 1
                if kp[pygame.K_DOWN]  or kp[pygame.K_s]: dy += 1
                if dx and dy:
                    f = C.SPEED / math.sqrt(2)
                    player.vx, player.vy = dx * f, dy * f
                elif dx or dy:
                    player.vx, player.vy = dx * C.SPEED, dy * C.SPEED
                else:
                    player.vx = player.vy = 0
            player.update()
            secret_stage.update()
            # Portal collision → fade out then show select screen
            if player.r.colliderect(secret_stage.portal_rect):
                _fade_target = "portal_enter"
                fade_alpha   = 0
                state        = C.FADE_OUT
            # Right edge → return to main stage
            elif player.x >= C.SW - C.PR:
                player.x  = float(secret_return_pos[0])
                player.y  = float(secret_return_pos[1])
                player.vx = player.vy = 0
                _fade_target = None
                state        = C.PLAY

        elif state == C.PLAY:
            # Player movement (suppressed during push-back)
            if player.push_cd == 0:
                kp = pygame.key.get_pressed()
                dx, dy = 0, 0
                if kp[pygame.K_LEFT]  or kp[pygame.K_a]: dx -= 1
                if kp[pygame.K_RIGHT] or kp[pygame.K_d]: dx += 1
                if kp[pygame.K_UP]    or kp[pygame.K_w]: dy -= 1
                if kp[pygame.K_DOWN]  or kp[pygame.K_s]: dy += 1
                if dx and dy:
                    f = C.SPEED / math.sqrt(2)
                    player.vx, player.vy = dx * f, dy * f
                elif dx or dy:
                    player.vx, player.vy = dx * C.SPEED, dy * C.SPEED
                else:
                    player.vx = player.vy = 0

                # Left edge → fade out then enter secret stage
                if player.x <= C.PR and dx < 0:
                    secret_return_pos = (player.x, player.y)
                    _fade_target = "secret_enter"
                    fade_alpha   = 0
                    state        = C.FADE_OUT

            player.update()

            # Key collection
            for k in key_items:
                if not k.collected:
                    k.update()
                    if player.r.colliderect(k.r):
                        k.collected = True
                        player.keys.append(k.door_num)
                        for d in doors:
                            if d.num == k.door_num:
                                d.locked = False
                        flash(f"Got key for Door {k.door_num}!", C.GOLD)

            # Door collisions
            for d in doors:
                if player.r.colliderect(d.r):
                    if d.locked:
                        flash(f"Door {d.num} is locked!  Find the key!", C.RED)
                        player.push(d)
                    elif d.completed:
                        # Completed doors act as walls – push back silently
                        player.push(d)
                    else:
                        # Enter question flow for this door
                        if d.num not in door_questions:
                            door_questions[d.num] = get_door_question(d.num, selected_grade, stage, used_ids)
                        active_door = d
                        active_q    = door_questions[d.num]
                        flash_msg   = ""
                        flash_timer = 0
                        fade_alpha  = 0
                        state       = C.FADE_OUT
                    break  # handle one door collision per frame

            for d in doors:
                d.update()

            if flash_timer > 0:
                flash_timer -= 1

        elif state == C.FADE_OUT:
            fade_alpha = min(255, fade_alpha + C.FADE_SPEED)
            if fade_alpha >= 255:
                if _fade_target == "secret_enter":
                    # Black screen reached — place player in secret area, fade back in
                    player.x  = float(C.SW - C.PR - 60)
                    player.y  = float(C.SH // 2)
                    player.vx = player.vy = 0
                    secret_stage.reset()
                    _fade_target = "secret_fadein"
                    state        = C.FADE_IN
                elif _fade_target == "portal_enter":
                    _fade_target = None
                    state        = C.SECRET_SELECT
                else:
                    q_start_time = pygame.time.get_ticks()
                    state        = C.DOOR_QUESTION

        elif state == C.DOOR_CORRECT:
            # Auto-advance to FADE_IN after 3 seconds
            if pygame.time.get_ticks() - correct_anim_start >= 3000:
                state = C.FADE_IN

        elif state == C.FADE_IN:
            fade_alpha = max(0, fade_alpha - C.FADE_SPEED)
            if fade_alpha <= 0:
                if _fade_target == "secret_fadein":
                    _fade_target = None
                    state        = C.SECRET
                elif all(d.completed for d in doors):
                    savegame.save(selected_grade, lvl, score, player.lives)
                    save_timer = 120
                    if stage < 5:
                        _advance_stage()
                        stage_transition.reset(stage)
                        state = C.STAGE_TRANSIT
                    else:
                        boss_cutscene.reset(lvl)
                        state = C.BOSS_CUTSCENE
                else:
                    state = C.PLAY

        elif state == C.BONUS_R:
            b_timer -= 1
            if b_timer <= 0:
                if bonus_won:
                    skip = lvl + 2
                    if skip > C.TOTAL:
                        state = C.GAMEWIN
                    else:
                        full_reset(skip, score, player.lives)
                else:
                    state = C.PLAY

        # Detect entry into TITLE state this frame and record timestamp for flash-in
        if state == C.TITLE and _prev_state != C.TITLE:
            title_enter_ms = pygame.time.get_ticks()

        # Tick save indicator countdown every frame regardless of state
        if save_timer > 0:
            save_timer -= 1

        # ── Debug command processor ───────────────────────────────────────────
        cmd = debug_menu.get_command()
        if cmd:
            if cmd.startswith("b") and cmd[1:].isdigit():
                target_lvl = int(cmd[1:])
                if 1 <= target_lvl <= C.TOTAL:
                    boss_cutscene.reset(target_lvl)
                    state = C.BOSS_CUTSCENE
            elif cmd.startswith("w") and cmd[1:].isdigit():
                target_lvl = int(cmd[1:])
                if 1 <= target_lvl <= C.TOTAL:
                    full_reset(target_lvl, score, player.lives)
            elif cmd == "win" and state == C.BOSS_FIGHT:
                boss_fight._boss_hp = 0
                boss_fight._log.append("[DEBUG] Boss HP set to 0.")
                boss_fight._phase  = "win"
                boss_fight.done    = True
                boss_fight.result  = "win"
            elif cmd == "heal" and state == C.BOSS_FIGHT:
                boss_fight._hero_hp = boss_fight._HERO_MAX_HP
                boss_fight._log.append("[DEBUG] HP restored.")

        # ── Draw ─────────────────────────────────────────────────────────────

        # Decide whether the secret area or the normal stage is the backdrop
        _secret_backdrop = (
            state in (C.SECRET, C.SECRET_SELECT, C.SECRET_QUIZ) or
            (state == C.FADE_IN  and _fade_target == "secret_fadein") or
            (state == C.FADE_OUT and _fade_target == "portal_enter")
        )

        if _secret_backdrop:
            secret_stage.draw_background()
            secret_stage.draw_portal()
            player.draw()
            if state == C.SECRET:
                hint = display.f_xs.render(
                    "Touch the portal   |   ESC to return", True, (180, 170, 220))
                display.screen.blit(
                    hint, (C.SW // 2 - hint.get_width() // 2, C.SH - 34))
        else:
            # Normal game world
            draw_bg(lvl)
            for k in key_items:
                k.draw()
            for d in doors:
                d.draw()
            player.draw()
            if state in (C.PLAY, C.FADE_OUT, C.FADE_IN, C.DOOR_QUESTION, C.STAGE_TRANSIT):
                draw_hud(lvl, player.lives, score, player.keys, doors_completed, total_stars, stage, save_timer)
            if flash_timer > 0 and state == C.PLAY:
                fs = display.f_big.render(flash_msg, True, flash_col)
                display.screen.blit(
                    fs, (C.SW // 2 - fs.get_width() // 2, C.SH // 2 - 20))

        # ── Overlay states ────────────────────────────────────────────────────
        if state == C.FADE_OUT or state == C.FADE_IN:
            fade_surf = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
            fade_surf.fill((0, 0, 0, fade_alpha))
            display.screen.blit(fade_surf, (0, 0))

        elif state in (C.SECRET_SELECT, C.SECRET_QUIZ):
            _draw_secret_overlay(state, secret_q_idx, secret_answers)

        elif state == C.DOOR_QUESTION and active_q is not None:
            draw_door_question(
                active_q,
                active_door.subject["name"],
                active_door.subject["color"],
                player.lives,
                flash_msg  if flash_timer > 0 else "",
                flash_col,
                assets.question_panel_img,
                elapsed_secs=(pygame.time.get_ticks() - q_start_time) / 1000.0,
            )
            if flash_timer > 0:
                flash_timer -= 1

        elif state == C.DOOR_CORRECT:
            draw_star_reveal(last_earned_stars,
                             pygame.time.get_ticks() - correct_anim_start)

        elif state == C.INTRO_FADE:
            intro_fade.draw()

        elif state == C.CUTSCENE:
            cutscene.draw()

        elif state == C.TRANSIT:
            cutscene2.draw()

        elif state == C.CHAR_CUTSCENE:
            char_cutscene.draw()

        elif state == C.BOSS_CUTSCENE:
            boss_cutscene.draw()

        elif state == C.BOSS_FIGHT:
            boss_fight.draw()

        elif state == C.STAGE_TRANSIT:
            stage_transition.draw()

        elif state == C.SPLASH:
            draw_splash()
        elif state == C.TITLE:
            draw_title(title_sel, savegame.exists(), title_enter_ms)
        elif state == C.TITLE_OPTIONS:
            draw_title_options(opts_sel, music.volume(), sfx.volume(),
                               music.track_name(), display.current_mode_name())
        elif state == C.TITLE_CREDITS:
            draw_title_credits()
        elif state == C.CHAR_SELECT:
            draw_char_select(char_sel, secret_char_popup, secret_char_sel)
        elif state == C.GRADE_SELECT:
            draw_grade_select()
        elif state == C.TUTORIAL_PROMPT:
            draw_tutorial_prompt(tutorial_sel)
        elif state == C.TUTORIAL:
            draw_tutorial(tutorial_page)
        elif state == C.INTRO:
            draw_intro(selected_grade)
        elif state == C.BONUS_Q:
            draw_bonus_q(bonus_q)
        elif state == C.BONUS_R:
            draw_bonus_res(bonus_won)
        elif state == C.LVLDONE:
            draw_lvl_done(lvl, score, level_stars, total_stars)
        elif state == C.GAMEOVER:
            draw_gameover(score)
        elif state == C.GAMEWIN:
            draw_gamewin(score)

        debug_menu.draw(display.screen)
        display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
