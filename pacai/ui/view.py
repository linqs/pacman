import abc
import os

from PIL import Image
from PIL import ImageDraw

from pacai.core.directions import Directions
from pacai.util import util

DEFAULT_GIF_FPS = 10
MIN_GIF_FPS = 1
DEFAULT_SKIP_FRAMES = 4

# By default, the sprite sheet is adjacent to this file.
DEFAULT_SPRITES = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pacman-sprites.png')

class AbstractView(abc.ABC):
    """
    A abstarct view that represents all the necessary functionality a specific
    view should implement.
    The ability to produce a gif is inherent to all views,
    even if they do not produce graphics at runtime.
    """

    def __init__(self, spritesPath = DEFAULT_SPRITES,
            gifPath = None, gifFPS = DEFAULT_GIF_FPS, skipFrames = DEFAULT_SKIP_FRAMES):
        self._spritesPath = spritesPath

        self._gifPath = gifPath
        self._gifFPS = max(MIN_GIF_FPS, int(gifFPS))

        self._saveFrames = (self._gifPath is not None)
        self._skipFrames = max(1, int(skipFrames))
        self._keyFrames = []

        # The number of frames this view has produced.
        self._frameCount = 0
        # The number of turns this view has produced.
        # (Tracked by the number of times agent 0 has been animated.)
        self._turnCount = 0

        self._sprites = Frame.loadSpriteSheet(spritesPath)

    def finish(self):
        """
        Signal that the game is over and the UI should cleanup.
        """

        # Save the gif.
        if (self._saveFrames and len(self._keyFrames) > 0):
            gifTimePerFrameMS = int(1.0 / self._gifFPS * 1000.0)

            images = [frame.toImage(self._sprites) for frame in self._keyFrames]
            images[0].save(self._gifPath, save_all = True, append_images = images,
                    duration = gifTimePerFrameMS, loop = 0, optimize = True)

    def getKeyboard(self):
        """
        For views that support keyboards, get an instance of a pacai.ui.keyboard.Keyboard.
        """

        raise NotImplementedError("This view does not support keyboards.")

    def initialize(self, state):
        """
        Perform an initial drawing of the view.
        """

        pass

    def update(self, state, forceDraw = False):
        """
        Materialize the view, given a state.
        """

        if (state.isOver()):
            forceDraw = True

        frame = Frame(self._frameCount, state, self._turnCount)
        if (state.isOver()
                or (self._saveFrames and self._frameCount % self._skipFrames == 0)):
            self._keyFrames.append(frame)

        self._drawFrame(state, frame, forceDraw = forceDraw)

        self._frameCount += 1
        if (state.getLastAgentMoved() == 0):
            self._turnCount += 1

    @abc.abstractmethod
    def _drawFrame(self, state, frame, forceDraw = False):
        """
        The real work for each view implementation.
        From a frame, output to whatever medium this view utilizes.
        """

        pass

    def pause(self):
        # TODO(eriq): Deprecated. From old interface.
        pass

    def draw(self, state):
        # TODO(eriq): Deprecated. From old interface.
        pass

# Note: Having this outside of Frame is a bit hacky,
# but we need to do it to clear up some static cyclic dependencies.
def _computeWallCode(hasWallN, hasWallE, hasWallS, hasWallW):
    """
    Given information about a wall's cardinal neighbors,
    compute the correct type of wall to use.
    The computation is similar to POSIX permission bits,
    all combinations produce unique sums.
    """

    WALL_BASE = 100

    N_WALL = 1
    E_WALL = 2
    S_WALL = 4
    W_WALL = 8

    code = WALL_BASE

    if (hasWallN):
        code += N_WALL

    if (hasWallE):
        code += E_WALL

    if (hasWallS):
        code += S_WALL

    if (hasWallW):
        code += W_WALL

    return code

