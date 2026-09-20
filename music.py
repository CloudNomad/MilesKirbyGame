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
import sys
import pygame

# ── Internal state ─────────────────────────────────────────────────────────────
_tracks: list[str] = []     # stage track paths (question.mp3 excluded)
_index:  int       = 0      # currently loaded track index
_muted:  bool      = False
_volume: float     = 0.7    # 0.0 – 1.0

_question_track:       str | None  = None   # path to question.mp3
_cutscene_track:       str | None  = None   # path to cutscene.mp3
_main_menu_track:      str | None  = None   # path to MainMenu.mp3
_kirby_cutscene_track: str | None  = None   # path to cutscene_kirby.mp3
_miles_cutscene_track: str | None  = None   # path to cutscene_miles.mp3
_main_menu_active:     bool        = False  # True while MainMenu.mp3 is the loaded track
_transition_tracks:    dict        = {}     # to_world (2-6) → path or None

_MUSIC_DIR        = os.path.join(
    getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))),
    "assets", "music"
)
_SUPPORTED        = {".mp3"}
_QUESTION_FILE        = "question.mp3"         # reserved — door question screen
_CUTSCENE_FILE        = "cutscene.mp3"         # reserved — opening cutscene
_MAIN_MENU_FILE       = "MainMenu.mp3"         # reserved — title screen
_KIRBY_CUTSCENE_FILE  = "cutscene_kirby.mp3"  # reserved — Kirby character intro
_MILES_CUTSCENE_FILE  = "cutscene_miles.mp3"  # reserved — Miles character intro
# World transition tracks: cutscene2.mp3 … cutscene6.mp3
_TRANSITION_FILES = {w: f"cutscene{w}.mp3" for w in range(2, 7)}

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
    global _tracks, _index, _question_track, _cutscene_track, _main_menu_track
    global _kirby_cutscene_track, _miles_cutscene_track, _transition_tracks

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

    # Build transition track dict (world 2-6)
    _transition_tracks = {}
    _transition_fnames = set()
    for w, fname in _TRANSITION_FILES.items():
        path = os.path.join(_MUSIC_DIR, fname)
        _transition_tracks[w] = path if os.path.isfile(path) else None
        _transition_fnames.add(fname)
        if _transition_tracks[w]:
            print(f"[music] Transition track (-> world {w}): {fname}")
        else:
            print(f"[music] No transition track for world {w} (add assets/music/{fname})")

    # Separate remaining reserved tracks from the stage playlist
    _RESERVED = (
        {_QUESTION_FILE, _CUTSCENE_FILE, _MAIN_MENU_FILE,
         _KIRBY_CUTSCENE_FILE, _MILES_CUTSCENE_FILE}
        | _transition_fnames
    )
    q_path  = os.path.join(_MUSIC_DIR, _QUESTION_FILE)
    c_path  = os.path.join(_MUSIC_DIR, _CUTSCENE_FILE)
    mm_path = os.path.join(_MUSIC_DIR, _MAIN_MENU_FILE)
    kc_path = os.path.join(_MUSIC_DIR, _KIRBY_CUTSCENE_FILE)
    mc_path = os.path.join(_MUSIC_DIR, _MILES_CUTSCENE_FILE)
    _question_track       = q_path  if os.path.isfile(q_path)  else None
    _cutscene_track       = c_path  if os.path.isfile(c_path)  else None
    _main_menu_track      = mm_path if os.path.isfile(mm_path) else None
    _kirby_cutscene_track = kc_path if os.path.isfile(kc_path) else None
    _miles_cutscene_track = mc_path if os.path.isfile(mc_path) else None
    _tracks = [t for t in all_files
               if os.path.basename(t) not in _RESERVED]
    _index  = 0

    if _question_track:
        print(f"[music] Question track:      {_QUESTION_FILE}")
    else:
        print(f"[music] No question track found (add assets/music/{_QUESTION_FILE})")
    if _cutscene_track:
        print(f"[music] Cutscene track:      {_CUTSCENE_FILE}")
    else:
        print(f"[music] No cutscene track found (add assets/music/{_CUTSCENE_FILE})")
    if _main_menu_track:
        print(f"[music] Main menu track:     {_MAIN_MENU_FILE}")
    else:
        print(f"[music] No main menu track found (add assets/music/{_MAIN_MENU_FILE})")
    if _kirby_cutscene_track:
        print(f"[music] Kirby intro track:   {_KIRBY_CUTSCENE_FILE}")
    else:
        print(f"[music] No Kirby intro track (add assets/music/{_KIRBY_CUTSCENE_FILE})")
    if _miles_cutscene_track:
        print(f"[music] Miles intro track:   {_MILES_CUTSCENE_FILE}")
    else:
        print(f"[music] No Miles intro track (add assets/music/{_MILES_CUTSCENE_FILE})")

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


def play_char_cutscene_track(char: str) -> None:
    """
    Play the character-specific intro track (cutscene_kirby.mp3 or
    cutscene_miles.mp3).  Falls back to the shared cutscene track, then play(0).
    """
    track = _kirby_cutscene_track if char == "kirby" else _miles_cutscene_track
    fallback = _cutscene_track
    chosen = track or fallback
    if chosen:
        try:
            pygame.mixer.music.load(chosen)
            pygame.mixer.music.set_volume(0.0 if _muted else _volume)
            pygame.mixer.music.play(-1)
            return
        except pygame.error as e:
            print(f"[music] Could not play char cutscene track: {e}")
    play(0)


def play_transition_track(to_world: int) -> None:
    """
    Play the world-transition track for the given destination world (2-6).
    Uses cutscene{to_world}.mp3; stops music if the file is not found.
    """
    global _main_menu_active
    _main_menu_active = False
    track = _transition_tracks.get(to_world)
    if track:
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(0.0 if _muted else _volume)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"[music] Could not play transition track for world {to_world}: {e}")
            pygame.mixer.music.stop()
    else:
        pygame.mixer.music.stop()


def play_cutscene2_track() -> None:
    """Alias kept for compatibility — plays the world-1→2 transition track."""
    play_transition_track(2)


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
