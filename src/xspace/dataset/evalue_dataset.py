import inspect
from types import MethodType
from typing import List
import csv
import json


class EvalueDataset:
    def __init__(self, lines:List=[], **kwargs):
        self.datas = lines
        self.__transform = lambda idx : self.datas[idx]
        self.kwargs = kwargs
    
    @classmethod 
    def from_csv(cls, file_path, head_type={}, **kwargs):
        lines = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in reader:
                line_dict = dict(zip(header, row))
                for key in header:
                    if key not in line_dict: continue
                    if line_dict[key] == '':
                        line_dict.pop(key)
                    elif key in head_type:
                        line_dict[key] = head_type[key](line_dict[key])
                    else:
                        pass
                lines.append(line_dict)
        return cls(lines, **kwargs)
    
    @classmethod
    def from_list(cls, file_path, **kwargs):
        lines = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        return cls(lines, **kwargs)
    
    @classmethod
    def from_jsonl(cls, file_path, **kwargs):
        lines = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    json_dict = json.loads(line)
                    lines.append(json_dict)
        return cls(lines, **kwargs)
    
    def register_transform(self, trans_function):
        signature = inspect.signature(trans_function)
        values = list(signature.parameters.values())
        assert len(values) == 2, f"The transform function should have two parameters, but got {len(values)}"
        assert issubclass(values[0].annotation, EvalueDataset) and values[1].annotation == int, \
            f"The first parameter should be {EvalueDataset}, but got {values[0].annotation}\n \
              and the second parameter should be {int}, but got {values[1].annotation}"
        
        self.__transform = MethodType(trans_function, self) 
        
        return self 
    
    def transform(self, idx):
        return self.__transform(idx)
    
    def __len__(self):
        return len(self.datas)
    
    def __getitem__(self, idx):
        data = self.transform(idx)
        return data
 