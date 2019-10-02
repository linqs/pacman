from pacai.ui.view import AbstractView
from pacai.ui.pacman.frame import PacmanFrame

class PacmanAbstractView(AbstractView):
    """
    A abstract view for pacman.
    Knows how to create pacman frames.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _createFrame(self, state):
        return PacmanFrame(self._frameCount, state, self._turnCount)
