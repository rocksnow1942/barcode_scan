

from pylibdmtx.pylibdmtx import decode,encode
from PIL import Image
import random

for i in range(96):
    d = f"{int(random.random()* (10**10)):010}"
    print(d)
    text = d
    dm = encode(text.encode(),scheme='AutoBest',size='12x12')
    # print(dm)
    img = Image.frombytes('RGB',(dm.width,dm.height),dm.pixels)
    img.save(f"./96DM/{text}.png")




import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import random



def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(255,255,255))
    return result

def add_border(image,percent):
    row,col = image.shape[:2]    
    mean = cv2.mean(image[row-2:row,0:col])[0]
    return cv2.copyMakeBorder(image, top=int(row*percent),
            bottom=int(row*percent), left=int(col*percent), 
            right = int(col*percent), borderType=cv2.BORDER_CONSTANT,value=[mean,mean,mean])


imgs = glob.glob('96DM/*.png')
rows = []
for r in range(8):
    cols = []
    for c in range(12):
        img = cv2.imread(imgs[r*12+c])
        img = add_border(img,0.33)
        deg = random.random()*360
        imgr = rotate_image(img,deg)
        cols.append(imgr)
    rows.append(cv2.hconcat(cols))

plate = cv2.vconcat(rows)

cv2.imwrite('plate.jpg',plate)


i = cv2.imread('./imgs/plate.jpg')

plt.imshow(i)

i.shape
i.shape[1::-1]


o = i.copy()

rect = cv2.rectangle(o,(200,200),(300,300),(0,255,0),50)

plt.imshow(o)

cv2.putText(o,'Test text',(200,200),cv2.FONT_HERSHEY_SIMPLEX,4,(255,0,0),5)

plt.imshow(o)



cv2.imwrite('test.png',o)