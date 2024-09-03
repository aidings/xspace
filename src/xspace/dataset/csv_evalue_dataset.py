import csv
import inspect
from types import MethodType

class CSVEvalueDataset:
    def __init__(self, csv_pth, head_type={}, **kwargs):
        
        lines = []
        with open(csv_pth, 'r') as f:
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
    
        self.datas = lines
        self.__transform = lambda idx : self.datas[idx]
        self.kwargs = kwargs
    
    def register_transform(self, trans_function):
        signature = inspect.signature(trans_function)
        values = list(signature.parameters.values())
        assert len(values) == 2, f"The transform function should have two parameters, but got {len(values)}"
        assert issubclass(values[0].annotation,CSVEvalueDataset) and values[1].annotation == int, \
            f"The first parameter should be {CSVEvalueDataset}, but got {values[0].annotation}\n \
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
 