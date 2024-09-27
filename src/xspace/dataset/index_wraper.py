
class DatasetIndexWrapper:
    def __init__(self, dataset):
        self.dataset = dataset
        self.didx = list(range(len(dataset)))
    
    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, index):
        if index >= len(self.dataset):
            raise IndexError("Index out of range")
        
        data = self.dataset[index]
        if isinstance(data, tuple):
            return data + (self.didx[index],)
        elif isinstance(data, list):
            return data + [self.didx[index]]
        elif isinstance(data, dict):
            data['_ridx'] = self.didx[index]
            return data
        else:
            raise TypeError(f"Unsupported data type {self.dataset[index].__class__}")
