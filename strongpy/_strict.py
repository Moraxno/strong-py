from inspect import getfullargspec
from functools import wraps

from .utils.helper import generate_typehints, args_dict, has_proper_type, \
    is_clean_decorator
from .utils.exceptions import ParameterTypeError, ReturnTypeError
from .utils.types import UnspecifiedType


def strict(*args, **kwargs):
    """ Decorates a function to be strictly type checked.
    """
    if is_clean_decorator(args, kwargs):
        # Only function was passed -> extract it from args.
        func = args[0]
        # StrictDecorator is constructed without params, because the default
        # options should be used. Afterwards call it with func to get a patched
        # function back and return it for further use.
        return StrictDecorator()(func)
    else:
        # The function was not passed, but arguments for options instead.
        # Implement option gathering here.
        options = StrictOptions()
        
        # Afterwards return the Decorator directly. In the next step it will be
        # called with the function, so we do not do this here. (Also we could
        # not if we wanted, as the function was never passed onto us.)
        return StrictDecorator(options)


class StrictOptions:
    def __init__(self, force_typehints=False):
        self.force_typehints = False


class StrictDecorator:
    def __init__(self, options=StrictOptions()):
        self.options = options

    def __call__(self, func):
        type_hints = generate_typehints(func)

        # Wrapping function for func.
        @wraps(func)
        def strict_func(*args, **kwargs):
            ad = args_dict(getfullargspec(func).args, args, kwargs)

            # Iterate trough the arguments and compare to type hints. 
            for key, value in ad.items():
                if type_hints[key] == UnspecifiedType:
                    continue
                elif not has_proper_type(value, type_hints[key]):
                    raise ParameterTypeError(func, key, type_hints[key], type(value))

            # If the arguments were correct, execute the function and catch the
            # return value for further inspection.
            result = func(*args, **kwargs)

            return_is_hinted = (type_hints["return"] != UnspecifiedType)
            return_has_wrong_type = not has_proper_type(result, type_hints["return"])

            # If the return value was type hinted and the type does not match, 
            # raise an exception ...
            if return_is_hinted and return_has_wrong_type:
                raise ReturnTypeError(func, type_hints["return"], type(result))

            # ... otherwise the function executed properly under strict conditions
            # and the result is returned.
            return result

        return strict_func
