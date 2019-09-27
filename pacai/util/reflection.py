import importlib

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

def getAllDescendents(classObject):
    descendents = set()

    for childClass in classObject.__subclasses__():
        descendents.add(childClass)
        descendents |= getAllDescendents(childClass)

    return descendents
