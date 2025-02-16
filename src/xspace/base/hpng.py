from PIL import Image
from loguru import logger
from io import BytesIO
from .dstruct import StrEnum
from typing import Dict
import json

class PNGMode(StrEnum):
    ENDIAN = 'endian'
    LSB = 'lsb'

class PNGHide:
    """hide str information into png image

    Args:
        hide_mode (PNGMode, optional): hide mode['lsb' in image, 'endian' to append image]. Defaults to 'endian'.
    
    Examples:
        >>> from xspace.base import hpng
        >>> hpng = hpng.PNGHide()
        >>> hpng.encode('input.png', 'hello', 'output.png')
        >>> hpng.decode('output.png') # 'hello'
    """
    def __init__(self, hide_mode: PNGMode='endian') -> None:
        
        self.magicBytes = {
            "unencryptedLSB": 0xdeadc0de,
            "unencrypted": 0x5afec0de
        }
        self.hide_mode = hide_mode

    @staticmethod 
    def __changeLast2Bits(origByte: int, newBits: int) -> int:
        """
        This function replaces the 2 LSBs of the given origByte with newBits
        """
        # First shift bits to left 2 times
        # Then shift bits to right 2 times, now we lost the last 2 bits
        # Perform OR operation between original_number and new_bits

        return (origByte >> 2) << 2 | newBits

    @staticmethod
    def __filesizeToBytes(data: bytes) -> bytes:
        """
        This function returns the size of data in 8 bytes
        """
        return (len(data)).to_bytes(8, byteorder='big')

    @staticmethod
    def __serializeData(data: bytes, padding: int = 1) -> list:
        """
        This function packs data into groups of 2bits and returns that list
        """
        serializedData = list()
        for datum in data:
            serializedData.append((datum >> 6) & 0b11)
            serializedData.append((datum >> 4) & 0b11)
            serializedData.append((datum >> 2) & 0b11)
            serializedData.append((datum >> 0) & 0b11)

        while len(serializedData) % padding != 0:
            serializedData.append(0)

        return serializedData

    @staticmethod
    def __deserializeData(data: list) -> bytes:
        """
        This function takes data and unpacks the '2bits groups' to get original data back
        """
        deserializeData = list()
        for i in range(0, len(data) - 4 + 1, 4):
            datum = (data[i] << 6) + (data[i + 1] << 4) + (data[i + 2] << 2) + (data[i + 3] << 0)
            deserializeData.append(datum)

        return bytes(deserializeData)

    def encode(self, inputImagePath: str|Image.Image, hide_strs: str|Dict, outputImagePath: str) -> None:
        """ encode str or dict into image

        Args:
            inputImagePath (str | Image.Image): input image path or PIL image object
            hide_strs (str | Dict): str or dict to hide
            outputImagePath (str): output image path
        """
        
        if isinstance(hide_strs, Dict):
            hide_strs = json.dumps(hide_strs, ensure_ascii=False)
        data = bytes(hide_strs, "utf-8")
        
        logger.debug("[*] {} file size : {} bytes".format(hide_strs, len(data)))

        if self.hide_mode == PNGMode.LSB:
            if isinstance(inputImage, Image.Image):
                image = inputImage
            else:
                image = Image.open(inputImagePath).convert('RGB')
            pixels = image.load()

            data = (self.magicBytes["unencryptedLSB"]).to_bytes(4, byteorder='big') + self.__filesizeToBytes(data) + data
            logger.debug("[*] Magic bytes used: {}".format(hex(self.magicBytes["unencryptedLSB"])))

            if len(data) > (image.size[0] * image.size[1] * 6) // 8:
                logger.warning("[*] Maximum hidden file size exceeded")
                logger.warning("[*] Maximum hidden file size for this image: {}".format((image.size[0] * image.size[1] * 6) // 8))
                logger.warning("[~] To hide this file, choose a bigger resolution")
                exit()

            logger.debug("[*] Hiding file in image")
            data = self.__serializeData(data, padding=3)
            data.reverse()

            imageX, imageY = 0, 0
            while data:
                # Pixel at index x and y
                pixel_val = pixels[imageX, imageY]

                # Hiding data in all 3 channels of each Pixel
                pixel_val = (self.__changeLast2Bits(pixel_val[0], data.pop()),
                            self.__changeLast2Bits(pixel_val[1], data.pop()),
                            self.__changeLast2Bits(pixel_val[2], data.pop()))

                # Save pixel changes to Image
                pixels[imageX, imageY] = pixel_val

                if imageX == image.size[0] - 1:          # If reached the end of X Axis
                    # Increment on Y Axis and reset X Axis
                    imageX = 0
                    imageY += 1
                else:
                    # Increment on X Axis
                    imageX += 1

            if not outputImagePath:
                outputImagePath = ".".join(inputImagePath.split(".")[:-1]) + "_with_hidden_file" + "." + inputImagePath.split(".")[-1]

            logger.debug(f"[+] Saving image to {outputImagePath}")
            image.save(outputImagePath)
        elif self.hide_mode == PNGMode.ENDIAN:
            logger.warning("[!] Warning: You should encrypt file if using endian mode")
            data = data + self.__filesizeToBytes(data) + (self.magicBytes["unencrypted"]).to_bytes(4, byteorder='little')
            logger.debug("[*] Magic bytes used: {}".format(hex(self.magicBytes["unencrypted"])))

            # inputImage = open(inputImagePath, "rb").read()
            if isinstance(inputImagePath, Image.Image):
                image = inputImagePath
            else:
                image = Image.open(inputImagePath).convert('RGB')
            bytesIO = BytesIO()
            image.save(bytesIO, format='PNG')
            inputImage = bytesIO.getvalue()
            
            inputImage += data

            outputImage = open(outputImagePath, "wb")
            outputImage.write(inputImage)
            outputImage.close()
        else:
            raise "Invalid hide mode"
    
    def decode(self, inputImagePath: str|bytes) -> None:
        """ decode str or dict from image
        Args:
            inputImagePath (str | bytes): input image path or bytes object
        Returns:
            str: str or dict from image
        """

        if isinstance(inputImagePath, bytes):
            inputImage = inputImagePath
        else:
            inputImage = open(inputImagePath, "rb").read()
        if int.from_bytes(inputImage[-4:], byteorder='little') in [self.magicBytes["unencrypted"]]:
            logger.debug("[+] Hidden file found in image")
            hiddenDataSize = int.from_bytes(inputImage[-12:-4], byteorder="big")
            hiddenData = inputImage[-hiddenDataSize - 12:-12]

            return hiddenData.decode()
        else:

            image = Image.open(inputImagePath).convert('RGB')
            pixels = image.load()

            data = list()                                 # List where we will store the extracted bits
            for imageY in range(image.size[1]):
                for imageX in range(image.size[0]):
                    if len(data) >= 48:
                        break

                    # Read pixel values traversing from [0, 0] to the end
                    pixel = pixels[imageX, imageY]

                    # Extract hidden message in chunk of 2 bits from each Channel
                    data.append(pixel[0] & 0b11)
                    data.append(pixel[1] & 0b11)
                    data.append(pixel[2] & 0b11)

            if self.__deserializeData(data)[:4] == bytes.fromhex(hex(self.magicBytes["unencryptedLSB"])[2:]):
                logger.debug("[+] Hidden file found in image")
            else:
                logger.warning("[!] Image don't have any hidden file")
                logger.warning("[*] Magic bytes found:    0x{}".format(self.__deserializeData(data)[:4].hex()))
                logger.warning("[*] Magic bytes supported: {}".format(", ".join([hex(x) for x in self.magicBytes.values()])))
                exit()

            logger.debug("[*] Extracting hidden file from image")
            hiddenDataSize = int.from_bytes(self.__deserializeData(data)[4:16], byteorder='big') * 4

            data = list()
            for imageY in range(image.size[1]):
                for imageX in range(image.size[0]):
                    if len(data) >= hiddenDataSize + 48:
                        break

                    # Read pixel values traversing from [0, 0] to the end
                    pixel = pixels[imageX, imageY]

                    # Extract hidden message in chunk of 2 bits from each Channel
                    data.append(pixel[0] & 0b11)
                    data.append(pixel[1] & 0b11)
                    data.append(pixel[2] & 0b11)

            data = self.__deserializeData(data[48:])

            return data.decode()


if __name__ == '__main__':
    h = PNGHide(hide_mode='endian')
    h.encode('/home/ding/iwork/github/xmodel/test/images/gubin.dog.jpg', '{x:1, y:2}', 'dog.png')

    print(h.decode('dog.png'))