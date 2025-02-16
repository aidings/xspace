from pathlib import Path

class FileRoot:
    """ Create a file root for a given rank. and create a new director every split_files.

        Args:
            root (str): the root directory for the files each rank.
            rank (int): the rank of the file root.
            split_files (int, optional): each split_files to create a new director . Defaults to 5_000.
    """
    def __init__(self, root, rank, split_files=5_000):
        
        self.split_files = split_files
        self.count = 0
        self.root = Path(root).joinpath(f'{rank}').absolute()
        self.root.mkdir(parents=True, exist_ok=True)
    
    def __call__(self):
        """ Get the next file path.
        Returns:
            pathlib.Path: the next file path.
        """
        self.count += 1
        file_numb = self.count // self.split_files + 1

        path = self.root / f"{self.split_files}_{file_numb}"
        path.mkdir(parents=True, exist_ok=True)

        return path

class RankFileWriter:
    """ Create a file writer for a given rank.
        Args:
            root (str): the root directory for the files each rank.
            name (str): the name of the file. Defaults to "result.txt".
            rank (int, optional): the rank of the file. Defaults to -1.
    """
    def __init__(self, root, name:str="result.txt", rank=-1):
        self.file_root = Path(root)
        self.file_root.mkdir(parents=True, exist_ok=True)
        self.name = Path(name)
        if rank == -1:
            self.pattern = None
            name = self.name.as_posix()
        else:
            self.pattern = self.name.stem + '_rank*' + self.name.suffix
            name = self.name.stem + f'_rank{rank}' + self.name.suffix

        self.file = (self.file_root / name).open(mode='w')
        
    
    def write(self, string):
        self.file.write(string)
        self.file.flush()
    
    def close(self):
        self.file.close()
    
    def __enter__(self): 
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    def combine(self):
        """ Combine all the files with the same name.
        """
        if self.pattern is not None:
            import subprocess
            files = self.file_root.glob(self.pattern)
            cat_ifile = []
            for file_path in files:
                cat_ifile.append(file_path.as_posix())
            cat_ifile = ' '.join(cat_ifile)
            dst_path = (self.file_root / self.name).as_posix()
            subprocess.check_output(f'cat {cat_ifile} > {dst_path}', shell=True)
        
