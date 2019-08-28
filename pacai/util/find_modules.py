import importlib
import sys

# TODO(eriq): I would like this method to be removed.
# There should be better ways than reflexivly searching modules.
def lookup(name):
    """
    Get a method or class from any imported module from its name.
    """

    for module_name in sys.modules:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue

        if (name in dir(module)):
            return getattr(module, name)

    raise Exception('%s not found as a method or class' % name)

def fetchModuleAttribute(name, modules):
    """
    Looks in the given modules for an attribute with the given name.
    Raises an exception if the attribute is not found.
    """

    for module in modules:
        if name in dir(module):
            return getattr(module, name)

    raise AttributeError("Could not locate attribute '%s' in modules: %s." % (name, modules))

def qualifiedImport(qualified_name):
    """
    Import a fully qualified name, e.g. 'pacai.util.util.qualifiedImport'.
    """

    if (qualified_name is None or qualified_name == 0):
        raise AttributeError("Empty supplied for import")

    parts = qualified_name.split('.')
    module_name = '.'.join(parts[0:-1])
    target_name = parts[-1]

    if (len(parts) == 1):
        raise AttributeError("Non-qualified name supplied for import: " + qualified_name)

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise AttributeError("Unable to locate module (%s) for qualified object (%s)." %
                (module_name, qualified_name))

    if (target_name == ''):
        return module

    return getattr(module, target_name)
