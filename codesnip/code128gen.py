import matplotlib.pyplot as plt
import random
from barcode import EAN13,Code128,UPCA
import cv2
from barcode.writer import ImageWriter
import numpy as np
from io import BytesIO
from string import printable


text = f"{int(random.random()*10**10):010}"

for i in range(10):
    text = f"{int(random.random()*10):010}"

hex(124)
len(printable)

def convert(x,string):
    "it seems that with less than 10 digits, use only number is much easier."
    l = len(string)
    digits = []
    while x:
        digits.append(string[x % l])
        x = int(x/l)
    return ''.join(digits[::-1])
        

h = convert(int(text),printable)



buf = BytesIO()
c128 = Code128(text,writer=ImageWriter())

c128 = Code128(h,writer=ImageWriter())

c128.write('128ascii.jpg')

c128.write(buf)


buf.seek(0)
filebyte = np.asarray(bytearray(buf.read()),dtype=np.uint8)
filebyte
img = cv2.imdecode(filebyte,cv2.IMREAD_GRAYSCALE)
img.shape
len(filebyte)

plt.imshow(img,cmap='gray')

cv2.imread(buf.getvalue())

with open('test.jpg', 'wb') as f:
    f.write(buf)


img_np = cv2.imdecode(buf.read(), cv2.CV_LOAD_IMAGE_COLOR)