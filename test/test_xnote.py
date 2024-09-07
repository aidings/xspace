import sys

sys.path.insert(0, '../src')
from xspace.base import XNote, Image, XNoteRow
import json

def test_xnote():
    xnote = XNote('./xnote.xlsx', 'Sheet1')
    xnote[0] = XNoteRow(["索引", "标题", "内容", "标签"])
    xnote[1,0] = 0
    xnote[1,1] = "这是一个测试"
    xnote[1,3] = Image('./xzs1.jpeg')
    
    print(xnote[0])
    print(xnote[1])
    xnote.save()

    xnote = XNote.from_dict('./xnote2.xlsx', {'索引': [1, 2], '内容': ["这是一个测试", "这是一个测试2"]})
    
    xnote.save()
    
    with XNote.from_list('./xnote3.xlsx', [{'索引': 1, '内容': "这是一个测试"}, {'索引': 2, '内容': "这是一个测试2"}], head=['索引', '内容']) as xnote:
        pass

    with XNote.from_list('./xnote4.xlsx', [[1, "这是一个测试"], [2, "这是一个测试2"]], head=['索引', '内容']) as xnote:
        pass

if __name__ == '__main__':
    test_xnote()