# TODO(eriq): Frames can probably be more effiicent with bit packing.
class Frame(object):
    """
    A general representation of that can be seen on-screen at a given time.
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

    # For the walls, we have a different sprite depending on what sides (lines) are present.
    # An 'X' in the name indicates that a wall is not there.
    # To get the pacman "tubular" look, adjacent walls will look connected
    # and not have a line between them.
    # Walls start at 100.
    WALL_NESW = _computeWallCode(False, False, False, False)
    WALL_NESX = _computeWallCode(False, False, False, True)
    WALL_NEXW = _computeWallCode(False, False, True, False)
    WALL_NEXX = _computeWallCode(False, False, True, True)
    WALL_NXSW = _computeWallCode(False, True, False, False)
    WALL_NXSX = _computeWallCode(False, True, False, True)
    WALL_NXXW = _computeWallCode(False, True, True, False)
    WALL_NXXX = _computeWallCode(False, True, True, True)
    WALL_XESW = _computeWallCode(True, False, False, False)
    WALL_XESX = _computeWallCode(True, False, False, True)
    WALL_XEXW = _computeWallCode(True, False, True, False)
    WALL_XEXX = _computeWallCode(True, False, True, True)
    WALL_XXSW = _computeWallCode(True, True, False, False)
    WALL_XXSX = _computeWallCode(True, True, False, True)
    WALL_XXXW = _computeWallCode(True, True, True, False)
    WALL_XXXX = _computeWallCode(True, True, True, True)

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
    PACMAN_END = 1700

    GHOST_1 = 2100
    GHOST_2 = 2200
    GHOST_3 = 2300
    GHOST_4 = 2400
    GHOST_5 = 2500
    GHOST_6 = 2600
    GHOST_END = 2700

    # Constants specific to the sprite sheet.

    SPRITE_SHEET_WALLS_ROW = 8

    # The order that the wall sprites appear in the sheet.
    SPRITE_SHEET_WALL_ORDER = [
        WALL_NESW,
        WALL_NESX,
        WALL_NEXW,
        WALL_NEXX,
        WALL_NXSW,
        WALL_NXSX,
        WALL_NXXW,
        WALL_NXXX,
        WALL_XESW,
        WALL_XESX,
        WALL_XEXW,
        WALL_XEXX,
        WALL_XXSW,
        WALL_XXSX,
        WALL_XXXW,
        WALL_XXXX,
    ]

    SPRITE_SHEET_AGENT_ORDER = [
        PACMAN_1,
        GHOST_1,
        GHOST_2,
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
    def isGhost(token):
        return token >= Frame.GHOST_1 and token <= Frame.GHOST_END

    @staticmethod
    def isPacman(token):
        return token >= Frame.PACMAN_1 and token <= Frame.PACMAN_END

    @staticmethod
    def isWall(token):
        return token >= Frame.WALL_NESW and token <= Frame.WALL_XXXX

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

    @staticmethod
    def _getAnimationOffset(direction, frame):
        """
        Get the token for a specific animation frame.
        """

        if (direction == Frame.STOP):
            return 0
        return 1 + (direction - 1) * Frame.ANIMATION_CYCLE + (frame % Frame.ANIMATION_CYCLE)

    @staticmethod
    def loadSpriteSheet(path):
        spritesheet = Image.open(path)

        sprites = {
            Frame.PACMAN_1: Frame._cropSprite(spritesheet, 0, 0),
            Frame.GHOST_1: Frame._cropSprite(spritesheet, 1, 0),
            Frame.GHOST_2: Frame._cropSprite(spritesheet, 2, 0),

            Frame.FOOD: Frame._cropSprite(spritesheet, 7, 0),
            Frame.CAPSULE: Frame._cropSprite(spritesheet, 7, 1),
            Frame.SCARED_GHOST: Frame._cropSprite(spritesheet, 7, 2),
        }

        # Load all the wall sprites.
        for wallIndex in range(len(Frame.SPRITE_SHEET_WALL_ORDER)):
            wallToken = Frame.SPRITE_SHEET_WALL_ORDER[wallIndex]
            sprite = Frame._cropSprite(spritesheet, Frame.SPRITE_SHEET_WALLS_ROW, wallIndex)
            sprites[wallToken] = sprite

        # Load all the agent animations.
        for agentIndex in range(len(Frame.SPRITE_SHEET_AGENT_ORDER)):
            baseToken = Frame.SPRITE_SHEET_AGENT_ORDER[agentIndex]

            for direction in Frame.DIRECTIONS:
                for frame in range(Frame.ANIMATION_CYCLE):
                    animationOffset = Frame._getAnimationOffset(direction, frame)
                    token = baseToken + animationOffset
                    sprites[token] = Frame._cropSprite(spritesheet, agentIndex, animationOffset)

        return sprites

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

    def _buildBoard(self, state):
        board = self._width * [None]
        for x in range(self._width):

            items = self._height * [Frame.EMPTY]
            for y in range(self._height):
                if (state.hasWall(x, y)):
                    items[y] = self._getWallToken(x, y, state)
                elif (state.hasFood(x, y)):
                    items[y] = Frame.FOOD
                elif (state.hasCapsule(x, y)):
                    items[y] = Frame.CAPSULE

            board[x] = items

        return board

    def _getWallToken(self, x, y, state):
        hasWallN = False
        hasWallE = False
        hasWallS = False
        hasWallW = False

        if (y != self._height - 1):
            hasWallN = state.hasWall(x, y + 1)

        if (x != self._width - 1):
            hasWallE = state.hasWall(x + 1, y)

        if (y != 0):
            hasWallS = state.hasWall(x, y - 1)

        if (x != 0):
            hasWallW = state.hasWall(x - 1, y)

        return _computeWallCode(hasWallN, hasWallE, hasWallS, hasWallW)

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
                token = None

                if (agentState.isPacman()):
                    token = Frame.PACMAN_1
                else:
                    token = Frame.GHOST_1 + (agentIndex - 1) * 100

                direction = Frame._translateDirection(agentState.getDirection())

                # token += Frame._getAnimationOffset(direction, self._turn)
                token += Frame._getAnimationOffset(direction, self._frame)

                tokens[position] = token

        return tokens

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
        if (self.isWall(token)):
            return (0, 51, 255)
        if (token == Frame.FOOD):
            return (255, 255, 255)
        elif (token == Frame.CAPSULE):
            return (255, 0, 255)
        elif (self.isGhost(token)):
            return (229, 0, 0)
        elif (self.isPacman(token)):
            return (255, 255, 61)
        elif (token == Frame.SCARED_GHOST):
            return (0, 255, 0)
        else:
            return (0, 0, 0)
