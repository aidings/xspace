import os
from pathlib import Path
import numpy as np
from PIL import Image
import imageio.v3 as iio
from io import BytesIO
import base64
import torch
import torchvision.transforms as TF
from .dstruct import StrEnum


def to_pil(img_buf: bytes|Path|str|np.ndarray|Image.Image|torch.Tensor, mode:str = 'RGB'):
    if isinstance(img_buf, bytes):
        image = iio.imread(img_buf)
        image = Image.fromarray(image).convert(mode)
    elif isinstance(img_buf, (Path, str)) and Path(img_buf).exists():
        image = Image.open(img_buf)
        image = image.convert(mode)
    elif isinstance(img_buf, np.ndarray):
        image = Image.fromarray(img_buf).convert(mode)
    elif isinstance(img_buf, Image.Image):
        image = img_buf.convert(mode)
    elif isinstance(img_buf, torch.Tensor):
        if len(img_buf.shape) == 3:
            image = TF.ToPILImage()(img_buf).convert(mode)
        else:
            image = None
            raise RuntimeError(f'Input Image error, please check out {img_buf}') 
    else:
        image = None
        raise RuntimeError(f'Input Image error, please check out {img_buf}')

    return image


def to_npy(img_buf: bytes|Path|str|np.ndarray|Image.Image|torch.Tensor):
    if isinstance(img_buf, bytes):
        image = iio.imread(img_buf)
    elif isinstance(img_buf, str) and os.path.isfile(img_buf):
        image = iio.imread(img_buf)
    elif isinstance(img_buf, str) and img_buf.startswith('http'):
        image = iio.imread(img_buf)
    elif isinstance(img_buf, np.ndarray):
        image = img_buf
    elif isinstance(img_buf, Image.Image):
        image = np.asarray(img_buf)
    elif isinstance(img_buf, torch.Tensor):
        if len(img_buf.shape) == 3:
            image = img_buf.cpu().numpy().transpose(1, 2, 0)
        else:
            raise ValueError('Error: Not support this shape tensor.shape')
    else:
        image = None
        raise ValueError('Error: Not support this type image buffer(byte, str, np.ndarry, PIL.Image)')
    
    if image.shape[2] == 4:
        color = image[:, :, 0:3].astype(np.float32)
        alpha = image[:, :, 3:4].astype(np.float32) / 255.0
        y = color * alpha + 255.0 * (1.0 - alpha)
        image = y.clip(0, 255).astype(np.uint8) 
    return image

class ImageTypeReader(StrEnum):
    PIL = 'pil'
    NPY = 'npy'
    STR = 'str'

class ImageFolderReader:
    __read_dict = {
        ImageTypeReader.PIL: to_pil,
        ImageTypeReader.NPY: to_npy,
        ImageTypeReader.STR: lambda x: x
    }
    def __init__(self, file_root, exts = ['.jpg', '.png', '.bmp', '.jpeg'], read_type:ImageTypeReader = ImageTypeReader.PIL):
        self.img_dir = []
        self.exts = []

        for img_dir in Path(file_root).glob(f'**/*'):
            if img_dir.suffix.lower() in exts:
                self.img_dir.append(img_dir)
        
        self.read_func = ImageFolderReader.__read_dict[read_type]
    
    def __len__(self):
        return len(self.img_dir)
    
    def __getitem__(self, idx):
        return self.read_func(self.img_dir[idx])

def image2bytes(img_buf: str|Path|Image.Image):
    if isinstance(img_buf, (Path, str)):
        try:
            return open(img_buf, 'rb').read()
        except:
            return base64.b64decode(img_buf)
    elif isinstance(img_buf, Image.Image):
        bytesIO = BytesIO()
        img_buf.save(bytesIO, format='PNG')
        return bytesIO.getvalue()
    else:
        raise ValueError('Error: Not support this type image buffer(byte, str, PIL.Image)')
