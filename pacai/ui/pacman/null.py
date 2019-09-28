from pacai.ui.pacman.view import PacmanAbstractView

class PacmanNullView(PacmanAbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _createFrame(self, state):
        # Don't bother creating any frames for gifs if we are not creating gifs.
        if (self._saveFrames):
            return super()._createFrame(state)

        return None

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        pass
