import abc

from PIL import Image
from PIL import ImageDraw

# TODO(eriq): This should eventually be false.
DEFAULT_SAVE_FRAMES = True
DEFAULT_SAVE_EVERY_N_FRAMES = 5

SQUARE_SIZE = 30

GIF_FPS = 10
GIF_FRAME_DURATION_MS = int(1.0 / GIF_FPS * 1000.0)
GIF_FILENAME = 'test.gif'

# TODO(eriq): This is specific for the Pacman-style games.
class AbstractView(abc.ABC):
    """
    A abstarct view that represents all the necessary functionality a specific
    view should implement.
    """

    def __init__(self,
            saveFrames = DEFAULT_SAVE_FRAMES, saveEveryNFrames = DEFAULT_SAVE_EVERY_N_FRAMES):
        self._saveFrames = saveFrames
        self._saveEveryNFrames = saveEveryNFrames
        self._frameCount = 0
        self._keyFrames = []

    def finish(self):
        """
        Signal that the game is over and the UI should cleanup.
        """

        if (self._saveFrames and len(self._keyFrames) > 0):
            images = [frame.toImage() for frame in self._keyFrames]
            images[0].save(GIF_FILENAME, save_all = True, append_images = images,
                    duration = GIF_FRAME_DURATION_MS, loop = 0, optimize = True)

    def initialize(self, state):
        """
        Perform an initial drawing of the view.
        """

        self.update(state, forceDraw = True)

    def update(self, state, forceDraw = False):
        """
        Materialize the view, given a state.
        """

        if (state.isOver()):
            forceDraw = True

        frame = Frame(state)
        if (state.isOver()
                or (self._saveFrames and self._frameCount % self._saveEveryNFrames == 0)):
            self._keyFrames.append(frame)

        self._drawFrame(state, frame, forceDraw = forceDraw)
        self._frameCount += 1

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

# TODO(eriq): Frames can probably be more effiicent with bit packing.
class Frame(object):
    """
    A general representation of that can be seen on-screen at a given time.
    """

    # Token to mark what can occupy different locations.
    EMPTY = 0
    WALL = 1
    FOOD = 2
    CAPSULE = 3
    PACMAN_1 = 10
    PACMAN_2 = 11
    PACMAN_3 = 12
    PACMAN_4 = 13
    PACMAN_5 = 14
    PACMAN_6 = 15
    GHOST_1 = 20
    GHOST_2 = 21
    GHOST_3 = 22
    GHOST_4 = 23
    GHOST_5 = 24
    GHOST_6 = 25
    SCARED_GHOST = 30

    def __init__(self, state):
        self._height = state.getInitialLayout().getHeight()
        self._width = state.getInitialLayout().getWidth()
        self._board = self._buildBoard(state)

    def getHeight(self):
        return self._height

    def getToken(self, x, y):
        return self._board[x][y]

    def getCol(self, x):
        return self._board[x]

    def getWidth(self):
        return self._width

    def _buildBoard(self, state):
        agentTokens = self._getAgentTokens(state)

        board = self._width * [None]
        for x in range(self._width):

            items = self._height * [Frame.EMPTY]
            for y in range(self._height):
                if (state.hasWall(x, y)):
                    items[y] = Frame.WALL

                if (state.hasFood(x, y)):
                    items[y] = Frame.FOOD

                if (state.hasCapsule(x, y)):
                    items[y] = Frame.CAPSULE

                if ((x, y) in agentTokens):
                    items[y] = agentTokens[(x, y)]

            board[x] = items

        return board

    def _getAgentTokens(self, state):
        """
        Returns: {(x, y): token, ...}
        """

        tokens = {}

        for agentIndex in range(state.getNumAgents()):
            agentState = state.getAgentState(agentIndex)
            position = agentState.getNearestPosition()

            if (agentState.isPacman()):
                tokens[position] = Frame.PACMAN_1
            elif (agentState.isScaredGhost()):
                tokens[position] = Frame.SCARED_GHOST
            else:
                tokens[position] = Frame.GHOST_1 + (agentIndex - 1)

        return tokens

    def toImage(self):
        image = Image.new('RGB', (self._width * SQUARE_SIZE, self._height * SQUARE_SIZE))

        draw = ImageDraw.Draw(image)

        for x in range(self._width):
            for y in range(self._height):
                color = self._tokenToColor(self._board[x][y])

                startPoint = self._toImageCoords(x, y)
                endPoint = self._toImageCoords(x + 1, y - 1)
                draw.rectangle([startPoint, endPoint], fill = color)

        return image

    def _toImageCoords(self, x, y):
        # PIL has (0, 0) as the upper-left, while pacai has it as the lower-left.
        return (x * SQUARE_SIZE, (self._height - 1 - y) * SQUARE_SIZE)

    def _tokenToColor(self, token):
        if (token == Frame.EMPTY):
            return (0, 0, 0)
        if (token == Frame.WALL):
            return (0, 51, 255)
        if (token == Frame.FOOD):
            return (255, 255, 255)
        elif (token == Frame.CAPSULE):
            return (255, 0, 255)
        elif (token >= Frame.GHOST_1 and token <= Frame.GHOST_6):
            return (229, 0, 0)
        elif (token >= Frame.PACMAN_1 and token <= Frame.PACMAN_6):
            return (255, 255, 61)
        elif (token == Frame.SCARED_GHOST):
            return (0, 255, 0)
        else:
            return (0, 0, 0)
