from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt
from PIL import Image
from pyautogui import *

def ocr_img_text(path="", saveimg=False, printResult=False):
    image = path
    if image == "":
        return None
    else:
        image = Image.open(image).convert('RGB')
    
    ocr = PaddleOCR(use_angle_cls = True, lang = 'ch')

    result = ocr.ocr(image, cls = True)

    if printResult is True:
        for line in result:
            for word in line:
                print(word)


ocr_img_text(path='start.png', printResult=True)