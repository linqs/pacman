import importlib

def qualifiedImport(qualifiedName):
    """
    Import a fully qualified name, e.g. 'pacai.util.util.qualifiedImport'.
    """

    if (qualifiedName is None or qualifiedName == '' or qualifiedName == 0):
        raise ValueError("Empty name supplied for import.")

    parts = qualifiedName.split('.')
    module_name = '.'.join(parts[0:-1])
    target_name = parts[-1]

    if (len(parts) == 1):
        raise ValueError("Non-qualified name supplied for import: " + qualifiedName)

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise ValueError("Unable to locate module (%s) for qualified object (%s)." %
                (module_name, qualifiedName))

    if (target_name == ''):
        return module

    return getattr(module, target_name)

def getAllDescendents(classObject):
    """
    Get all the descendent classes of the given class.
    """

    descendents = set()

    for childClass in classObject.__subclasses__():
        descendents.add(childClass)
        descendents |= getAllDescendents(childClass)

    return descendents
