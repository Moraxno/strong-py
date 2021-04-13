# import __main__
import strongpy
from strongpy import strict


@strict()
def __abc(a: int, b: str, c, d: float, aa: str = "hi", ba: 1 = 4):
    pass


__abc(1, "2", 3, 4.0, ba=5, aa="6")


def wrapper(*args, **kwargs):
    if kwargs == {} and len(args) == 1:
        print("No args")
    else:
        print("args")
        print(args, kwargs)
        return lambda x: x



@wrapper()
def f(num):
    return num + 1

