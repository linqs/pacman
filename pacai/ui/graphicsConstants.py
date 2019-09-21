from pacai.ui import graphicsUtils

DEFAULT_ZOOM = 1.0
DEFAULT_FRAME_TIME = 0.0
DEFAULT_GIF_FRAME_SKIP = 0
DEFAULT_GIF_FPS = 10
DEFAULT_CAPTURE_ARG = False
DEFAULT_GIF_ARG = None
DEFAULT_PANE_FONT_SIZE = 24
DEFAULT_GRID_SIZE = 30.0
DEFAULT_TEXT_SIZE = 20
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = graphicsUtils.formatColor(0, 0, 0)
WALL_COLOR = graphicsUtils.formatColor(0, 51.0 / 255.0, 1)
INFO_PANE_COLOR = graphicsUtils.formatColor(0.4, 0.4, 0)
SCORE_COLOR = graphicsUtils.formatColor(0.9, 0.9, 0.9)
PACMAN_OUTLINE_WIDTH = 2
PACMAN_CAPTURE_OUTLINE_WIDTH = 4
WHITE = graphicsUtils.formatColor(1, 1, 1)
BLACK = graphicsUtils.formatColor(0, 0, 0)


GHOST_COLORS = [
    graphicsUtils.formatColor(0.9, 0, 0),  # Red
    graphicsUtils.formatColor(0, 0.3, 0.9),  # Blue
    graphicsUtils.formatColor(0.98, 0.41, 0.07),  # Orange
    graphicsUtils.formatColor(0.1, 0.75, 0.7),  # Green
    graphicsUtils.formatColor(1, 0.6, 0),  # Yellow
    graphicsUtils.formatColor(0.4, 0.13, 0.91),  # Purple
]

TEAM_COLORS = GHOST_COLORS[:2]

GHOST_SHAPE = [
    (0, 0.3),
    (0.25, 0.75),
    (0.5, 0.3),
    (0.75, 0.75),
    (0.75, -0.5),
    (0.5, -0.75),
    (-0.5, -0.75),
    (-0.75, -0.5),
    (-0.75, 0.75),
    (-0.5, 0.3),
    (-0.25, 0.75)
]
GHOST_SIZE = 0.65
SCARED_COLOR = graphicsUtils.formatColor(1, 1, 1)

GHOST_VEC_COLORS = list(map(graphicsUtils.colorToVector, GHOST_COLORS))

PACMAN_COLOR = graphicsUtils.formatColor(1, 1, 61.0 / 255)
PACMAN_SCALE = 0.5

# Food
FOOD_COLOR = graphicsUtils.formatColor(1, 1, 1)
FOOD_SIZE = 0.1

# Laser
LASER_COLOR = graphicsUtils.formatColor(1, 0, 0)
LASER_SIZE = 0.02

# Capsule graphics
CAPSULE_COLOR = graphicsUtils.formatColor(1, 1, 1)
CAPSULE_SIZE = 0.25

# Drawing walls
WALL_RADIUS = 0.15

# Fonts and Text Modifiers
DEFAULT_FONT = "Times"
CONSOLAS_FONT = "Consolas"
TIMES_FONT = "Times"
TEXT_MOD_BOLD = "bold"

# Teams
TEAM_BLUE = "BLUE TEAM"
TEAM_RED = "RED TEAM"
