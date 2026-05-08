"""
music.py – Background music manager.

Drop audio files into  assets/music/  and they are picked up automatically.
Supported format: .mp3

Controls (handled in game.py):
    M  – mute / unmute
    N  – next track
    B  – previous track
    ]  – volume up  (+10 %)
    [  – volume down (−10 %)

Tracks are played in alphabetical filename order and loop continuously.
If the folder is empty or missing, all calls are silent no-ops.

Usage
──────
    import music
    music.init()          # call after pygame.init()
    music.play()          # start playing track 0

    music.next_track()    # advance one track
    music.prev_track()    # go back one track
    music.toggle_mute()   # mute / unmute

    # In your draw loop you can show:
    music.track_name()    # → "02 Battle Theme"  (filename without extension)
    music.is_muted()      # → False
    music.volume()        # → 0.7  (0.0 – 1.0)
    music.track_index()   # → 1  (0-based index into track list)
    music.track_count()   # → 4
"""

import os
import pygame

# ── Internal state ─────────────────────────────────────────────────────────────
_tracks: list[str] = []     # stage track paths (question.mp3 excluded)
_index:  int       = 0      # currently loaded track index
_muted:  bool      = False
_volume: float     = 0.7    # 0.0 – 1.0

_question_track:   str | None = None   # path to question.mp3    (None if not found)
_cutscene_track:   str | None = None   # path to cutscene.mp3    (None if not found)
_cutscene2_track:  str | None = None   # path to cutscene2.mp3   (None if not found)
_main_menu_track:  str | None = None   # path to MainMenu.mp3    (None if not found)
_main_menu_active: bool       = False  # True while MainMenu.mp3 is the loaded track

_MUSIC_DIR        = os.path.join(os.path.dirname(__file__), "assets", "music")
_SUPPORTED        = {".mp3"}
_QUESTION_FILE    = "question.mp3"    # reserved — door question screen
_CUTSCENE_FILE    = "cutscene.mp3"    # reserved — opening cutscene
_CUTSCENE2_FILE   = "cutscene2.mp3"   # reserved — level 1→2 transition cutscene
_MAIN_MENU_FILE   = "MainMenu.mp3"    # reserved — title screen

# MainMenu.mp3 is 75.05 s; loop 3 s early so the transition is seamless.
_MAIN_MENU_LOOP_MS = int((75.05 - 3.0) * 1000)   # 72 050 ms


# ── Public API ─────────────────────────────────────────────────────────────────

def init() -> None:
    """
    Scan assets/music/ for playable files.
    Must be called after pygame.init() (pygame.mixer is initialised here).
    Safe to call even if the folder is missing.

    question.mp3 is reserved for the door-question screen and is excluded
    from the normal stage playlist.
    """
    global _tracks, _index, _question_track, _cutscene_track, _cutscene2_track, _main_menu_track

    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"[music] pygame.mixer could not initialise: {e}")
        return

    if not os.path.isdir(_MUSIC_DIR):
        print(f"[music] No music folder found at: {_MUSIC_DIR}")
        print( "[music] Create  assets/music/  and drop .mp3 files in it.")
        return

    all_files = sorted(
        os.path.join(_MUSIC_DIR, f)
        for f in os.listdir(_MUSIC_DIR)
        if os.path.splitext(f)[1].lower() in _SUPPORTED
    )

    # Separate reserved tracks from the stage playlist
    _RESERVED = {_QUESTION_FILE, _CUTSCENE_FILE, _CUTSCENE2_FILE, _MAIN_MENU_FILE}
    q_path  = os.path.join(_MUSIC_DIR, _QUESTION_FILE)
    c_path  = os.path.join(_MUSIC_DIR, _CUTSCENE_FILE)
    c2_path = os.path.join(_MUSIC_DIR, _CUTSCENE2_FILE)
    mm_path = os.path.join(_MUSIC_DIR, _MAIN_MENU_FILE)
    _question_track  = q_path  if os.path.isfile(q_path)  else None
    _cutscene_track  = c_path  if os.path.isfile(c_path)  else None
    _cutscene2_track = c2_path if os.path.isfile(c2_path) else None
    _main_menu_track = mm_path if os.path.isfile(mm_path) else None
    _tracks = [t for t in all_files
               if os.path.basename(t) not in _RESERVED]
    _index  = 0

    if _question_track:
        print(f"[music] Question track:   {_QUESTION_FILE}")
    else:
        print(f"[music] No question track found (add assets/music/{_QUESTION_FILE} for a dedicated track)")
    if _cutscene_track:
        print(f"[music] Cutscene track:   {_CUTSCENE_FILE}")
    else:
        print(f"[music] No cutscene track found (add assets/music/{_CUTSCENE_FILE} for a dedicated track)")
    if _cutscene2_track:
        print(f"[music] Cutscene 2 track: {_CUTSCENE2_FILE}")
    else:
        print(f"[music] No cutscene2 track found (add assets/music/{_CUTSCENE2_FILE} for a dedicated track)")
    if _main_menu_track:
        print(f"[music] Main menu track:  {_MAIN_MENU_FILE}")
    else:
        print(f"[music] No main menu track found (add assets/music/{_MAIN_MENU_FILE} for a dedicated track)")

    if _tracks:
        print(f"[music] Found {len(_tracks)} stage track(s):")
        for i, t in enumerate(_tracks):
            print(f"         {i+1:>2}.  {os.path.basename(t)}")
    else:
        print(f"[music] No stage tracks found in assets/music/")


