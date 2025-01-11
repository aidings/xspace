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
from typing import List
from .colors import COLOR_64
from collections import OrderedDict


def to_pil(img_buf: bytes|Path|str|np.ndarray|Image.Image|torch.Tensor, mode:str = 'RGB'):
    if isinstance(img_buf, bytes) or isinstance(img_buf, str) and img_buf.startswith('http'):
        image = iio.imread(img_buf)
        image = Image.fromarray(image)
    elif isinstance(img_buf, (Path, str)) and Path(img_buf).exists():
        image = Image.open(img_buf)
    elif isinstance(img_buf, np.ndarray):
        image = Image.fromarray(img_buf)
    elif isinstance(img_buf, Image.Image):
        image = img_buf
    elif isinstance(img_buf, torch.Tensor):
        if len(img_buf.shape) == 3:
            image = TF.ToPILImage()(img_buf)
        else:
            image = None
            raise RuntimeError(f'Input Image error, please check out {img_buf}') 
    else:
        image = None
        raise RuntimeError(f'Input Image error, please check out {img_buf}')
    
    if mode:
        image = image.convert(mode)

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
    
    if len(image.shape) > 2 and image.shape[2] == 4:
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
    if isinstance(img_buf, (str, Path)):
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


import numpy as np
from PIL import Image, ImageDraw 


class ImageMasker(object):
    def __init__(self, width, height, label=0, canvas=None):
        if canvas is not None:
            self.canvas = canvas
        else:
            self.canvas = Image.new('L', (width, height), label)
        self.draw = ImageDraw.Draw(self.canvas)

    def rect(self, left, top, right, bottom, label=255, width=1):
        self.draw.rectangle((left, top, right, bottom), fill=label, width=width)
    
    def save(self, file_name):
        self.canvas.save(file_name)
    
    def circle(self, x, y, radius, label=255, width=1):
        self.draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=label, width=width)
    
    def polygon(self, points, label=255, width=1):
        self.draw.polygon(points, fill=label, width=width)
    
    def line(self, x1, y1, x2, y2, label=255, width=1):
        self.draw.line((x1, y1, x2, y2), fill=label, width=width)
    
    def image(self, imgbuf, tl=(0,0)):
        image = to_pil(imgbuf, mode='L')
        self.canvas.paste(image, tl)

    @classmethod
    def from_file(cls, imgbuf):
        image = to_pil(imgbuf, mode='L')
        return cls(image.size[0], image.size[1], canvas=image)
    
    def to_npy(self):
        return np.array(self.canvas)
    
    def show_mask(self, image):
        mask = np.array(self.canvas, dtype=np.float32)
        if mask.max() > 1:
            mask /= 255
        mask = mask[:, :, np.newaxis]
        image_float = np.array(image, dtype=np.float32)
        result = image_float * (1 - mask) + image_float * mask * 0.7
        result = result.clip(0, 255)
        return Image.fromarray(result.astype(np.uint8))


