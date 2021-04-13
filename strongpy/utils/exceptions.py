_PARAMETER_TYPE_ERROR_MSG =\
    "{0}() parameter '{1}' is of type '{2}' and should be of type '{3}'."


class ParameterTypeError(Exception):
    """ Signals an ill-typed parameter passed into a strictly type-checking
        function.
    """

    def __init__(self, function, paramname, targettype, giventtype):
        global _PARAMETER_TYPE_ERROR_MSG
        
        message = _PARAMETER_TYPE_ERROR_MSG.format(
            function.__name__,
            paramname,
            giventtype.__name__,
            targettype.__name__,
        )

        super().__init__(message)


_RETURN_TYPE_ERROR_MSG =\
    "Return value of {0}() is of type '{1}' and should be of type '{2}'."


class ReturnTypeError(Exception):
    def __init__(self, function, targettype, giventtype):
        global _RETURN_TYPE_ERROR_MSG

        message = _RETURN_TYPE_ERROR_MSG.format(
            function.__name__,
            giventtype.__name__,
            targettype.__name__,
        )

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
