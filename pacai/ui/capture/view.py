from pacai.ui.view import AbstractView
from pacai.ui.capture.frame import CaptureFrame

class CaptureAbstractView(AbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _createFrame(self, state):
        return CaptureFrame(self._frameCount, state, self._turnCount)
