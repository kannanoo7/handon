class PyframexError(Exception):
    """Base class for all exceptions in Pyframe."""


class RouterNNotFound(PyframexError):
    """Raised when a router is not found."""
    pass

class PluginError(PyframexError):
    """Raised when there is an error with a plugin."""
    pass
