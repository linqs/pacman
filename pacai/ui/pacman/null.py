from pacai.ui.pacman.view import PacmanAbstractView

class PacmanNullView(PacmanAbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        pass
