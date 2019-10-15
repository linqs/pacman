from pacai.ui.null import AbstractNullView
from pacai.ui.pacman.view import PacmanAbstractView

class PacmanNullView(AbstractNullView, PacmanAbstractView):
    """
    A null view for pacman.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
