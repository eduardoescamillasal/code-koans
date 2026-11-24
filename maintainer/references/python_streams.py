from collections import deque

prediction = ((10, 20), (30,))
contrast = ((10, 20), (10, 20, 30))


def windows(iterable, width):
    if width < 1:
        raise ValueError("width must be positive")
    recent = deque(maxlen=width)
    for item in iterable:
        recent.append(item)
        if len(recent) == width:
            yield tuple(recent)


def first_rises(readings, limit):
    from itertools import islice

    rises = (index for index, (left, right) in enumerate(windows(readings, 2)) if right > left)
    return list(islice(rises, limit))
