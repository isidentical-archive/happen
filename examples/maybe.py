import builtins
import random
from happen.happen import keyword_patcher


class Maybe:
    def __bool__(self):
        return random.choice((True, False))

    def __repr__(self):
        return f"Maybe?"

    def __str__(self):
        return repr(self)


Maybe = Maybe()
keyword_patcher(("Maybe",), "__main__")
original_isinstance = isinstance


def check(a, b):
    if a is Maybe and b is bool:
        return True
    return original_isinstance(a, b)


builtins.isinstance = check
