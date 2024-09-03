from pathlib import Path

class FileRoot:
    def __init__(self, root, rank, split_files=5_000):
        self.split_files = split_files
        self.count = 0
        self.root = Path(root).joinpath(f'{rank}').absolute()
        self.root.mkdir(parents=True, exist_ok=True)
    
    def __call__(self):
        self.count += 1
        file_numb = self.count // self.split_files + 1

        path = self.root / f"{self.split_files}_{file_numb}"
        path.mkdir(parents=True, exist_ok=True)

        return path

class RankFileWriter:
    def __init__(self, root, name, rank):
        self.file_root = Path(root)
        self.file_root.mkdir(parents=True, exist_ok=True)
        self.name = Path(name)
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
        import subprocess
        files = self.file_root.glob(self.pattern)
        cat_ifile = []
        for file_path in files:
            cat_ifile.append(file_path.as_posix())
        cat_ifile = ' '.join(cat_ifile)
        dst_path = (self.file_root / self.name).as_posix()
        subprocess.check_output(f'cat {cat_ifile} > {dst_path}', shell=True)
        
