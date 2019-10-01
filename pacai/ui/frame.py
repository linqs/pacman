"""
A Frame is the base unit of a View.
Frames hold all the information necessary to draw the game in whatever medium
the view chooses.
"""

import abc

from PIL import Image
from PIL import ImageDraw

from pacai.ui import spritesheet
from pacai.ui import token
from pacai.util import util

# The range of intensity values for highlighted locations.
MAX_HIGHLIGHT_INTENSITY_RANGE = 150

SCORE_X_POSITION = 0.55
SCORE_Y_POSITION = -0.95

class Frame(abc.ABC):
    """
    A general representation of that can be seen on-screen at a given time.
    Frames are the basic units of the views.
    """

    def __init__(self, frame, state, turn):
        self._frame = frame
        self._turn = turn

        self._boardHeight = state.getInitialLayout().getHeight()
        self._boardWidth = state.getInitialLayout().getWidth()

        # All items on the board are at integral potision.
        self._board = self._buildBoard(state)

        # Agents may not be at integral positions, so they are represented independently.
        self._agentTokens = self._getAgentTokens(state)

        # Highlight locations is on the lowest layer.
        self._highlightLocations = state.getHighlightLocations()
        if (self._highlightLocations is None):
            self._highlightLocations = []

        self._score = state.getScore()

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

    def getBoardHeight(self):
        return self._boardHeight

    def getImageHeight(self):
        # +1 for the score.
        return (self._boardHeight + 1) * spritesheet.SQUARE_SIZE

    def getImageWidth(self):
        return self._boardWidth * spritesheet.SQUARE_SIZE

    def getToken(self, x, y):
        return self._board[x][y]

    def getCol(self, x):
        return self._board[x]

    def getBoardWidth(self):
        return self._boardWidth

    def toImage(self, sprites = {}, font = None):
        # Height is +1 for the score.
        size = (
            self._boardWidth * spritesheet.SQUARE_SIZE,
            (self._boardHeight + 1) * spritesheet.SQUARE_SIZE
        )

        image = Image.new('RGB', size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)

        # First, draw any highlights.
        for i in range(len(self._highlightLocations)):
            (x, y) = self._highlightLocations[i]
            startPoint = self._toImageCoords(x, y)
            endPoint = self._toImageCoords(x + 1, y - 1)

            intensity = int((i / len(self._highlightLocations)) * MAX_HIGHLIGHT_INTENSITY_RANGE)

            draw.rectangle([startPoint, endPoint], fill = (255, intensity, intensity))

        # Then, draw the board.
        for x in range(self._boardWidth):
            for y in range(self._boardHeight):
                if (self._board[x][y] != token.EMPTY_TOKEN):
                    self._placeToken(x, y, self._board[x][y], sprites, image, draw)

        # Finally, overlay the agents.
        for ((x, y), agentToken) in self._agentTokens.items():
            self._placeToken(x, y, agentToken, sprites, image, draw)

        # Draw score
        position = self._toImageCoords(SCORE_X_POSITION, SCORE_Y_POSITION)
        scoreText = "Score: %d" % (self._score)
        draw.text(position, scoreText, self._getTextColor(), font)

        return image

    def _buildBoard(self, state):
        board = self._boardWidth * [None]
        for x in range(self._boardWidth):

            items = self._boardHeight * [token.EMPTY_TOKEN]
            for y in range(self._boardHeight):
                if (state.hasWall(x, y)):
                    items[y] = self._getWallToken(x, y, state)
                elif (state.hasFood(x, y)):
                    items[y] = self._getFoodToken(x, y, state)
                elif (state.hasCapsule(x, y)):
                    items[y] = self._getCapsuleToken(x, y, state)

            board[x] = items

        return board

    @abc.abstractmethod
    def _getAgentBaseToken(self, x, y, agentIndex, state):
        pass

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

    @abc.abstractmethod
    def _getCapsuleBaseToken(self, x, y, state):
        pass

    def _getCapsuleToken(self, x, y, state):
        return self._getCapsuleBaseToken(x, y, state) + token.CAPSULE_OFFSET

    @abc.abstractmethod
    def _getFoodBaseToken(self, x, y, state):
        pass

    def _getFoodToken(self, x, y, state):
        return self._getFoodBaseToken(x, y, state) + token.FOOD_OFFSET

    @abc.abstractmethod
    def _getTextColor(self):
        pass

    @abc.abstractmethod
    def _getWallBaseToken(self, x, y, state):
        pass

    def _getWallToken(self, x, y, state):
        hasWallN = False
        hasWallE = False
        hasWallS = False
        hasWallW = False

        baseToken = self._getWallBaseToken(x, y, state)

        if (y != self._boardHeight - 1):
            hasWallN = state.hasWall(x, y + 1)

        if (x != self._boardWidth - 1):
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
            int((self._boardHeight - 1 - y) * spritesheet.SQUARE_SIZE)
        )

    def _tokenToColor(self, objectToken):
        if (objectToken == token.EMPTY_TOKEN):
            return (0, 0, 0)
        elif (objectToken == token.HIGHLIGHT_TOKEN):
            return (255, 0, 0)
        elif (token.isWall(objectToken)):
            return (0, 51, 255)
        elif (token.isFood(objectToken)):
            return (255, 255, 255)
        elif (token.isCapsule(objectToken)):
            return (255, 0, 255)
        elif (token.isGhost(objectToken)):
            return (229, 0, 0)
        elif (token.isPacman(objectToken)):
            return (255, 255, 61)
        elif (objectToken == token.SCARED_GHOST_TOKEN):
            return (0, 255, 0)
        else:
            return (0, 0, 0)
