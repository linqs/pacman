class Keyboard(object):
    """
    A class for using input from a keyboard.
    TKinter is used to capture user input, so it should be installed when using this.

    The general way this class works is by keeping track of the most recent keys that were pressed.
    Then, a caller can query what keys were pressed.
    A key press can be cleared either with the clear() method or the clearKeys option to query().
    """

    def __init__(self, tkRootWindow):
        self._keys = []

        self._root = tkRootWindow

        # Bind to key-down, key-up, and focus events.
        self._root.bind("<KeyPress>", self._keyPress)
        self._root.bind("<KeyRelease>", self._keyRelease)
        self._root.bind("<FocusIn>", self._clear)
        self._root.bind("<FocusOut>", self._clear)

    def clear(self):
        """
        Clear any pending keys.
        """

        self._keys.clear()

    def query(self, queryKeys = None):
        """
        Check for a set of keys (or all keys if none are specified).
        Keys that are checked for will be cleared after this call.

        Returns: a list of keys that have been pressed (in FIFO order).
        """

        returnKeys = []
        keepKeys = []

        for key in self._keys:
            if (queryKeys is None or key in queryKeys):
                returnKeys.append(key)
            else:
                keepKeys.append(key)

        self._keys = keepKeys
        return returnKeys

    def _clear(self, event):
        self.clear()

    def _keyPress(self, event):
        self._keys.append(event.keysym)

    def _keyRelease(self, event):
        pass
