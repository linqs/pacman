import inspect
## code to handle timeouts
import signal

def raiseNotDefined():
    print("Method not implemented: %s" % inspect.stack()[1][3])
    sys.exit(1)

def pause():
    """
    Pauses the output stream awaiting user feedback.
    """

    print("<Press enter/return to continue>")
    input()

# Code to handle timeouts.

class TimeoutFunctionException(Exception):
    """
    Exception to raise on a timeout
    """

    pass

class TimeoutFunction:
    def __init__(self, function, timeout):
        self.timeout = timeout
        self.function = function

    def handle_timeout(self, signum, frame):
        raise TimeoutFunctionException()

    def __call__(self, *args):
        if 'SIGALRM' not in dir(signal):
            return self.function(*args)
        old = signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.timeout)
        try:
            result = self.function(*args)
        finally:
            signal.signal(signal.SIGALRM, old)

        signal.alarm(0)
        return result
