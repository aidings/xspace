import inspect
import json
import yaml
from loguru import logger
from .config import ConfigDict
from pathlib import Path

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