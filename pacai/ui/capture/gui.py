from pacai.ui.capture.view import CaptureAbstractView
from pacai.ui.gui import AbstractGUIView

class CaptureGUIView(CaptureAbstractView, AbstractGUIView):
    """
    A GUI view for capture.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
