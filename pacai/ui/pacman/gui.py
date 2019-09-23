import tkinter

from PIL import ImageTk

from pacai.ui.keyboard import Keyboard
from pacai.ui.view import AbstractView
from pacai.ui.view import Frame

class PacmanGUIView(AbstractView):
    def __init__(self):
        super().__init__()

        self._root = tkinter.Tk()
        self._canvas = None

        self._height = None
        self._width = None

    def getKeyboard(self):
        return Keyboard(self._root)

    # Override
    def initialize(self, state):
        self._height = state.getInitialLayout().getHeight() * Frame.SQUARE_SIZE
        self._width = state.getInitialLayout().getWidth() * Frame.SQUARE_SIZE

        self._canvas = tkinter.Canvas(self._root, height = self._height, width = self._width)
        self._canvas.pack()

        # TODO(eriq): This will move to the top once the main graphcs loop is fixed.
        super().initialize(state)

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        image = ImageTk.PhotoImage(frame.toImage(self._sprites))
        self._canvas.create_image(0, 0, image = image, anchor = tkinter.NW)

        self._root.update_idletasks()
        self._root.update()
