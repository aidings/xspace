from loguru import logger
from typing import List, Callable

class Batcher(object):
    """ 根据batch_size 对list_data进行batch处理, 迭代器形式

        Args:
            list_data (List): 输入列表数据
            batch_size (int, optional): 批量大小. Defaults to 1.
            parse_ldata (Callable, optional): 处理一行数据方法. Defaults to None.
    """
    def __init__(self, list_data: List, batch_size: int=1, parse_ldata: Callable=None, **kwargs):
        
        self.list_data = list_data 
        self.batch_size = batch_size
        assert batch_size > 0, "batch_size must be greater than 0"
        self.idx = 0
        self._parse = parse_ldata or self._parse_ldata
        self.kwargs = kwargs
    
    def _parse_ldata(self, data, **kwargs):
        return data
   
    def __iter__(self):
        return self 
    
    def __next__(self):
        if self.idx >= len(self.list_data):
            self.idx = 0
            raise StopIteration
        
        batch = [] 
        bidx = self.idx
        for i in range(bidx, len(self.list_data)):
            try:
                bdata = self._parse(self.list_data[i], **self.kwargs)
                batch.append(bdata)
                if len(batch) == self.batch_size:
                    yield batch
                elif i == len(self.list_data) - 1:
                    yield batch
            except Exception as e:
                logger.error(f"Error parsing data: {e}")
            
            self.idx += 1