import os
import math
from typing import List
# from joblib import Parallel, delayed

class MProcDatas:
    def __init__(self, datas: List, rank_numb: int = 1):
        step = math.ceil(len(datas) / rank_numb)
        rank = os.environ.get('RANK', 0)
        self.datas = datas[step*rank:step*(rank+1)]
    
    def __len__(self):
        return len(self.datas)
    
    def transform(self, index):
        return self.datas[index]
    
    def __getitem__(self, index):
        return self.datas[index] 
    
   