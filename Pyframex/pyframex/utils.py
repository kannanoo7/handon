import inspect 


def is_awaitable(obj):
    return inspect.isawaitable(obj)
