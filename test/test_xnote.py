import sys

sys.path.insert(0, '../src')
from xspace.base import XNote, Image
import json

def test_xnote():
    xnote = XNote('./xnote.xlsx', 'Sheet1')
    xnote[0] = ["索引", "标题", "内容", "标签"]
    xnote[1,0] = 0
    xnote[1,1] = "这是一个测试"
    xnote[1,3] = Image('./xzs1.jpeg')
    
    print(xnote[0])
    print(xnote[1])
    xnote.save()

if __name__ == '__main__':
    test_xnote()