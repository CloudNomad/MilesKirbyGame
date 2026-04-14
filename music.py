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

_question_track:  str | None = None   # path to question.mp3  (None if not found)
_cutscene_track:  str | None = None   # path to cutscene.mp3  (None if not found)

_MUSIC_DIR       = os.path.join(os.path.dirname(__file__), "assets", "music")
_SUPPORTED       = {".mp3"}
_QUESTION_FILE   = "question.mp3"    # reserved — door question screen
_CUTSCENE_FILE   = "cutscene.mp3"    # reserved — opening cutscene


# ── Public API ─────────────────────────────────────────────────────────────────

def init() -> None:
    """
    Scan assets/music/ for playable files.
    Must be called after pygame.init() (pygame.mixer is initialised here).
    Safe to call even if the folder is missing.

    question.mp3 is reserved for the door-question screen and is excluded
    from the normal stage playlist.
    """
    global _tracks, _index, _question_track, _cutscene_track

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
    _RESERVED = {_QUESTION_FILE, _CUTSCENE_FILE}
    q_path = os.path.join(_MUSIC_DIR, _QUESTION_FILE)
    c_path = os.path.join(_MUSIC_DIR, _CUTSCENE_FILE)
    _question_track = q_path if os.path.isfile(q_path) else None
    _cutscene_track = c_path if os.path.isfile(c_path) else None
    _tracks = [t for t in all_files
               if os.path.basename(t).lower() not in _RESERVED]
    _index  = 0

    if _question_track:
        print(f"[music] Question track:  {_QUESTION_FILE}")
    else:
        print(f"[music] No question track found (add assets/music/{_QUESTION_FILE} for a dedicated track)")
    if _cutscene_track:
        print(f"[music] Cutscene track:  {_CUTSCENE_FILE}")
    else:
        print(f"[music] No cutscene track found (add assets/music/{_CUTSCENE_FILE} for a dedicated track)")

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
