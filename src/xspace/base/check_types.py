import inspect
from typing import List, Callable

def check_function_input_types(func: Callable, nparam: int, type_args:List=[]):
    """ Checks the input types of a function.

    Args:
        func (Callable): check function's parameter types.
        nparam (int): func's parameter number.
        type_args (list, optional): Expect the type of parameters in func. Defaults to [].

    Raises:
        TypeError: nparam != len(type_args).
        TypeError: type_args[i] != values[i].annotation.
    """
    signature = inspect.signature(func)
    values = list(signature.parameters.values())
    assert len(values) == nparam, f"Expected {nparam} parameters, got {len(values)}"
    types = []
    for i, itype in enumerate(type_args):
        if type_args[i] is None:
            types.append(None)
        else:
            types.append(issubclass(itype, values[i].annotation))
    
    if not all(types):
       raise TypeError(f"Expected type {type_args} for parameters {types}")