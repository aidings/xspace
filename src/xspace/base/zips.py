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