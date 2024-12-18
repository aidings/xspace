from typing import List, Dict
import json
import csv
from copy import deepcopy as dcp

class ListDict:
    def __init__(self, list_dict: List[Dict] = []):
        self.list_dict = list_dict
        self.kick_dict = {}
    
    @classmethod
    def from_json_list(cls, json_list_path: str):
        list_dict = []
        with open(json_list_path, 'r') as f:
            for line in f:
                list_dict.append(json.loads(line.strip()))
        
        return cls(list_dict)
    
    @classmethod 
    def from_dict(cls, dict_path: str|Dict, key_name: str='index'):
        list_dict = []
        if isinstance(dict_path, str):
            with open(dict_path, 'r') as f:
                kdict = json.load(f)
                for key in kdict.keys():
                    value = kdict[key]
                    value[key_name] = key
                    list_dict.append(value)
        else:
            for key in dict_path.keys():
                value = dict_path[key]
                value[key_name] = key
                list_dict.append(value)

        return cls(list_dict)
    
    @classmethod
    def from_csv(cls, csv_path: str, delimiter: str=','):
        list_dict = []
        with open(csv_path, 'r') as f:
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader)

            for row in reader:
                line_dict = dict(zip(header, row))
                list_dict.append(line_dict)
        return cls(list_dict)
    
    def set_key(self, key: str):
        list_dict = dcp(self.list_dict) 
        kick_dict = {}
        for line_dict in list_dict.keys():
            value = line_dict.pop(key)
            kick_dict[value] = line_dict
        
        self.kick_dict = kick_dict

    def __getitem__(self, key):
        return self.kick_dict[key]
    
    def __setitem__(self, key, value):
        raise NotImplementedError
    
    def keys(self):
        return self.kick_dict.keys()
    
    def __len__(self):
        return len(self.list_dict)
    
    def save(self, csv_path: str, delimiter: str=','):
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            header = list(self.list_dict[0].keys())
            writer.writerow(header)
            for line_dict in self.list_dict:
                row = [line_dict.get(key, '') for key in header]
                writer.writerow(row)
    
            