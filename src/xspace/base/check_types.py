import inspect

def check_function_input_types(func, nparam, type_args=[]):
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