from pacai.ui.view import AbstractView

class AbstractNullView(AbstractView):
    """
    A view that does not output anything.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _createFrame(self, state):
        # Only create frames if we are creating a gif and this is not a skip frame.
        if (self._saveFrames and (self._frameCount % self._skipFrames == 0)):
            return super()._createFrame(state)

        return None

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        pass
