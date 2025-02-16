import re

class ExtractBrackets:
    """ extract brackets' content from a string

        Args:
            pat (list, optional): a pair bracket. Defaults to ['<>'].
    """
    def __init__(self, pat=['<>']):
        
        pat_str = []
        for p in pat:
            b,e = p
            pat_str.append('[%s](.*?)[%s]' % (b, e))
        
        # print(pat_str)
        self.pat = re.compile('|'.join(pat_str), re.S)

    def extract(self, xstr:str, with_flag:bool=False, index:bool=False):
        """ extract brackets' content from a string
        Args:
            xstr (str): a string
            with_flag (bool, optional): whether to return the brackets. Defaults to False.
            index (bool, optional): whether to return the index. Defaults to False.
        Returns:
            list: a list of brackets' content
        """
        
        mstr = []
        rets = re.finditer(self.pat, xstr)
        flag_offset = int(not with_flag)
        for data in rets:
            s = data.start() + flag_offset
            e = data.end() - flag_offset
            if e - s > 0:
                match = xstr[s:e]
                res = (match, (s, e)) if index else match
                mstr.append(res)
        return mstr
