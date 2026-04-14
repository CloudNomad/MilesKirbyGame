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
    → DOOR_QUESTION  (full-screen question; music switches to next track)
      • correct  → door marked completed, +100 pts, FADE_IN
      • wrong    → lives -1, flash message, stay on DOOR_QUESTION
    → FADE_IN   (alpha 255 → 0 over ~28 frames; original music resumes)
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
                        draw_intro, draw_door_question, draw_bonus_q,
                        draw_bonus_res, draw_lvl_done, draw_gameover, draw_gamewin)
import save     as savegame
import sounds   as sfx
import cutscene
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
    music.set_volume(0.0)
    music.play_cutscene_track()   # start immediately — fades in during cutscene
    assets.load_all()             # loads while music is already running
    sfx.init()

    lvl            = 1
    score          = 0
    selected_grade = 0        # set on grade-select screen; 0 = not yet chosen
    selected_char  = "kirby"  # set on char-select screen: "kirby" or "miles"
    char_sel       = 0        # 0 = Kirby, 1 = Miles (cursor on char-select screen)
    state          = C.CUTSCENE
    cutscene.reset()

    # ── Title / options menu state ─────────────────────────────────────────────
    title_sel = 0   # 0=New Game  1=Load Game  2=Options  3=Credits
    opts_sel  = 0   # 0=Music Vol  1=Sound Vol  2=Music Track  3=Display Mode  4=Back

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

    # ── Bonus round ────────────────────────────────────────────────────────────
    bonus_q   = None
    bonus_won = None
    b_timer   = 0

    # ── Local helpers ─────────────────────────────────────────────────────────
    def flash(msg, col=C.WHITE, dur=110):
        nonlocal flash_msg, flash_timer, flash_col
        flash_msg = msg; flash_timer = dur; flash_col = col

    def full_reset(new_lvl, new_score, new_lives, keep_grade=True):
        nonlocal lvl, score, state, player, doors, key_items
        nonlocal door_questions, doors_completed, selected_grade
        nonlocal flash_msg, flash_timer, fade_alpha
        nonlocal active_door, active_q, stage_track_idx
        nonlocal bonus_q, bonus_won, title_sel
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
        title_sel = 0
        if keep_grade and selected_grade:
            state = C.PLAY
        else:
            selected_grade = 0
            state = C.TITLE

    # ── Main loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        display.clock.tick(C.FPS)

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
                elif state == C.CUTSCENE:
                    cutscene.advance()
                    if cutscene.done:
                        music.play(0)
                        state = C.TITLE

                elif state == C.SPLASH:
                    # Any key (except the global ones already handled) advances
                    if pygame.time.get_ticks() >= 1500:
                        sfx.play_select()
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
                            active_door.completed = True
                            doors_completed.add(active_door.num)
                            score      += 100
                            flash_msg   = ""
                            flash_timer = 0
                            state       = C.FADE_IN
                        else:
                            # ── Wrong ─────────────────────────────────────────
                            player.lives -= 1
                            flash("Wrong!  Try again!", C.RED, 120)
                            if player.lives <= 0:
                                state = C.GAMEOVER

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
                            full_reset(lvl + 1, score, player.lives)

                elif state in (C.GAMEOVER, C.GAMEWIN):
                    if ev.key in (pygame.K_RETURN, pygame.K_r):
                        savegame.delete()
                        full_reset(1, 0, 3, keep_grade=False)
                        music.play(0)

            # ── Mouse click ──────────────────────────────────────────────────
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = display.to_canvas(ev.pos)

                if state == C.SPLASH:
                    if pygame.time.get_ticks() >= 1500:
                        sfx.play_select()
                        state = C.TITLE

                elif state == C.TITLE:
                    _mw, _my0, _iw, _ih, _ih_step = 380, 202, 344, 42, 52
                    _bx = (C.SW - _mw) // 2 + 18
                    for i in range(4):
                        iy = _my0 + 18 + i * _ih_step
                        if _bx <= mx <= _bx + _iw and iy <= my <= iy + _ih:
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
                    _bw, _bh = 420, 68
                    _gx = (C.SW - (_bw * 2 + 16)) // 2
                    _gy = 118 + 106 + 18
                    for i in range(4):
                        bx2 = _gx + (i % 2) * (_bw + 16)
                        by2 = _gy + (i // 2) * (_bh + 12)
                        if bx2 <= mx <= bx2 + _bw and by2 <= my <= by2 + _bh:
                            if active_q is not None:
                                if i == active_q["ans"]:
                                    active_door.completed = True
                                    doors_completed.add(active_door.num)
                                    score += 100
                                    flash_msg = ""; flash_timer = 0
                                    state = C.FADE_IN
                                else:
                                    player.lives -= 1
                                    flash("Wrong!  Try again!", C.RED, 120)
                                    if player.lives <= 0:
                                        state = C.GAMEOVER
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
                    else:
                        full_reset(lvl + 1, score, player.lives)

                elif state in (C.GAMEOVER, C.GAMEWIN):
                    savegame.delete()
                    full_reset(1, 0, 3, keep_grade=False)
                    music.play(0)

        # ── Update ───────────────────────────────────────────────────────────
        if state == C.CUTSCENE:
            if cutscene.update():
                music.play(0)   # level1.mp3 is now index 0 (cutscene.mp3 excluded)
                state = C.TITLE

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
                music.play_question_track()
                state = C.DOOR_QUESTION

        elif state == C.FADE_IN:
            fade_alpha = max(0, fade_alpha - C.FADE_SPEED)
            if fade_alpha <= 0:
                music.resume_stage(stage_track_idx)
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
            draw_hud(lvl, player.lives, score, player.keys, doors_completed)

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
            )
            if flash_timer > 0:
                flash_timer -= 1

        elif state == C.CUTSCENE:
            cutscene.draw()

        elif state == C.SPLASH:
            draw_splash()
        elif state == C.TITLE:
            draw_title(title_sel, savegame.exists())
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
            draw_lvl_done(lvl, score)
        elif state == C.GAMEOVER:
            draw_gameover(score)
        elif state == C.GAMEWIN:
            draw_gamewin(score)

        display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
