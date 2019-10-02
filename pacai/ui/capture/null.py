from pacai.ui.capture.view import CaptureAbstractView
from pacai.ui.null import AbstractNullView

class CaptureNullView(AbstractNullView, CaptureAbstractView):
    """
    A null view for capture.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
