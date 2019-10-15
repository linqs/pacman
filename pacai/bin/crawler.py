"""
Binary for the crawler simulation.
"""

import sys

from pacai.ui.crawler.gui import run
from pacai.util.logs import initLogging

def _load_args(args):
    executable = args.pop(0)
    if (len(args) > 1 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s [max steps]" % (executable), file = sys.stderr)
        sys.exit(1)

    max_steps = None
    if (len(args) > 0):
        max_steps = int(args.pop(0))

    return max_steps

def main(argv):
    """
    Entry point for the crawler simulation.
    The args are a blind pass of `sys.argv`.
    """

    initLogging()
    max_steps = _load_args(argv)
    sys.exit(run(max_steps = max_steps))

if __name__ == '__main__':
    main(sys.argv)
