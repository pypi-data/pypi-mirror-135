"""Thanks to Alan Cristhian for this code, I couldn't
install statically correctly cuz pip was s--ting itself
but I copied your code here with minor modifications. Thanks."""

import inspect
import sys
import warnings

try:
    import cython
    
except (ModuleNotFoundError, ImportError):
    pass

from .exception import *
from .objtype import suppress

# async generators only present in Python 3.6+
has_async_gen_fun = (3, 6) <= sys.version_info[:2]


def _can_cython_inline():
    """Checks whether we are in a context which makes it possible to compile code inline with Cython.
    Currently it is known that standard REPL and IDLE can't do that.
    """
    import __main__ as main

    # statically works with IPython
    if hasattr(main, 'get_ipython'):
        return True

    # standard REPL doesn't have __file__
    return hasattr(main, '__file__')


def _get_source_code(obj):
    if inspect.isclass(obj):
        lines = inspect.getsourcelines(obj)[0]
        extra_spaces = lines[0].find("class")
        return "".join(l[extra_spaces:] for l in lines)
    elif callable(obj):
        lines = inspect.getsourcelines(obj)[0]
        extra_spaces = lines[0].find("@")
        return "".join(l[extra_spaces:] for l in lines[1:])
    else:
        message = "Function or class expected, got {}.".format(type(obj).__name__)
        raise TypeError(message)


def _get_non_local_scopes(frame):
    while frame:
        yield frame.f_locals
        frame = frame.f_back


def _get_outer_variables(obj):
    frame = inspect.currentframe().f_back
    non_local_scopes = _get_non_local_scopes(frame)
    non_local_variables = list(obj.__code__.co_freevars)
    variables = {}
    for scope in non_local_scopes:
        for name in non_local_variables:
            if name in scope:
                variables[name] = scope[name]
                non_local_variables.remove(name)
        if not non_local_variables:
            break
    return variables


def typed(obj):
    """Compiles a function or class with cython."""
    try:
        with suppress():
            if not _can_cython_inline():
                return obj
            elif has_async_gen_fun and inspect.isasyncgenfunction(obj):
                raise TypeError("Async generator funcions are not supported.")

            source = _get_source_code(obj)
            frame = inspect.currentframe().f_back
            if inspect.isclass(obj):
                locals_ = frame.f_locals
            else:
                locals_ = _get_outer_variables(obj)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                compiled = cython.inline(source, locals=locals_,
                                         globals=frame.f_globals, quiet=True)
                return compiled[obj.__name__]
        
    except NameError:
        raise ModuleError("Cython must be installed to use beetroot.typed. Try `pip install cython` or `pip install beetroot[cython]` or `pip install beetroot[speed]`")

if False:
    warnings.warn(
        "Current code isn't launched from a file so statically.typed isn't able to cythonize stuff."
        "Falling back to normal Python code.",
        RuntimeWarning
    )