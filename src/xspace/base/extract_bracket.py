import re

class ExtractBrackets:
    def __init__(self, pat=['<>']):
        pat_str = []
        for p in pat:
            b,e = p
            pat_str.append('[%s](.*?)[%s]' % (b, e))
        
        # print(pat_str)
        self.pat = re.compile('|'.join(pat_str), re.S)

    def extract(self, xstr, with_flag=False, index=False):
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
