"""
Tokens are the atomic unit of frames.
A token represents any object that can be on a pacman board (including the walls).
A frame really consists of a collection of tokens.
It is up to specific views to know how to interpret tokens into displayable objects.

Internally tokens are just ints, so we can do math on them.
We typically reserve a range of numbers for some related type of tokens,
like all walls or agents.
Then, we establish some "base" tokens within each group,
like the first red wall or the first yellow pacman.
Then, we can add known/computed constants to the base tokens to get a specific token,
like a red top-left corner wall or a pacman facing up with an open mouth.
"""

from pacai.core.directions import Directions

# There are 4 frames in each animation cycle.
# See getAnimationToken() for details on how animation frames are laid out.
ANIMATION_CYCLE = 4

EMPTY_TOKEN = 0
HIGHLIGHT_TOKEN = 1
SCARED_GHOST_TOKEN = 10

# Reserve 100s for food.
FOOD_START = 100
FOOD_OFFSET = 1
CAPSULE_OFFSET = 2
DEFAULT_FOOD_BASE = 100
RED_FOOD_BASE = 110
BLUE_FOOD_BASE = 120
FOOD_END = 199

# Reserve 200s for walls.
WALL_START = 200
BLUE_WALL_BASE = 200
RED_WALL_BASE = 250
WALL_END = 299

# Pacman gets the 1000s.
PACMAN_START = 1000
PACMAN_1 = 1100
PACMAN_2 = 1200
PACMAN_3 = 1300
PACMAN_4 = 1400
PACMAN_5 = 1500
PACMAN_6 = 1600
PACMAN_7 = 1700
PACMAN_END = 1800

# Ghosts get the 2000s.
GHOST_START = 2000
GHOST_1 = 2100
GHOST_2 = 2200
GHOST_3 = 2300
GHOST_4 = 2400
GHOST_5 = 2500
GHOST_6 = 2600
GHOST_END = 2700

def getAnimationToken(baseToken, direction, frame):
    """
    Get the token for a specific animation frame (for an agent).
    Animation frames are grouped by direction.
    The initial frame (0) is always the stopped animation.
    Then the cardinal directions (NESW) are cycled through.
    Each direction has ANIMATION_CYCLE number of tokens.
    """

    if (direction == Directions.STOP):
        return baseToken

    directionIndex = Directions.CARDINAL.index(direction)

    return baseToken + 1 + (directionIndex * ANIMATION_CYCLE) + (frame % ANIMATION_CYCLE)

def getWallToken(baseToken, hasWallN, hasWallE, hasWallS, hasWallW):
    """
    Given information about a wall's cardinal neighbors,
    compute the correct type of wall to use.
    To get the pacman "tubular" look, adjacent walls will look connected
    and not have a line between them.
    The computation is similar to POSIX permission bits,
    all combinations produce unique sums.
    """

    N_WALL = 1
    S_WALL = 2
    E_WALL = 4
    W_WALL = 8

    token = baseToken

    if (hasWallN):
        token += N_WALL

    if (hasWallE):
        token += E_WALL

    if (hasWallS):
        token += S_WALL

    if (hasWallW):
        token += W_WALL

    return token

def isCapsule(token):
    return token >= FOOD_START and token <= FOOD_END and token % 2 == 0

def isFood(token):
    return token >= FOOD_START and token <= FOOD_END and token % 2 == 1

def isGhost(token):
    return token >= GHOST_START and token <= GHOST_END

def isPacman(token):
    return token >= PACMAN_START and token <= PACMAN_END

def isWall(token):
    return token >= WALL_START and token <= WALL_END
