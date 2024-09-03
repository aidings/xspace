import os
import json
import torch
from loguru import logger
from pathlib import Path
from typing import List


class StateDict:
    def __init__(self, model:torch.nn.Module, map_key={}, del_key=[], local_rank=-1):
        assert isinstance(model, torch.nn.Module), 'model must be torch.nn.Module'
        self.model = model
        self.map_key = map_key
        self.del_key = del_key
        self.local_rank = local_rank
    
    def __get_val(self, state_dict, get_key:List[str]):
        assert isinstance(get_key, list), 'get_key must be list'
        nkey = len(get_key)
        if nkey == 0:
            return state_dict
        if nkey == 1:
            return state_dict[get_key[0]]
        else:
            return self.__get_val(state_dict[get_key[0]], get_key[1:])

    def load(self, ckpt_path, strict=False, get_key=[]):
        """load state_dict from checkpoint into model

        Args:
            ckpt_path (str, os.PathLike): input checkpoint path
            strict (bool, optional): validation the checkpoint keys all match model keys. Defaults to False.
            get_key (list, optional): ckpt_path model key's location. Defaults to [].
        """
        if isinstance(ckpt_path, dict):
            ckpt = ckpt_path
            for key in ckpt.keys():
                ckpt[key] = ckpt[key].to('cpu')
        elif isinstance(ckpt_path, (str, os.PathLike)) and Path(ckpt_path).suffix == '.safetensors':
            ckpt = self._safe2ckpt(ckpt_path)
        else:
            ckpt = torch.load(ckpt_path, map_location='cpu')

        if 'state_dict' in ckpt:
            ckpt = ckpt['state_dict']

        ckpt = self.__get_val(ckpt, get_key)

        # 映射key
        ckpt = self.__map_key(ckpt)
        # 移除多GPU模式的权重
        ckpt = self.__remove_module(ckpt)

        _, match = self.diff(ckpt)

        self.model.load_state_dict(match, strict=strict)

        return ckpt

    def diff(self, ckpt):
        info = {"match": 0, "size_not_same": {}, "name_not_same": [], "both_not_same": []}
        match = {}
        state_dict = self.model.state_dict()
        for key in state_dict.keys():
            flag = False
            for del_key in self.del_key:
                flag = del_key in key
                if flag:
                   break
            if flag:
                continue
            if key in ckpt.keys():
                # name same
                if state_dict[key].size() == ckpt[key].size():
                    # weight same
                    info['match'] += 1
                    match[key] = ckpt[key]
                else:
                    info['size_not_same'][key] = (list(state_dict[key].size()), list(ckpt[key].size()))
                    info['both_not_same'].append(key)
            else:
                info['name_not_same'].append(key)
                info['both_not_same'].append(key)
        
        dict_info = json.dumps({'match': info['match'],
                                'name_not_same': len(info['name_not_same']),
                                'size_not_same': len(info['size_not_same']),
                                'both_not_same': len(info['both_not_same'])},
                                ensure_ascii=True)
        if self.local_rank in [-1, 0]:
            if len(info['both_not_same']):
                logger.warning(f"[{self.model.__class__.__name__}] The following keys are not same in state_dict and ckpt: {info['both_not_same']}")
            else:
                logger.info(f"[{self.model.__class__.__name__}] All keys are same in state_dict and ckpt.")
            logger.debug(f"[{self.model.__class__.__name__}] {dict_info}")
        return info, match

    def __map_key(self, ckpt):
        if len(self.map_key) == 0:
            return ckpt

        kdict = {}
        for key in self.map_key.keys():
            if key in ckpt.keys():
                dst_key = self.map_key[key]
                kdict[dst_key] = ckpt[key]
            else:
                kdict[key] = ckpt[key]
        return kdict

    def __remove_module(self, ckpt):
        kdict = {}
        for key in ckpt.keys():
            if key.startswith('module.'):
                mkey = key[7:]
                kdict[mkey] = ckpt[key]
            else:
                kdict[key] = ckpt[key]
        return kdict

    @staticmethod
    def _safe2ckpt(safe_path):
        from safetensors import safe_open
        ckpt = {}
        with safe_open(safe_path, framework='pt', device='cpu') as f:
            for key in f.keys():
                ckpt[key] = f.get_tensor(key)
        return ckpt
