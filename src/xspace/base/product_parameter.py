import itertools
from typing import List


class ProductParameter:
    def __init__(self, param_dict: dict = {}):
        self.param_dict = param_dict
        self.product = []
    
    def __len__(self):
        return len(self.product)
    
    def __setitem__(self, key:str, value: List):
        self.param_dict[key] = value
    
    def __getitem__(self, index: int):
        return self.product[index]

    def run(self):
        for key in self.param_dict.keys():
            assert isinstance(self.param_dict[key], list), f"{key} is not a list"
        
        def _maps(vals):
            return dict(zip(self.param_dict.keys(), vals))
        
        klist = []
        for key in self.param_dict.keys():
            klist.append(self.param_dict[key])

        caresian_preod = list(itertools.product(*klist))
        # print(caresian_preod)
        self.product = list(map(_maps, caresian_preod))