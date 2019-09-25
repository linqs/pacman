from PIL import Image
from PIL import ImageDraw

from pacai.core.directions import Directions
from pacai.util import util

# Reserve 200 tokens for walls.
BLUE_WALL_BASE = 200
RED_WALL_BASE = 250
WALL_END = 299

# Reserve 100 tokens for food.
DEFAULT_FOOD_BASE = 100
RED_FOOD_BASE = 110
BLUE_FOOD_BASE = 120
FOOD_END = 199

# TODO(eriq): Frames can probably be more effiicent with bit packing.
class Frame(object):
    """
    A general representation of that can be seen on-screen at a given time.
    Frames are the basic units of the views.
    """

    SQUARE_SIZE = 50

    STOP = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    DIRECTIONS = [
        NORTH,
        EAST,
        SOUTH,
        WEST,
    ]

    # There are 4 frames in each animation cycle.
    ANIMATION_CYCLE = 4

    # Token to mark what can occupy different locations.
    EMPTY = 0
    FOOD = 1
    CAPSULE = 2
    SCARED_GHOST = 3

    # Animations fill the room between the explicitly listed tokens.
    PACMAN_1 = 1100
    PACMAN_2 = 1200
    PACMAN_3 = 1300
    PACMAN_4 = 1400
    PACMAN_5 = 1500
    PACMAN_6 = 1600
    PACMAN_7 = 1700
    PACMAN_END = 1800

    GHOST_1 = 2100
    GHOST_2 = 2200
    GHOST_3 = 2300
    GHOST_4 = 2400
    GHOST_5 = 2500
    GHOST_6 = 2600
    GHOST_END = 2700

    # Constants specific to the sprite sheet.

    # The row where several miscellaneous items appear on.
    MISC_ROW = 13

    # The different types of food that appear.
    SPRITE_SHEET_FOOD_TYPES = [
        DEFAULT_FOOD_BASE,
        RED_FOOD_BASE,
        BLUE_FOOD_BASE,
    ]

    # The different wall types that appear (their base token number and spritesheet row).
    SPRITE_SHEET_WALL_TYPES = [
        (BLUE_WALL_BASE, 14),
        (RED_WALL_BASE, 15),
    ]

    # The order that the wall sprites appear in the sheet.
    # True indicates that there is a wall adjacent in that cardinal direction (N, E, S, W).
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

    SPRITE_SHEET_AGENTS = [
        (PACMAN_1, 0),
        (PACMAN_2, 1),
        (PACMAN_3, 2),
        (PACMAN_4, 3),
        (PACMAN_5, 4),
        (PACMAN_6, 5),
        (PACMAN_7, 6),
        (GHOST_1, 7),
        (GHOST_2, 8),
        (GHOST_3, 9),
        (GHOST_4, 10),
        (GHOST_5, 11),
        (GHOST_6, 12),
    ]

    def __init__(self, frame, state, turn):
        self._frame = frame
        self._turn = turn

        self._height = state.getInitialLayout().getHeight()
        self._width = state.getInitialLayout().getWidth()

        # All items on the board are at integral potision.
        self._board = self._buildBoard(state)

        # Agents may not be at integral positions, so they are represented independently.
        self._agentTokens = self._getAgentTokens(state)

    def getAgents(self):
        return self._agentTokens

    def getDiscreteAgents(self):
        """
        Get the agentTokens, but with interger positions.
        """

        agentTokens = {}

        for (position, agent) in self._agentTokens.items():
            agentTokens[util.nearestPoint(position)] = agent

        return agentTokens

    def getHeight(self):
        return self._height

    def getToken(self, x, y):
        return self._board[x][y]

    def getCol(self, x):
        return self._board[x]

    def getWidth(self):
        return self._width

    @staticmethod
    def isCapsule(token):
        return token >= DEFAULT_FOOD_BASE and token <= FOOD_END and token % 2 == 0

    @staticmethod
    def isFood(token):
        return token >= DEFAULT_FOOD_BASE and token <= FOOD_END and token % 2 == 1

    @staticmethod
    def isGhost(token):
        return token >= Frame.GHOST_1 and token <= Frame.GHOST_END

    @staticmethod
    def isPacman(token):
        return token >= Frame.PACMAN_1 and token <= Frame.PACMAN_END

    @staticmethod
    def isWall(token):
        return token >= BLUE_WALL_BASE and token <= WALL_END

    @staticmethod
    def loadSpriteSheet(path):
        spritesheet = Image.open(path)

        sprites = {}

        # Load the food.
        miscColumnIndex = 0
        for foodTypeBase in Frame.SPRITE_SHEET_FOOD_TYPES:
            for foodItem in [Frame.FOOD, Frame.CAPSULE]:
                token = foodTypeBase + foodItem
                sprites[token] = Frame._cropSprite(spritesheet, Frame.MISC_ROW, miscColumnIndex)
                miscColumnIndex += 1

        # The scared ghost is after the food.
        sprites[Frame.SCARED_GHOST] = Frame._cropSprite(spritesheet, Frame.MISC_ROW,
                miscColumnIndex)

        # Load all the wall sprites.
        for (wallTypeBase, row) in Frame.SPRITE_SHEET_WALL_TYPES:
            for wallIndex in range(len(Frame.SPRITE_SHEET_WALL_ORDER)):
                adjacentWalls = Frame.SPRITE_SHEET_WALL_ORDER[wallIndex]
                wallToken = Frame._computeWallToken(wallTypeBase, *adjacentWalls)

                sprites[wallToken] = Frame._cropSprite(spritesheet, row, wallIndex)

        # Load all the agents.
        for (agentBaseToken, row) in Frame.SPRITE_SHEET_AGENTS:
            # Load the stopped sprite.
            sprites[agentBaseToken] = Frame._cropSprite(spritesheet, row, 0)

            # Now load animations.
            for direction in Frame.DIRECTIONS:
                for frame in range(Frame.ANIMATION_CYCLE):
                    animationOffset = Frame._getAnimationOffset(direction, frame)
                    token = agentBaseToken + animationOffset
                    sprites[token] = Frame._cropSprite(spritesheet, row, animationOffset)

        return sprites

    def toImage(self, sprites = {}):
        size = (self._width * Frame.SQUARE_SIZE, self._height * Frame.SQUARE_SIZE)
        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)

        # First, draw the board.
        for x in range(self._width):
            for y in range(self._height):
                self._placeToken(x, y, self._board[x][y], sprites, image, draw)

        # Now, overlay the agents.
        for ((x, y), agentToken) in self._agentTokens.items():
            self._placeToken(x, y, agentToken, sprites, image, draw)

        return image

    def _buildBoard(self, state):
        board = self._width * [None]
        for x in range(self._width):

            items = self._height * [Frame.EMPTY]
            for y in range(self._height):
                if (state.hasWall(x, y)):
                    items[y] = self._getWallToken(x, y, state)
                elif (state.hasFood(x, y)):
                    items[y] = self._getFoodToken(x, y, state)
                elif (state.hasCapsule(x, y)):
                    items[y] = self._getCapsuleToken(x, y, state)

            board[x] = items

        return board

    @staticmethod
    def _computeWallToken(base, hasWallN, hasWallE, hasWallS, hasWallW):
        """
        Given information about a wall's cardinal neighbors,
        compute the correct type of wall to use.
        The computation is similar to POSIX permission bits,
        To get the pacman "tubular" look, adjacent walls will look connected
        and not have a line between them.
        all combinations produce unique sums.
        """

        N_WALL = 1
        E_WALL = 2
        S_WALL = 4
        W_WALL = 8

        code = base

        if (hasWallN):
            code += N_WALL

        if (hasWallE):
            code += E_WALL

        if (hasWallS):
            code += S_WALL

        if (hasWallW):
            code += W_WALL

        return code

    @staticmethod
    def _cropSprite(spritesheet, row, col):
        # (left, upper, right, lower)
        rectangle = (
            col * Frame.SQUARE_SIZE,
            row * Frame.SQUARE_SIZE,
            (col + 1) * Frame.SQUARE_SIZE,
            (row + 1) * Frame.SQUARE_SIZE,
        )

        return spritesheet.crop(rectangle)

    def _getAgentTokens(self, state):
        """
        Returns: {(x, y): token, ...}
        """

        tokens = {}

        for agentIndex in range(state.getNumAgents()):
            agentState = state.getAgentState(agentIndex)
            position = agentState.getPosition()

            if (agentState.isScaredGhost()):
                tokens[position] = Frame.SCARED_GHOST
            else:
                token = self._getAgentBaseToken(*position, agentIndex, state)

                direction = Frame._translateDirection(agentState.getDirection())

                # token += Frame._getAnimationOffset(direction, self._turn)
                token += Frame._getAnimationOffset(direction, self._frame)

                tokens[position] = token

        return tokens

    @staticmethod
    def _getAnimationOffset(direction, frame):
        """
        Get the token for a specific animation frame.
        """

        if (direction == Frame.STOP):
            return 0
        return 1 + (direction - 1) * Frame.ANIMATION_CYCLE + (frame % Frame.ANIMATION_CYCLE)

    def _getCapsuleToken(self, x, y, state):
        return self._getCapsuleBaseToken(x, y, state) + Frame.CAPSULE

    def _getFoodToken(self, x, y, state):
        return self._getFoodBaseToken(x, y, state) + Frame.FOOD

    def _getWallToken(self, x, y, state):
        hasWallN = False
        hasWallE = False
        hasWallS = False
        hasWallW = False

        baseToken = self._getWallBaseToken(x, y, state)

        if (y != self._height - 1):
            hasWallN = state.hasWall(x, y + 1)

        if (x != self._width - 1):
            hasWallE = state.hasWall(x + 1, y)

        if (y != 0):
            hasWallS = state.hasWall(x, y - 1)

        if (x != 0):
            hasWallW = state.hasWall(x - 1, y)

        return Frame._computeWallToken(baseToken, hasWallN, hasWallE, hasWallS, hasWallW)

    def _placeToken(self, x, y, token, sprites, image, draw):
        startPoint = self._toImageCoords(x, y)
        endPoint = self._toImageCoords(x + 1, y - 1)

        if (token in sprites):
            image.paste(sprites[token], startPoint, sprites[token])
        else:
            color = self._tokenToColor(token)
            draw.rectangle([startPoint, endPoint], fill = color)

    def _toImageCoords(self, x, y):
        # PIL has (0, 0) as the upper-left, while pacai has it as the lower-left.
        return (int(x * Frame.SQUARE_SIZE), int((self._height - 1 - y) * Frame.SQUARE_SIZE))

    def _tokenToColor(self, token):
        if (token == Frame.EMPTY):
            return (0, 0, 0)
        elif (self.isWall(token)):
            return (0, 51, 255)
        elif (self.isFood(token)):
            return (255, 255, 255)
        elif (self.isCapsule(token)):
            return (255, 0, 255)
        elif (self.isGhost(token)):
            return (229, 0, 0)
        elif (self.isPacman(token)):
            return (255, 255, 61)
        elif (token == Frame.SCARED_GHOST):
            return (0, 255, 0)
        else:
            return (0, 0, 0)

    @staticmethod
    def _translateDirection(direction):
        if (direction == Directions.NORTH):
            return Frame.NORTH
        elif (direction == Directions.EAST):
            return Frame.EAST
        elif (direction == Directions.SOUTH):
            return Frame.SOUTH
        elif (direction == Directions.WEST):
            return Frame.WEST
        else:
            return Frame.STOP

    # TODO(eriq): Abstract out Pacman and Capture frames, and split the blow methods acordingly.

    # Pacman

    def _getAgentBaseToken(self, x, y, agentIndex, state):
        if (state.getAgentState(agentIndex).isPacman()):
            return Frame.PACMAN_1
        else:
            return Frame.GHOST_1 + (agentIndex - 1) * 100

    def _getCapsuleBaseToken(self, x, y, state):
        return DEFAULT_FOOD_BASE

    def _getFoodBaseToken(self, x, y, state):
        return DEFAULT_FOOD_BASE

    def _getWallBaseToken(self, x, y, state):
        return BLUE_WALL_BASE

    # Capture
    """
    def _getAgentBaseToken(self, x, y, agentIndex, state):
        if (state.getAgentState(agentIndex).isPacman()):
            return Frame.PACMAN_2 + agentIndex * 100
        else:
            return Frame.GHOST_1 + agentIndex * 100

    def _getCapsuleBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return RED_FOOD_BASE
        else:
            return BLUE_FOOD_BASE

    def _getFoodBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return RED_FOOD_BASE
        else:
            return BLUE_FOOD_BASE


    def _getWallBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return RED_WALL_BASE
        else:
            return BLUE_WALL_BASE
    """
