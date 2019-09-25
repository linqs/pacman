import time
import tkinter

from PIL import ImageTk

from pacai.ui.keyboard import Keyboard
from pacai.ui import spritesheet
from pacai.ui.view import AbstractView

MAX_FPS = 1000

class AbstractGUIView(AbstractView):
    def __init__(self, fps = 0, **kwargs):
        super().__init__(**kwargs)

        self._fps = int(max(0, min(MAX_FPS, fps)))

        # To make computations easier, we will actually convert "unlimited FPS" to our FPS max.
        if (self._fps == 0):
            self._fps = MAX_FPS

        self._timePerFrame = 1.0 / self._fps

        self._totalDrawRequests = None
        self._totalDroppedFrames = None

        self._initTime = None
        self._lastDrawTime = None

        self._root = tkinter.Tk()
        self._canvas = None

        self._height = None
        self._width = None

    def getKeyboard(self):
        return Keyboard(self._root)

    # Override
    def initialize(self, state):
        super().initialize(state)

        self._height = state.getInitialLayout().getHeight() * spritesheet.SQUARE_SIZE
        self._width = state.getInitialLayout().getWidth() * spritesheet.SQUARE_SIZE

        self._canvas = tkinter.Canvas(self._root, height = self._height, width = self._width)
        self._canvas.pack()

        self._totalDrawRequests = 0
        self._totalDroppedFrames = 0
        self._initTime = time.time()

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        self._totalDrawRequests += 1

        # Delay drawing the frame to cap the FPS.
        # Every iteration of the loop outputs a frame,
        # so ensure that no single frame is output too quickly.
        if (not forceDraw):
            now = time.time()

            # The FPS after accounting for dropped frames.
            adjustedFPS = self._totalDrawRequests / (now - self._initTime)

            # To keep the FPS up, we may skip animating frames.
            if (adjustedFPS < self._fps):
                self._totalDroppedFrames += 1
                return

            if (self._lastDrawTime is not None):
                timeLeft = self._timePerFrame - (now - self._lastDrawTime)
                if (timeLeft > 0):
                    # Use Tkinter to block.
                    self._root.after(int(1000 * timeLeft))

        image = ImageTk.PhotoImage(frame.toImage(self._sprites))
        self._canvas.create_image(0, 0, image = image, anchor = tkinter.NW)

        self._root.update_idletasks()
        self._root.update()

        self._lastDrawTime = time.time()
