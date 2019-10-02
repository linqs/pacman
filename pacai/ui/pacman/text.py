from pacai.ui.pacman.view import PacmanAbstractView
from pacai.ui.text import AbstractTextView

class PacmanTextView(PacmanAbstractView, AbstractTextView):
    """
    A text view for pacman.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
