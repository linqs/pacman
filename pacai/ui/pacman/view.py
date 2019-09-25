from pacai.ui.view import AbstractView
from pacai.ui.pacman.frame import PacmanFrame

class PacmanAbstractView(AbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _createFrame(self, state):
        return PacmanFrame(self._frameCount, state, self._turnCount)
