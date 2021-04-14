from strongpy import strict, autocast


class A:
    pass


class B(A):
    pass


@autocast
def repeat(text: str, num: int) -> str:
    return text * num


def unsafe_repeat(text, num):
    return text * num


print(repeat(12, 4))
print(unsafe_repeat(12, 4))
