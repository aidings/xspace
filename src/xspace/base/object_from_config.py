import math
from .utils import object_from_config
from copy import deepcopy as dcp
from tqdm import tqdm
from .color_print import print_table, Table_Theme


class ObjectFromConfig:
    def __init__(self, config, pbar_show=True, **kwargs):
        assert 'objects' in config.keys(), 'config must have key "objects"'
        self.okeys = [f'_{key}_' for key in kwargs.keys()]
        self.config = dcp(config['objects'])
        self.objs = {}
        self.objs.update(kwargs)
        self.__objecters(pbar_show)

        for key, value in self.objs.items():
            self.__setattr__(key, value)
    
    def __is_cited_object(self, key):
        value = self.config
        for key in key.split('.'):
            value = value[key]
        return not isinstance(value, dict)
    
    @staticmethod
    def match_value(value):
        return isinstance(value, str) and value[0] == '_' and value[-1] == '_'
    
    def __proc_cited_objs(self, value):
        ivalue = []
        def _proc_strs(val):
            obj = val
            if self.match_value(val):
                name = val[1:-1]
                if name in self.objs.keys():
                    obj = self.objs[name]
                else:
                    obj = self.__objecter(val)
            return obj
        
        if isinstance(value, (list, tuple)):
            for val in value:
                ival = _proc_strs(val)
                ivalue.append(ival)
        else:
            ivalue = _proc_strs(value)
        
        return ivalue
    
    def __objecter(self, key):
        names = key.split('.')
        conf = self.config
        knames = []
        for name in names[:-1]:
            try:
                conf = conf[name]
            except:
                conf = conf[int(name)]
            
            if self.match_value(name):
                mname = name[1:-1]
                knames.append(mname)
        iname = names[-1][1:-1]
        knames.append(iname)
        is_top = len(names) == 1 and self.match_value(names[0])
        if is_top and iname in self.objs.keys():
            return self.objs[iname]
            
        if self.__is_cited_object(key):
            # is cited object
            obj = self.__proc_cited_objs(conf[names[-1]]) 
            conf.pop(names[-1])
            conf[iname] = obj
        else:
            # knames.append('module')
            conf[iname] = object_from_config(conf.pop(names[-1]))
            if is_top:
                self.objs[names[0][1:-1]] = conf[iname]
        if is_top: 
            return self.objs[iname]

    def __parse(self, kdict, path=''):
        results = []
        
        # Iterate over the current level of the dictionary
        for k, v in kdict.items():
            
            # Construct the full path to this key by appending it to our previous path
            currPath = f'{path}.{k}' if path else k
            
            # Check whether the key contains two consecutive underlines anywhere within its name
            if any([self.match_value(str(i)) for i in [k, currPath]]):
                results.append(currPath)
                        
            # If we are allowed to look inside nested dictionaries, do so
            if isinstance(v, dict):
                results.extend(self.__parse(v, currPath))   
            elif isinstance(v, (list, tuple)):
                for ik, iv in enumerate(v):
                    if isinstance(iv, dict):
                        results.extend(self.__parse(iv, f'{currPath}.{ik}'))
        
        results = [p for p in results if self.match_value(p.split('.')[-1])]
        results = sorted(results, key=lambda x:len(x.split('.'))+1, reverse=True)
        
        return results
    
    def __objecters(self, pbar_show=True):
        keys = self.__parse(self.config)

        sort_dict = dict([(x,self.__sort_keys(x, 0)) for x in keys])
        for key in sort_dict.keys():
            skey = key.split('.')
            if len(skey) > 1:
                clev = sort_dict[skey[0]]
                sort_dict[skey[0]] = max(clev, sort_dict[key] + 1) 
        keys = sorted(keys, key=lambda x: sort_dict[x])
        
        show_keys = set()
        for key in keys:
            ikey = key.split('.')[-1]
            show_keys.add(ikey[1:-1])
        
        show_keys = list(show_keys) 
        if pbar_show:
            ncol = 4
            table = []
            for row_idx in range(int(math.ceil(len(show_keys) / ncol))):
                b = row_idx * ncol
                e = min(b + ncol, len(show_keys))
                table.append(show_keys[b:e])
            if len(table[-1]) != ncol:
                table[-1] += [''] * (ncol - len(table[-1]))
            titles = ['module'] * ncol
            print_table(table, titles, theme=Table_Theme.GREEN)

        pbar = tqdm(total=len(keys), desc='objecting', colour='green', disable=not pbar_show)
        for key in keys: 
            ikey = key[1:-1]
            pbar.set_postfix_str(ikey)
            self.__objecter(key)
            pbar.update()
     
    def __getitem__(self, key):
        return self.objs[key]
    
    def __setitem__(self, key, value):
        raise NotImplementedError('cannot set values')
    
    def __sort_keys(self, key, level):
        if key in self.okeys:
            return 0
        if '.' not in key:
            obj = self.config[key]
            if 'params' not in obj.keys():
                return level
            levels = [level]
            for key in obj['params'].keys():
                if self.match_value(key):
                    # 2: 列表， 1: 字符串
                    value = obj['params'][key]
                    if self.match_value(value):
                        ilevel = self.__sort_keys(value, level+1)
                        levels.append(ilevel)
                    elif isinstance(value, (list, tuple)):
                        for val in value:
                            ilevel = self.__sort_keys(val, level+1)
                            levels.append(ilevel)
                    else:
                        pass
            return max(levels) 

        ikey = key.split('.')
        obj = self.config
        for key in ikey:
            obj = obj[key]
            
        if isinstance(obj, dict):
            return level
        elif self.match_value(obj):
            level = self.__sort_keys(obj, level+1)
        elif isinstance(obj, (list, tuple)):
            levels = [level]
            for val in obj:
                ilevel = self.__sort_keys(val, level+1)
                levels.append(ilevel)
            level = max(levels)
        else:
            pass
        
        return level
