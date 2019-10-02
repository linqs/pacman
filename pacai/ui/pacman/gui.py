from pacai.ui.gui import AbstractGUIView
from pacai.ui.pacman.view import PacmanAbstractView

class PacmanGUIView(PacmanAbstractView, AbstractGUIView):
    """
    A GUI view for pacman.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
