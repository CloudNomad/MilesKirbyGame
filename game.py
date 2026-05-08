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
                        draw_gameover, draw_gamewin)
import save     as savegame
import sounds   as sfx
import cutscene
import cutscene2
import intro_fade
from player     import Player
from level      import new_level_data, random_bonus_question
from questions  import get_door_question


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
    score          = 0
    selected_grade = 0        # set on grade-select screen; 0 = not yet chosen
    selected_char  = "kirby"  # set on char-select screen: "kirby" or "miles"
    char_sel       = 0        # 0 = Kirby, 1 = Miles (cursor on char-select screen)
    state          = C.INTRO_FADE
    intro_fade.reset()

    # ── Title / options menu state ─────────────────────────────────────────────
    title_sel      = 0   # 0=New Game  1=Load Game  2=Options  3=Credits
    opts_sel       = 0   # 0=Music Vol  1=Sound Vol  2=Music Track  3=Display Mode  4=Back
    title_enter_ms = 0   # ticks when TITLE state was last entered (for flash-in)
    _prev_state    = None

    player, doors, key_items = _build_level(lvl, selected_char)

    # ── Per-level question + completion tracking ───────────────────────────────
    door_questions  = {}   # door_num → question dict (drawn on first touch)
    doors_completed = set()  # door nums answered correctly this level

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
        nonlocal lvl, score, state, player, doors, key_items
        nonlocal door_questions, doors_completed, selected_grade
        nonlocal flash_msg, flash_timer, fade_alpha
        nonlocal active_door, active_q, stage_track_idx
        nonlocal bonus_q, bonus_won, title_sel
        nonlocal level_stars, total_stars
        lvl   = new_lvl
        score = new_score
        player, doors, key_items = _build_level(lvl, selected_char)
        player.lives     = new_lives
        door_questions   = {}
        doors_completed  = set()
        flash_msg        = ""
        flash_timer      = 0
        fade_alpha       = 0
        active_door      = None
        active_q         = None
        music.play(new_lvl - 1)          # level 1 = index 0, level 2 = index 1, …
        stage_track_idx  = new_lvl - 1
        bonus_q          = None
        bonus_won        = None
        title_sel        = 0
        level_stars      = 0             # fresh star count for each level
        if not keep_grade:
            total_stars  = 0            # full game restart — wipe total
        if keep_grade and selected_grade:
            state = C.PLAY
        else:
            selected_grade = 0
            state = C.TITLE

    # ── Main loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        display.clock.tick(C.FPS)
        _prev_state = state

        # ── Events ───────────────────────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:

                # ── Quit ──────────────────────────────────────────────────────
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

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
                    if ev.key in (pygame.K_LEFT, pygame.K_a):
                        char_sel = (char_sel - 1) % 2
                        sfx.play_nav()
                    elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                        char_sel = (char_sel + 1) % 2
                        sfx.play_nav()
                    elif ev.key == pygame.K_1:
                        char_sel = 0
                        sfx.play_nav()
                    elif ev.key == pygame.K_2:
                        char_sel = 1
                        sfx.play_nav()
                    elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        sfx.play_select()
                        selected_char = "kirby" if char_sel == 0 else "miles"
                        state = C.GRADE_SELECT

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
                        state = C.INTRO

                elif state == C.INTRO:
                    if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        stage_track_idx = music.track_index()
                        state = C.PLAY

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
                        elif lvl == 1:
                            cutscene2.reset()
                            music.play_cutscene2_track()
                            state = C.TRANSIT_12
                        else:
                            full_reset(lvl + 1, score, player.lives)

                elif state == C.TRANSIT_12:
                    cutscene2.advance()
                    if cutscene2.done:
                        full_reset(2, score, player.lives)

                elif state in (C.GAMEOVER, C.GAMEWIN):
                    if ev.key in (pygame.K_RETURN, pygame.K_r):
                        savegame.delete()
                        full_reset(1, 0, 3, keep_grade=False)
                        music.play_main_menu_track()

            # ── Mouse click ──────────────────────────────────────────────────
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = display.to_canvas(ev.pos)

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
                    _cw, _ch, _gap = 360, 430, 60
                    _lx = (C.SW - (_cw * 2 + _gap)) // 2
                    for i in range(2):
                        cx2 = _lx + i * (_cw + _gap)
                        if cx2 <= mx <= cx2 + _cw and 108 <= my <= 108 + _ch:
                            char_sel = i
                            sfx.play_select()
                            selected_char = "kirby" if i == 0 else "miles"
                            state = C.GRADE_SELECT
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
                                        d.num, selected_grade)
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
                    elif lvl == 1:
                        cutscene2.reset()
                        music.play_cutscene2_track()
                        state = C.TRANSIT_12
                    else:
                        full_reset(lvl + 1, score, player.lives)

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

        elif state == C.TRANSIT_12:
            if cutscene2.update():
                full_reset(2, score, player.lives)

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
                            door_questions[d.num] = get_door_question(d.num, selected_grade)
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
                q_start_time = pygame.time.get_ticks()   # start timing the answer
                state = C.DOOR_QUESTION   # level music keeps playing

        elif state == C.DOOR_CORRECT:
            # Auto-advance to FADE_IN after 3 seconds
            if pygame.time.get_ticks() - correct_anim_start >= 3000:
                state = C.FADE_IN

        elif state == C.FADE_IN:
            fade_alpha = max(0, fade_alpha - C.FADE_SPEED)
            if fade_alpha <= 0:
                # level music was never stopped, nothing to resume
                # Check if all doors are now completed
                eligible = [d for d in doors if not (d.locked and d.num not in doors_completed)]
                if all(d.completed for d in doors):
                    savegame.save(selected_grade, lvl, score, player.lives)
                    state = C.LVLDONE
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

        # ── Draw ─────────────────────────────────────────────────────────────

        # Stage is always drawn (even under fades)
        draw_bg(lvl)

        for k in key_items:
            k.draw()
        for d in doors:
            d.draw()

        player.draw()

        # HUD only shown during active gameplay
        if state in (C.PLAY, C.FADE_OUT, C.FADE_IN, C.DOOR_QUESTION):
            draw_hud(lvl, player.lives, score, player.keys, doors_completed, total_stars)

        # Flash message (centred in play area, only during PLAY)
        if flash_timer > 0 and state == C.PLAY:
            fs = display.f_big.render(flash_msg, True, flash_col)
            display.screen.blit(
                fs, (C.SW // 2 - fs.get_width() // 2, C.SH // 2 - 20))

        # ── Overlay states ────────────────────────────────────────────────────
        if state == C.FADE_OUT or state == C.FADE_IN:
            fade_surf = pygame.Surface((C.SW, C.SH), pygame.SRCALPHA)
            fade_surf.fill((0, 0, 0, fade_alpha))
            display.screen.blit(fade_surf, (0, 0))

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

        elif state == C.TRANSIT_12:
            cutscene2.draw()

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
            draw_char_select(char_sel)
        elif state == C.GRADE_SELECT:
            draw_grade_select()
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

        display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
