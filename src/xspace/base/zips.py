from pathlib import Path
import zipfile
from tqdm import tqdm

def zip_files(file_list, zip_pth):
    # 创建一个新的 ZIP 文件
    with zipfile.ZipFile(zip_pth, 'w') as new_zip:
        for file_path in tqdm(file_list, desc='zipping files'):
            new_zip.write(file_path)

# 上下文管理器确保在退出代码块时关闭 ZIP 文件


def unzip_files(zip_pth, root_path):
    zip_pth = Path(zip_pth)
    root_path = Path(root_path)
    zip_file = zipfile.ZipFile(zip_pth.as_posix())
    zip_list = zip_file.namelist() # 得到压缩包里所有文件
    nzip_list = []
    for name in zip_list:
        if '__MACOSX' not in name:
            nzip_list.append(name)

    name = zip_pth.stem
    save_root = Path(root_path)
    # save_root = os.path.join(root_path, name)
    # save_root = root_path.joinpath(name)

    if len(nzip_list) == 1:
        save_root.parent.mkdir(parents=True, exist_ok=True)
        for f in nzip_list:
            zip_file.extract(f, save_root.parent.as_posix()) # 循环解压文件到指定目录
    else:
        save_root.mkdir(parents=True, exist_ok=True)
        for f in nzip_list:
            zip_file.extract(f, save_root.as_posix()) # 循环解压文件到指定目录

    zip_file.close() # 关闭文件，必须有，释放内存
    return len(nzip_list)

class ZipFileReader:
    """ ZipFileReader reads files from a zip file.

        Args:
            zip_pth (os.PathLike): zip file path.
            use_idx_key (bool, optional): use index as key or file name as key. Defaults to False.
    """
    def __init__(self, zip_pth, use_idx_key=False):
        
        self.zip_ref = zipfile.ZipFile(zip_pth, 'r')
        self.name_list = self.zip_ref.namelist()
        self.__get = self.__get_by_idx if use_idx_key else self.__get_by_pth
        self.__idx = 0
        self.zip_root = zipfile.Path(self.zip_ref, at='')
    
    def is_file(self, index: int | str):
        name = self.__get(index)
        return self.zip_root.joinpath(name).is_file()
    
    def __get_by_idx(self, idx: int):
        return self.name_list[idx]
    
    def __get_by_pth(self, pth: str):
        return pth
    
    def __len__(self):
        return len(self.name_list)
    
    def __getitem__(self, index):
        name = self.__get(index)
        return self.__read_file(name)
    
    def __setitem__(self, index, value):
        raise NotImplementedError('ZipImageReader does not support assignment')
    
    def __iter__(self):
        return self
    
    def __read_file(self, name: str):
        with self.zip_ref.open(name) as f:
            return f
    
    def __next__(self):
        if self.__idx >= len(self.name_list):
            self.__idx = 0
            raise StopIteration
        name = self.__get_by_idx(self.__idx)
        self.__idx += 1
        return self.__read_file(name)
        