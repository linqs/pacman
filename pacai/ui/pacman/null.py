from pacai.ui.view import AbstractView

class PacmanNullView(AbstractView):
    def __init__(self):
        super().__init__()

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        pass
