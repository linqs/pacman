from pacai.ui.null import AbstractNullView
from pacai.ui.pacman.view import PacmanAbstractView

class PacmanNullView(AbstractNullView, PacmanAbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
