import os
from PIL import Image
import pytesseract
import cv2
from enum import Enum
import argparse

imageFiles = ['.jpg', '.jpeg', '.png', '.svg']
pdfFiles = ['.pdf']

class FileType(Enum):
    IMAGETYPE = 1
    PDFTYPE = 2


def main(args):
    """ 
    """
    if (getFileType(args.file) == FileType.IMAGETYPE):
        return processImageFile(args.file, args.program)

def getFileExtension(file):
    """
    """
    _, fileExtension = os.path.splitext(file)
    return fileExtension


def getFileType(file):
    """
    """
    fileExtension = getFileExtension(file)
    if (fileExtension in imageFiles):
        return FileType.IMAGETYPE
    if (fileExtension in pdfFiles):
        return FileType.PDFTYPE


def processImageFile(file, cmd=None):
    """
    """
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    tempImage = "tempImage" + getFileExtension(file)
    cv2.imwrite(tempImage, gray)

    if cmd is not None:
        pytesseract.pytesseract.tesseract_cmd = cmd

    return (pytesseract.image_to_string(Image.open(tempImage)))


def processPdfFile(file):
    """
    """
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",  help="the imput file from which to extract text")
    parser.add_argument("-p", "--program", help="the location of the tesseract command")
    args = parser.parse_args()
    print(main(args))