def play(index: int = 0) -> None:
    """Load and start playing the track at *index* (loops indefinitely)."""
    global _index
    pygame.mixer.music.stop()   # always stop whatever is currently playing
    if not _tracks:
        return
    _index = index % len(_tracks)
    _load_and_play(_index)


def next_track() -> None:
    """Advance to the next track (wraps around)."""
    if not _tracks:
        return
    play((_index + 1) % len(_tracks))


def prev_track() -> None:
    """Go back to the previous track (wraps around)."""
    if not _tracks:
        return
    play((_index - 1) % len(_tracks))


def toggle_mute() -> None:
    """Mute or unmute without stopping playback."""
    global _muted
    if not _tracks:
        return
    _muted = not _muted
    pygame.mixer.music.set_volume(0.0 if _muted else _volume)


def volume_up(step: float = 0.1) -> None:
    """Increase volume by *step* (capped at 1.0)."""
    set_volume(min(1.0, _volume + step))


def volume_down(step: float = 0.1) -> None:
    """Decrease volume by *step* (floored at 0.0)."""
    set_volume(max(0.0, _volume - step))


def set_volume(v: float) -> None:
    """Set volume directly (0.0 – 1.0). Un-mutes automatically."""
    global _volume, _muted
    _volume = max(0.0, min(1.0, v))
    _muted  = False
    pygame.mixer.music.set_volume(_volume)  # always apply (covers reserved tracks too)


def stop() -> None:
    """Stop playback entirely."""
    if _tracks:
        pygame.mixer.music.stop()


def play_question_track() -> None:
    """
    Play the dedicated question track (question.mp3) on loop.
    Falls back to next_track() if question.mp3 was not found.
    """
    if _question_track:
        try:
            pygame.mixer.music.load(_question_track)
            pygame.mixer.music.set_volume(0.0 if _muted else _volume)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"[music] Could not play question track: {e}")
            next_track()
    else:
        next_track()


def play_cutscene_track() -> None:
    """
    Play the dedicated cutscene track (cutscene.mp3) on loop.
    Falls back to play(0) if cutscene.mp3 was not found.
    cutscene.mp3 is excluded from the stage playlist so it never
    bleeds into normal level music.
    """
    if _cutscene_track:
        try:
            pygame.mixer.music.load(_cutscene_track)
            pygame.mixer.music.set_volume(0.0 if _muted else _volume)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"[music] Could not play cutscene track: {e}")
            play(0)
    else:
        play(0)


def play_cutscene2_track() -> None:
    """
    Play the dedicated level-transition track (cutscene2.mp3) on loop.
    If the file is missing, the currently playing track continues unchanged —
    level 2 music will start automatically when full_reset() is called after
    the cutscene ends.
    """
    if _cutscene2_track:
        try:
            pygame.mixer.music.load(_cutscene2_track)
            pygame.mixer.music.set_volume(0.0 if _muted else _volume)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"[music] Could not play cutscene2 track: {e}")
            pygame.mixer.music.stop()
    else:
        print(f"[music] cutscene2.mp3 not found — stopping music during transition"
              f" (add assets/music/cutscene2.mp3 for a dedicated track)")
        pygame.mixer.music.stop()


def play_main_menu_track() -> None:
    """
    Play MainMenu.mp3 for the title screen.
    Call update_main_menu() every frame while on any title state so the track
    loops 3 seconds before its natural end (at 72.05 s of 75.05 s total).
    """
    global _main_menu_active
    _main_menu_active = False
    if _main_menu_track:
        try:
            pygame.mixer.music.load(_main_menu_track)
            pygame.mixer.music.set_volume(0.0 if _muted else _volume)
            pygame.mixer.music.play(0)   # play once; update_main_menu handles re-loop
            _main_menu_active = True
        except pygame.error as e:
            print(f"[music] Could not play main menu track: {e}")
            play(0)
    else:
        play(0)


def update_main_menu() -> None:
    """Call once per frame while in any title state. Re-loops 3 s before track end."""
    if not _main_menu_active:
        return
    pos = pygame.mixer.music.get_pos()   # ms since last play(); -1 if stopped
    if pos < 0 or pos >= _MAIN_MENU_LOOP_MS:
        pygame.mixer.music.play(0)


def resume_stage(index: int = 0) -> None:
    """Resume playing the stage track at the given index."""
    play(index)


# ── Read-only state helpers ────────────────────────────────────────────────────

def track_name() -> str:
    """Filename of the current track (no extension), or empty string."""
    if not _tracks:
        return ""
    return os.path.splitext(os.path.basename(_tracks[_index]))[0]


def is_muted() -> bool:
    return _muted


def volume() -> float:
    return _volume


def track_index() -> int:
    return _index


def track_count() -> int:
    return len(_tracks)


def has_music() -> bool:
    return bool(_tracks)


# ── Internal helpers ───────────────────────────────────────────────────────────

def _load_and_play(index: int) -> None:
    try:
        pygame.mixer.music.load(_tracks[index])
        pygame.mixer.music.set_volume(0.0 if _muted else _volume)
        pygame.mixer.music.play(-1)   # -1 = loop forever
    except pygame.error as e:
        print(f"[music] Could not play '{os.path.basename(_tracks[index])}': {e}")
