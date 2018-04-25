from PIL import Image
import requests
from io import BytesIO


import pytesseract
import argparse
import cv2
import os
import numpy

#pytesseract.pytesseract.tesseract_cmd = os.path.expanduser('~/.env/lib/python3.4/site-packages/pytesseract/pytesseract.py')
pytesseract.pytesseract.tesseract_cmd = "/home/csgrad/satyasiv/.env/lib/python3.4/site-packages/tesseract/"
url = "https://pbs.twimg.com/media/DZKXuPPVoAAvNWo.jpg"

response = requests.get(url)
img = Image.open(BytesIO(response.content))

pix = numpy.array(img)
tessdata_dir_config = '--tessdata-dir "/home/csgrad/satyasiv/.env/"'
# Example config: '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
# It's important to include double quotes around the dir path.

#pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)

text = pytesseract.image_to_string(img, config=tessdata_dir_config)
print(text)
