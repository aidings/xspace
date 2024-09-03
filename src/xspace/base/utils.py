import importlib

def module_from_string(module_string:str, func:str=None, reload=False):
    """ get module from string

    Args:
        module_string (str): just like `path.to.module`
        reload (bool, optional): reload the module. Defaults to False.

    Returns:
        object: module function
    """
    module, cls = module_string.rsplit(".", 1)
    if reload:
        module_imp = importlib.import_module(module)
        importlib.reload(module_imp)
    obj = getattr(importlib.import_module(module, package=None), cls)
    if func:
        obj = getattr(obj, func)
    return obj 
    

def object_from_config(config:dict):
    """ instantiate a class from config

    Args:
        config (dict): {'target': 'path.to.SomeClass', 'params': {'arg1': 'value1'}}

    Raises:
        KeyError: no `target` key in config

    Returns:
        object: a class instance
    """
    if not "target" in config:
        raise KeyError("Expected key `target` to instantiate.")
    module = module_from_string(config["target"], config.get('func', None))
    params = config.get("params", dict())
    kparams = {}
    for key in params:
        if key.startswith("~"):
            kparams[key[1:]] = module_from_string(params[key])
        else:
            kparams[key] = params[key]
    return module(**kparams)
