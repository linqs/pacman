"""
A Frame is the base unit of a View.
Frames hold all the information necessary to draw the game in whatever medium
the view chooses.
"""

from PIL import Image
from PIL import ImageDraw

from pacai.ui import spritesheet
from pacai.ui import token
from pacai.util import util

class Frame(object):
    """
    A general representation of that can be seen on-screen at a given time.
    Frames are the basic units of the views.
    """

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

    def toImage(self, sprites = {}):
        size = (self._width * spritesheet.SQUARE_SIZE, self._height * spritesheet.SQUARE_SIZE)
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

            items = self._height * [token.EMPTY_TOKEN]
            for y in range(self._height):
                if (state.hasWall(x, y)):
                    items[y] = self._getWallToken(x, y, state)
                elif (state.hasFood(x, y)):
                    items[y] = self._getFoodToken(x, y, state)
                elif (state.hasCapsule(x, y)):
                    items[y] = self._getCapsuleToken(x, y, state)

            board[x] = items

        return board

    def _getAgentTokens(self, state):
        """
        Returns: {(x, y): token, ...}
        """

        tokens = {}

        for agentIndex in range(state.getNumAgents()):
            agentState = state.getAgentState(agentIndex)
            position = agentState.getPosition()

            if (agentState.isScaredGhost()):
                tokens[position] = token.SCARED_GHOST_TOKEN
            else:
                agentBaseToken = self._getAgentBaseToken(*position, agentIndex, state)
                direction = agentState.getDirection()

                # agentToken = token.getAnimationToken(agentBaseToken, direction, self._turn)
                agentToken = token.getAnimationToken(agentBaseToken, direction, self._frame)

                tokens[position] = agentToken

        return tokens

    def _getCapsuleToken(self, x, y, state):
        return self._getCapsuleBaseToken(x, y, state) + token.CAPSULE_OFFSET

    def _getFoodToken(self, x, y, state):
        return self._getFoodBaseToken(x, y, state) + token.FOOD_OFFSET

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

        return token.getWallToken(baseToken, hasWallN, hasWallE, hasWallS, hasWallW)

    def _placeToken(self, x, y, objectToken, sprites, image, draw):
        startPoint = self._toImageCoords(x, y)
        endPoint = self._toImageCoords(x + 1, y - 1)

        if (objectToken in sprites):
            image.paste(sprites[objectToken], startPoint, sprites[objectToken])
        else:
            color = self._tokenToColor(objectToken)
            draw.rectangle([startPoint, endPoint], fill = color)

    def _toImageCoords(self, x, y):
        # PIL has (0, 0) as the upper-left, while pacai has it as the lower-left.
        return (
            int(x * spritesheet.SQUARE_SIZE),
            int((self._height - 1 - y) * spritesheet.SQUARE_SIZE)
        )

    def _tokenToColor(self, objectToken):
        if (objectToken == token.EMPTY_TOKEN):
            return (0, 0, 0)
        elif (self.isWall(objectToken)):
            return (0, 51, 255)
        elif (self.isFood(objectToken)):
            return (255, 255, 255)
        elif (self.isCapsule(objectToken)):
            return (255, 0, 255)
        elif (self.isGhost(objectToken)):
            return (229, 0, 0)
        elif (self.isPacman(objectToken)):
            return (255, 255, 61)
        elif (objectToken == token.SCARED_GHOST_TOKEN):
            return (0, 255, 0)
        else:
            return (0, 0, 0)

    # TODO(eriq): Abstract out Pacman and Capture frames, and split the blow methods acordingly.

    # Pacman

    def _getAgentBaseToken(self, x, y, agentIndex, state):
        if (state.getAgentState(agentIndex).isPacman()):
            return token.PACMAN_1
        else:
            return token.GHOST_1 + (agentIndex - 1) * 100

    def _getCapsuleBaseToken(self, x, y, state):
        return token.DEFAULT_FOOD_BASE

    def _getFoodBaseToken(self, x, y, state):
        return token.DEFAULT_FOOD_BASE

    def _getWallBaseToken(self, x, y, state):
        return token.BLUE_WALL_BASE

    # Capture
    """
    def _getAgentBaseToken(self, x, y, agentIndex, state):
        if (state.getAgentState(agentIndex).isPacman()):
            return token.PACMAN_2 + agentIndex * 100
        else:
            return token.GHOST_1 + agentIndex * 100

    def _getCapsuleBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return token.RED_FOOD_BASE
        else:
            return token.BLUE_FOOD_BASE

    def _getFoodBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return token.RED_FOOD_BASE
        else:
            return token.BLUE_FOOD_BASE


    def _getWallBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return token.RED_WALL_BASE
        else:
            return token.BLUE_WALL_BASE
    """
