import os
from collections import OrderedDict


class Returns(object):
    def __init__(self, project:str):
        """构造Server Return返回值

        Args:
            project (str): 项目名称
        """
        self.prefix = project.upper()
        self.codes = OrderedDict()
        self.codes['0'] = self.prefix + ': execution succeed'
    
    def succeed(self):
        return 0

    def __setitem__(self, code:int, msg:str):
        """注册绑定错误代码和提示信息

        Args:
            code (int): 错误代码
            msg (str): 提示信息
        """
        if str(code) in self.codes.keys():
            raise ValueError(self.prefix + ': [%s] the key is already registered.' % (str(code)))
        else:
            self.codes[str(code)] = self.prefix + ': ' + msg

    def __get_msg(self, code):
        return self.codes[str(code)]

    def help(self, path='./'):
        """生成帮助文件

        Args:
            path (str, optional): 帮助文件生成路径. Defaults to './'.
        """
        with open(os.path.join(path, self.prefix + '_help.csv'), 'w') as f:
            f.write('code,msg\n')
            for key in self.codes.keys():
                f.write('%s,%s\n' % (key, self.codes[key]))

    def __call__(self, ret, code:int):
        """生成返回代码

        Args:
            ret (any): 需要返回的值
            code (int): 确定返回代码

        Raises:
            ValueError: 返回代码不在列表中

        Returns:
            dict: 返回结构体
        """
        if str(code) not in self.codes.keys():
            raise ValueError(self.prefix + ": make sure your code in Returns")

        fret = {
            "code": code,
            "result": ret,
            "msg": self.__get_msg(code)
        }

        return fret
        
