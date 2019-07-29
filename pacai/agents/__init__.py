# We need to specially load all the agents so we can look for them at runtime.

import glob
import os

__all__ = []

for path in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")):
    if (os.path.basename(path) == '__init__.py'):
        continue

    # Just include the basename without the extension.
    __all__.append(os.path.basename(path)[:-3])

# TEST
__all__ = ['agent', 'keyboardAgents', 'ghostAgents']
