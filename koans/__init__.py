"""Shared marker for incomplete predictions."""


class _Blank:
    def __repr__(self):
        return "__ (fill in your prediction)"


__ = _Blank()
