class ParameterTypeError(Exception):
    """ Signals an ill-typed parameter passed into a strictly type-checking
        function.
    """

    TEMPLATE_MESSAGE = \
        "{0} parameter '{1}' is of type '{2}' and should be of type '{3}'."

    def __init__(self, function, paramname, targettype, giventtype):
        message = self.TEMPLATE_MESSAGE.format(
            function.__name__,
            paramname,
            giventtype.__name__,
            targettype.__name__,
        )

        super().__init__(message)


class ReturnTypeError(Exception):
    TEMPLATE_MESSAGE = \
        "Return value of {0} is of type '{1}' and should be of type '{2}'."

    def __init__(self, function, targettype, giventype):

        message = self.TEMPLATE_MESSAGE.format(
            function.__name__,
            giventype.__name__,
            targettype.__name__,
        )

        super().__init__(message)


class ParameterTypehintMissingError(Exception):
    TEMPLATE_MESSAGE = "Parameter {1} of {0} has no type hint."

    def __init__(self, function, param):
        message = self.TEMPLATE_MESSAGE.format(function.__name__, param)
        super().__init__(message)


_NON_KWARG_IN_DECORATOR_MSG =\
    "StrongPy decorators do not accept keywordless arguments. The following \
    arguments were passed without a keyword: {0}."


class NonKwargInDecoratorError(Exception):
    def __init__(self, args):
        global _NON_KWARG_IN_DECORATOR_MSG

        message = _NON_KWARG_IN_DECORATOR_MSG.format(
            args
        )

        super().__init__(message)
