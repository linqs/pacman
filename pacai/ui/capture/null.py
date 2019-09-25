from pacai.ui.capture.view import CaptureAbstractView

class CaptureNullView(CaptureAbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        pass
