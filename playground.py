# import __main__
import strongpy
from strongpy import strict, autocast

@autocast
def repeat(text: str, num: int) -> bool:
    return text * num


def unsafe_repeat(text, num):
    return text * num


print(repeat(12, 4))
print(unsafe_repeat(12, 4))
