import inspect
import json
import yaml
from loguru import logger
from .config import ConfigDict

from pathlib import Path
from copy import deepcopy as dcopy

class XKwargs(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.copy = dcopy(kwargs) 
    
    def get(self, key, default=None):
        if key in self:
            return self.copy.pop(key)
        return default

    def left(self):
        return self.copy
    
    def reset(self):
        self.copy.update(self.__dict__)

def get_class_defaults(conf_path=None, cls=None):
    # 创建参数字典
    args_dict = {}

    if cls:
        constructor = cls.__init__

        # 获取构造函数的默认参数
        parameters = list(inspect.signature(constructor).parameters.values())[1:]  # 从第二个参数开始，第一个为self

        for param in parameters:
            if param.default is not param.empty:
                args_dict[param.name] = param.default
    
    if conf_path is not None:
        if isinstance(conf_path, str):
            path = Path(conf_path) 
            if path.suffix == '.yaml':
                with open(conf_path, 'r') as f:
                    conf = yaml.load(f, Loader=yaml.FullLoader)
            elif path.suffix == '.json':
                with open(conf_path, 'r') as f:
                    conf = json.load(f)
            else:
                raise ValueError(f"Unsupported config file type: {path.suffix}")
        elif isinstance(conf_path, (dict, ConfigDict)):
            conf = conf_path
            keys = []
            if len(args_dict) > 0:
                for key in conf_path.keys():
                    if key not in args_dict:
                        keys.append(key)
                if len(keys) > 0:
                    logger.warning(f"Config file contains unexpected keys: {keys} not in {list(args_dict.keys())}")
        else:
            raise TypeError(f"Unsupported config type: {type(conf_path)}")

    if cls:
        for key, value in conf.items():
            if key in args_dict:
                args_dict[key] = value
    else:
        args_dict = conf
    
    return args_dict


class Input2Wargs:
    def __init__(self, func):
        sigature = inspect.signature(func)
        self.defaults = {}
        self.okeys = []
        if inspect.isfunction(func):
            for k, v in sigature.parameters.items():
                self.defaults[k] = v.default
                self.okeys.append(k)
        elif inspect.ismethod(func):
            for k, v in sigature.parameters.items():
                if k == "self":
                    continue
                self.defaults[k] = v.default
                self.okeys.append(k)
        else:
            raise TypeError(f"Unsupported function type: {type(func)}")
        self.skeys = set(self.okeys)
    
    def __call__(self, *args, **kwargs):
        params = {}
        params.update(kwargs)
        n = len(args)
        for k, v in zip(self.okeys[:n], args):
            params[k] = v
        
        return params
    
    def __getitem__(self, key):
        return self.defaults[key]
    
    def __setitem__(self, key, value):
        raise ValueError("Cannot set default value")
    
    def match(self, **kwargs):
        mdict = {}
        iskeys = self.skeys & set(kwargs.keys())
        mdict.update({k: kwargs[k] for k in iskeys})
        return mdict