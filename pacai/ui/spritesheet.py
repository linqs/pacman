"""
The graphics for pacman are held in a spritesheet.
This file knows how to read a spritesheet and map sprites to tokens.
"""

from PIL import Image

from pacai.core.directions import Directions
from pacai.ui import token

# The size of each sprite square.
SQUARE_SIZE = 50

# The row where several miscellaneous items appear on.
MISC_ROW = 13

# The different types of food that appear.
SPRITE_SHEET_FOOD_TYPES = [
    token.DEFAULT_FOOD_BASE,
    token.RED_FOOD_BASE,
    token.BLUE_FOOD_BASE,
]

# The different wall types that appear (their base token number and spritesheet row).
SPRITE_SHEET_WALL_TYPES = [
    (token.BLUE_WALL_BASE, 14),
    (token.RED_WALL_BASE, 15),
]

# The order that the wall sprites appear in the sheet.
# True indicates that there is a wall adjacent in that cardinal direction (N, E, S, W).
# See token.getWallToken().
SPRITE_SHEET_WALL_ORDER = [
    (False, False, False, False),
    (False, False, False, True),
    (False, False, True, False),
    (False, False, True, True),
    (False, True, False, False),
    (False, True, False, True),
    (False, True, True, False),
    (False, True, True, True),
    (True, False, False, False),
    (True, False, False, True),
    (True, False, True, False),
    (True, False, True, True),
    (True, True, False, False),
    (True, True, False, True),
    (True, True, True, False),
    (True, True, True, True),
]

# The different types of agents in the spritesheet.
SPRITE_SHEET_AGENTS = [
    (token.PACMAN_1, 0),
    (token.PACMAN_2, 1),
    (token.PACMAN_3, 2),
    (token.PACMAN_4, 3),
    (token.PACMAN_5, 4),
    (token.PACMAN_6, 5),
    (token.PACMAN_7, 6),
    (token.GHOST_1, 7),
    (token.GHOST_2, 8),
    (token.GHOST_3, 9),
    (token.GHOST_4, 10),
    (token.GHOST_5, 11),
    (token.GHOST_6, 12),
]

def loadSpriteSheet(path):
    spritesheet = Image.open(path)

    sprites = {}

    # Load the food.
    miscColumnIndex = 0
    for foodTypeBase in SPRITE_SHEET_FOOD_TYPES:
        for foodItem in [token.FOOD_OFFSET, token.CAPSULE_OFFSET]:
            foodToken = foodTypeBase + foodItem
            sprites[foodToken] = _cropSprite(spritesheet, MISC_ROW, miscColumnIndex)
            miscColumnIndex += 1

    # The scared ghost is after the food.
    sprites[token.SCARED_GHOST_TOKEN] = _cropSprite(spritesheet, MISC_ROW, miscColumnIndex)

    # Load all the wall sprites.
    for (wallTypeBase, row) in SPRITE_SHEET_WALL_TYPES:
        for wallIndex in range(len(SPRITE_SHEET_WALL_ORDER)):
            adjacentWalls = SPRITE_SHEET_WALL_ORDER[wallIndex]
            wallToken = token.getWallToken(wallTypeBase, *adjacentWalls)

            sprites[wallToken] = _cropSprite(spritesheet, row, wallIndex)

    # Load all the agents.
    for (agentBaseToken, row) in SPRITE_SHEET_AGENTS:
        # Load the stopped sprite.
        sprites[agentBaseToken] = _cropSprite(spritesheet, row, 0)

        # Now load animations.
        for direction in Directions.CARDINAL:
            for frame in range(token.ANIMATION_CYCLE):
                # We need the offset to crop the sprite, so pass 0 in as the base token.
                animationOffset = token.getAnimationToken(0, direction, frame)
                agentToken = agentBaseToken + animationOffset
                sprites[agentToken] = _cropSprite(spritesheet, row, animationOffset)

    return sprites

def _cropSprite(spritesheet, row, col):
    # (left, upper, right, lower)
    rectangle = (
        col * SQUARE_SIZE,
        row * SQUARE_SIZE,
        (col + 1) * SQUARE_SIZE,
        (row + 1) * SQUARE_SIZE,
    )

    return spritesheet.crop(rectangle)
