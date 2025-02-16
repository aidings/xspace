from types import SimpleNamespace

class Dict2Attr(SimpleNamespace):
    """ Convert a dictionary to a class with attributes.

        Args:
            dictionary (dict): a python dictionary
            **kwargs: other keyword arguments
    """
    def __init__(self, dictionary, **kwargs):
        
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, Dict2Attr(value))
            elif isinstance(value, list):
                self.__setattr__(key, map(Dict2Attr, value))
            else:
                self.__setattr__(key, value)
        self.dictionary = dictionary
    
    def __getitem__(self, key):
        return self.dictionary[key] 
    
    def __setitem__(self, key, value):
        self.dictionary[key] = value
    
    def kwargs(self):
        return self.dictionary