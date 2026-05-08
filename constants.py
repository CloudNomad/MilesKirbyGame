"""
constants.py – All game constants, colors, layout values, and states.
No pygame dependency so this can be imported anywhere safely.
"""

# ─── Screen ───────────────────────────────────────────────────────────────────
SW, SH = 1100, 650   # screen width / height
FPS    = 60

# ─── Layout ───────────────────────────────────────────────────────────────────
DW, DH = 90, 130     # door width / height
PR     = 30          # player radius
SPEED  = 5
TOTAL  = 6           # total number of levels
WT     = 18          # wall strip thickness

# HUD is a small semi-transparent overlay – does NOT reserve screen space
HUD_H  = 44          # height of the translucent stats strip at the top

# Fixed door positions – flush with screen edges (full-screen stage)
# Door 1: top-center wall
D1X = (SW - DW) // 2          # 505
D1Y = 0                        # flush with top edge

# Door 2: bottom-center wall
D2X = (SW - DW) // 2          # 505
D2Y = SH - DH                  # 520

# Door 3: right-center wall
D3X = SW - DW                  # 1010
D3Y = (SH - DH) // 2          # 260

# ─── Colors ───────────────────────────────────────────────────────────────────
WHITE   = (255, 255, 255);  BLACK   = (  0,   0,   0)
PINK    = (255, 182, 193);  HOTPNK  = (255, 105, 180)
RED     = (200,  30,  30);  DKRED   = (140,  15,  15)
BLUE    = ( 30,  80, 200);  DKBLUE  = ( 15,  40, 120)
GOLD    = (255, 215,   0);  YELLOW  = (255, 230,  50)
GREEN   = ( 50, 200,  80);  DKGRN   = ( 20, 130,  50)
CYAN    = ( 50, 220, 220);  ORANGE  = (255, 150,  50)
GRAY    = (150, 150, 150);  DKGRAY  = ( 60,  60,  60)
LGRAY   = (200, 200, 200);  LPURPLE = (200, 160, 255)

BG      = (240, 248, 255)   # soft white-blue background
WALL_C  = (155, 170, 195)   # wall fill
WALL_LT = (180, 195, 218)   # wall highlight edge
WALL_DK = (110, 128, 158)   # wall shadow edge

# ─── Game states ──────────────────────────────────────────────────────────────
INTRO         = 0
PLAY          = 1
BONUS_Q       = 2
BONUS_R       = 3
LVLDONE       = 4
GAMEOVER      = 5
GAMEWIN       = 6
SPLASH        = 7   # animated logo / splash screen (first thing shown)
TITLE         = 8   # main menu (New Game / Load / Options / Credits)
TITLE_OPTIONS = 9   # options submenu (volume, display mode)
TITLE_CREDITS = 10  # credits screen
GRADE_SELECT  = 11  # grade-selection screen shown before intro
FADE_OUT      = 12  # fading to black before door question
DOOR_QUESTION = 13  # full-screen per-door question screen
FADE_IN       = 14  # fading back in after answering
CUTSCENE      = 15  # opening cinematic (before title screen)
CHAR_SELECT   = 16  # character selection screen
DOOR_CORRECT  = 17  # epic star-reveal popup after a correct door answer
TRANSIT       = 18  # cinematic transition between worlds (generic)
INTRO_FADE    = 19  # pre-opening text-fade sequence ("It was a peaceful day…")

# ─── Fade speed ───────────────────────────────────────────────────────────────
FADE_SPEED = 9      # alpha units per frame (255/9 ≈ 28 frames = ~0.5 s at 60 fps)

# ─── Door subject definitions ─────────────────────────────────────────────────
DOOR_SUBJECTS = {
    1: {"name": "Grammar",    "color": (30,  80,  200)},
    2: {"name": "Vocabulary", "color": (20,  160,  80)},
    3: {"name": "Science",    "color": (130,  50, 200)},
}
