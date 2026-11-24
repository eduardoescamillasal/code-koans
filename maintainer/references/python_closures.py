from functools import wraps

prediction = (7, 7, 7)
contrast = (7, 7)


def _cache_key(args: tuple[object, ...], kwargs: dict[str, object]) -> tuple[object, ...]:
    return args, tuple(sorted(kwargs.items()))


def memoize(function):
    cache = {}

    @wraps(function)
    def wrapper(*args, **kwargs):
        key = _cache_key(args, kwargs)
        if key not in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]

    return wrapper


def routes(n, m, blocked):
    @memoize
    def visit(x, y):
        if x > n or y > m or (x, y) in blocked:
            return 0
        if (x, y) == (n, m):
            return 1
        return visit(x + 1, y) + visit(x, y + 1)

    return visit(0, 0)
