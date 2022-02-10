import math
import sys
import time
import tkinter

from PIL import Image
from PIL import ImageTk

from pacai.ui.keyboard import Keyboard
from pacai.ui import spritesheet
from pacai.ui.view import AbstractView

MAX_FPS = 1000
TK_BASE_NAME = 'pacai'
DEATH_SLEEP_TIME = 0.5

MIN_WINDOW_HEIGHT = 100
MIN_WINDOW_WIDTH = 100

class AbstractGUIView(AbstractView):
    """
    Most of the functionality necessary to draw graphics in a window.
    `tkinter` is used, so Tk must be installed on the machine.
    """

    def __init__(self, fps = 0, title = 'pacai', **kwargs):
        super().__init__(**kwargs)

        self._fps = int(max(0, min(MAX_FPS, fps)))

        # To make computations easier, we will actually convert "unlimited FPS" to our FPS max.
        if (self._fps == 0):
            self._fps = MAX_FPS

        self._timePerFrame = 1.0 / self._fps

        self._totalDrawRequests = None
        self._totalDroppedFrames = None

        self._firstDrawTime = None
        self._lastDrawTime = None

        if (title != 'pacai'):
            title = 'pacai - %s' % (str(title))

        self._root = tkinter.Tk(baseName = TK_BASE_NAME)
        self._root.protocol('WM_DELETE_WINDOW', self._windowClosed)
        self._root.minsize(width = MIN_WINDOW_WIDTH, height = MIN_WINDOW_HEIGHT)
        self._root.resizable(True, True)
        self._root.title(title)

        self._root.bind("<Configure>", self._resize)

        self._canvas = None
        self._imageArea = None

        self._height = None
        self._width = None

        self._dead = False
        self._keyboard = None

    # Override
    def finish(self):
        super().finish()

        self._canvas.delete("all")

    def getKeyboard(self):
        # tkinter is not good with multiple keybinds.
        if (self._keyboard is None):
            self._keyboard = Keyboard(self._root)

        return self._keyboard

    # Override
    def initialize(self, state):
        super().initialize(state)

        # Height is +1 for the score.
        self._height = max(
            MIN_WINDOW_HEIGHT,
            (state.getInitialLayout().getHeight() + 1) * spritesheet.SQUARE_SIZE)
        self._width = max(
            MIN_WINDOW_WIDTH,
            state.getInitialLayout().getWidth() * spritesheet.SQUARE_SIZE)

        if (self._canvas is None):
            self._canvas = tkinter.Canvas(self._root, height = self._height, width = self._width,
                    highlightthickness = 0)

        self._imageArea = self._canvas.create_image(0, 0, image = None, anchor = tkinter.NW)
        self._canvas.pack(fill = 'both', expand = True)

        self._totalDrawRequests = 0
        self._totalDroppedFrames = 0
        self._firstDrawTime = None

    def _cleanup(self, exit = True):
        """
        This GUI has been killed, clean up.
        This is one of the rare cases where we will exit outside of the bin package.
        """

        # Sleep for a short period, so the last state of the game can be seen.
        time.sleep(DEATH_SLEEP_TIME)

        if (self._root is not None):
            self._root.destroy()
            self._root = None

        if (exit):
            sys.exit(0)

    def _adjustFPS(self):
        """
        Decide if we need to take some action to adjust the FPS.
        If we are drawing too slow, we will drop a frame.
        If we are drawing too fast, we will block and timeout.
        In the case of a dropped frame, this will return true.
        """

        now = time.time()

        if (math.isclose(0.0, now - self._firstDrawTime)):
            return True

        # The FPS after accounting for dropped frames.
        adjustedFPS = self._totalDrawRequests / (now - self._firstDrawTime)

        # To keep the FPS up, we may skip animating frames.
        if (adjustedFPS < self._fps):
            self._totalDroppedFrames += 1
            return True

        if (self._lastDrawTime is not None):
            timeLeft = self._timePerFrame - (now - self._lastDrawTime)
            if (timeLeft > 0):
                # Use Tkinter to block.
                self._root.after(int(1000 * timeLeft))

        return False

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        if (self._dead):
            self._cleanup()

        self._totalDrawRequests += 1

        if (self._firstDrawTime is None):
            self._firstDrawTime = time.time()

            # This is our first frame, we do not have an FPS to stabilize yet.
            forceDraw = True

        if (not forceDraw and self._adjustFPS()):
            return

        image = frame.toImage(self._sprites, self._font)

        # Check for a resize.
        if (self._height != frame.getImageHeight() or self._width != frame.getImageWidth()):
            image = image.resize((self._width, self._height), resample = Image.LANCZOS)

        # Convert the image into a tk image.
        image = ImageTk.PhotoImage(image)
        self._canvas.itemconfig(self._imageArea, image = image)

        self._root.update_idletasks()
        self._root.update()

        self._lastDrawTime = time.time()

    def _resize(self, event):
        if (self._width == event.width and self._height == event.height):
            return

        # Ignore resize requests that are for a single pixel.
        # (These requests are sometimes generated from OSX.)
        if (event.width == 1 and event.height == 1):
            return

        self._width = max(MIN_WINDOW_WIDTH, event.width)
        self._height = max(MIN_WINDOW_HEIGHT, event.height)

        self._canvas.config(width = self._width, height = self._height)
        self._canvas.pack(fill = 'both', expand = True)

    def _windowClosed(self, event = None):
        """
        Handler for the TK window closing.
        """

        self._dead = True
