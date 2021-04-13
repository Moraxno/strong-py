from inspect import getfullargspec
from functools import wraps

from .utils.helper import \
    generate_typehints, \
    construct_args_dict, \
    has_proper_type, \
    is_clean_decorator, \
    FunctionSpecifications

from .utils.exceptions import \
    ParameterTypeError, \
    ReturnTypeError, \
    ParameterTypehintMissingError

from .utils.types import UnspecifiedType
from .utils.constants import RETURN_TYPE_NAME

_DEFAULT_STRICT_OPTIONS = {
    "force_parameter_typehints": True
}


def strict(*args, **kwargs):
    """ Decorates a function to be strictly type checked.
    """
    if is_clean_decorator(args, kwargs):
        # Only function was passed -> extract it from args.
        func = args[0]
        # Strict wrapper is constructed with default options.
        return StrictWrappedFunction(func, _DEFAULT_STRICT_OPTIONS)
    else:
        # The function was not passed, but arguments for options instead. Let's
        # gather them as a dict. Then the default options are loaded and
        # updated by the ones given as kwargs.
        options = _DEFAULT_STRICT_OPTIONS.copy()
        options.update(kwargs)
        # Afterwards return a lambda expression that will construct the wrapper
        # as soon as it is called.
        return lambda func: StrictWrappedFunction(func, options)


class StrictWrappedFunction:
    def __init__(self, function, options=_DEFAULT_STRICT_OPTIONS):
        self.function = function
        self.options = options
        self.specs = FunctionSpecifications(function)

        # TODO: execute static checks on the typehints
        self.__verify_param_typehints()
        # self.__verify_param_default_values()
        # self.__verify_return_typehint()
        pass

        self.__rehook_metadata()

    def __call__(self, *args, **kwargs):
        ad = construct_args_dict(self.specs.args, args, kwargs)

        # Iterate trough the arguments and compare to type hints.
        for key, value in ad.items():
            if self.specs.typehints[key] == UnspecifiedType:
                continue
            elif not has_proper_type(value, self.specs.typehints[key]):
                raise ParameterTypeError(
                    self.function, key, self.specs.typehints[key], type(value)
                )

        # If the arguments were correct, execute the function and catch the
        # return value for further inspection.
        result = self.function(*args, **kwargs)
        result_typehint = self.specs.typehints[RETURN_TYPE_NAME]

        return_is_hinted = (result_typehint != UnspecifiedType)
        return_has_wrong_type = \
            not has_proper_type(result, result_typehint)

        # If the return value was type hinted and the type does not match,
        # raise an exception ...
        if return_is_hinted and return_has_wrong_type:
            raise ReturnTypeError(self.function, result_typehint, type(result))

        # ... otherwise the function executed properly under strict
        # conditions and the result is returned.
        return result

    def __verify_param_typehints(self):
        if self.options["force_parameter_typehints"] is True:
            for arg in self.specs.args:
                if self.specs.typehints[arg] == UnspecifiedType:
                    raise ParameterTypehintMissingError(self.function, arg)
        else:
            # Nothing to verify.
            return True

    def __rehook_metadata(self):
        """ Changes metadata of this object to that of the wrapped function, so
            docstring, function_name and associated module are consistent.
        """
        self.__doc__ = self.function.__doc__
        self.__name__ = self.function.__name__
        self.__module__ = self.function.__module__
