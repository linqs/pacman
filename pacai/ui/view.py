import abc
import os

from PIL import ImageFont

from pacai.ui import spritesheet

DEFAULT_GIF_FPS = 10
MIN_GIF_FPS = 1
DEFAULT_SKIP_FRAMES = 4

# By default, the sprite sheet is adjacent to this file.
DEFAULT_SPRITES = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pacman-sprites.png')

THIS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
FONT_PATH = os.path.join(THIS_DIR, 'fonts', 'roboto', 'RobotoMono-Regular.ttf')

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

        self._sprites = spritesheet.loadSpriteSheet(spritesPath)
        self._font = ImageFont.truetype(FONT_PATH, spritesheet.SQUARE_SIZE - 14)

    def finish(self):
        """
        Signal that the game is over and the UI should cleanup.
        """

        # Save the gif.
        if (self._saveFrames and len(self._keyFrames) > 0):
            gifTimePerFrameMS = int(1.0 / self._gifFPS * 1000.0)

            images = [frame.toImage(self._sprites, self._font) for frame in self._keyFrames]
            images[0].save(self._gifPath, save_all = True, append_images = images,
                    duration = gifTimePerFrameMS, loop = 0, optimize = False)

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

        frame = self._createFrame(state)
        if (frame is not None and self._saveFrames
                and (state.isOver() or (self._frameCount % self._skipFrames == 0))):
            self._keyFrames.append(frame)

        self._drawFrame(state, frame, forceDraw = forceDraw)

        self._frameCount += 1
        if (state.getLastAgentMoved() == 0):
            self._turnCount += 1

    @abc.abstractmethod
    def _createFrame(self, state):
        """
        Create the frame using the given state.
        Children can decide on the correct concrete representation of a frame.
        """

        pass

    @abc.abstractmethod
    def _drawFrame(self, state, frame, forceDraw = False):
        """
        The real work for each view implementation.
        From a frame, output to whatever medium this view utilizes.
        """

        pass