class ImagePaster:
    def __init__(self, width, height, color=(255, 255, 255)):
        if len(color) == 3:
            self.bg = Image.new('RGB', (width, height), color)
        elif len(color) == 1:
            self.bg = Image.new('L', (width, height), color)
        else:
            raise ValueError('Error: Not support this color')
    
    def paste(self, imgbuf, tl=(0,0)):
        image = to_pil(imgbuf, mode=self.bg.mode)
        self.bg.paste(image, tl)
        return self.bg
    
    @classmethod
    def from_file(cls, imgbufs:List = [], row=1, color=255, img_width=None, resample=Image.BILINEAR):
        """ create new image with images from imgbufs

        Args:
            imgbufs (List, optional): lot of image buffer. Defaults to [].
            row (int, optional): canvas row number. Defaults to 1.
            color (int, optional): background color. Defaults to 255.
            img_width (int, optional): same width for all images. Defaults to None.
            resample (int, optional): resize method. Defaults to Image.BILINEAR.

        Returns:
            ImagePaster: a new image with images from imgbufs
        """
        nimg = len(imgbufs)
        assert nimg > 0, 'Error: No image input'
        imgs = []
        whr = None

        # makesure all image has same width/height ratio
        # and resize all image to same width
        for imgbuf in imgbufs:
            img = to_pil(imgbuf, mode=None)
            if whr is None:
                whr = img.size[0] / img.size[1]
                if img_width is None:
                    img_width = img.size[0]
            else:
                assert img.size[0] / img.size[1] == whr, 'Error: Image width/height ratio not match'
            
            img = img.resize((img_width, int(img_width / img.size[0] * img.size[1])), resample=resample)
            imgs.append(img)
        
        # split images to row x col
        images = []
        col = int(np.ceil(nimg / row))
        x, y = 0, 0
        for i in range(row): 
            img_row = []
            for j in range(col):
                idx = i * col + j
                img_row.append((imgs[idx], (x, y)))
                x += imgs[idx].size[0]
            y += imgs[idx].size[1]
            images.append(img_row)
        
        # create new image with max width and height
        width = max([len(row) for row in images]) * images[0].size[0]
        height = col * images[0].size[1]

        # create canvas and paste images
        obj = cls(width, height, color=color)
        for row in images:
            for col in row:
                obj.paste(row[0], tl=col[1])
        
        return obj

from dataclasses import dataclass, field

@dataclass
class ImageWithMask:
    image: Image.Image
    mask: Image.Image
    label: List[str] = field(default_factory=list) 

    def __post_init__(self):
        assert self.image.size == self.mask.size and \
            self.image.mode == 'RGB' and \
                self.mask.mode == 'L', 'Error: Image and Mask size or mode not match'

        nc = len(set(self.mask.getdata()))
        if len(self.label) == 0:
            self.label = [f'{i}' for i in range(1, nc)]
        else:
            if nc == len(self.label):
                self.label = self.label[1:]
            elif nc == len(self.label) + 1:
                pass
            else:
                raise ValueError('Error: Label number not match')
            
    @classmethod
    def from_class(cls, image: Image.Image, mask: Image.Image, labels: List[str]):
        lsets = OrderedDict()
        imask = np.array(mask)
        
        for idx, label in enumerate(labels):
            if label not in lsets:
                lsets[label] = idx
            else:
                imask[imask == idx] = lsets[label]
        
        return cls(image, Image.fromarray(imask), list(lsets.keys()))
         
    def concat(self):
        image = np.asarray(self.image)
        mask = np.asarray(self.mask)
        mask = mask[:, :, np.newaxis]
        image_with_mask = np.concatenate((image, mask), axis=2)
        return image_with_mask
    
    def resize(self, size):
        image = self.image.resize(size, resample=Image.Resampling.LANCZOS)
        mask = self.mask.resize(size, resample=Image.Resampling.NEAREST)

        return ImageWithMask(image, mask, self.label)
    
    def show(self, alpha=0.5):
        nc = len(COLOR_64)
        unique_values = set(self.mask.getdata())
        if len(unique_values) > nc:
            raise ValueError(f"Mask contains more than {nc} unique values")

        # 创建一个空白的彩色图像
        colored_mask = Image.new('RGB', self.mask.size)

        # 根据mask的值填充颜色
        draw = ImageDraw.Draw(colored_mask)
        imask = np.asarray(self.mask)
        colors = []
        for value in unique_values:
            if value == 0:  # 跳过背景
                continue
            color = COLOR_64[value % nc]
            mask = ((imask == value) * 255).astype(np.uint8)
            draw.bitmap((0, 0), Image.fromarray(mask), fill=color)
            colors.append(color)

        # 将彩色mask与原图像混合
        output_image = Image.blend(self.image, colored_mask, alpha)
        
        return dict(show=output_image, label_color=dict(zip(self.label, colors)), colored_mask=colored_mask)
    
    def blend(self, image):
        return self.image.copy().paste(image, mask=self.mask)
        

        