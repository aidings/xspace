from loguru import logger

class Batcher(object):
    def __init__(self, list_data, batch_size=1, parse_ldata=None, **kwargs):
        self.list_data = list_data 
        self.batch_size = batch_size
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