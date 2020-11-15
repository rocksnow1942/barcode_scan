from pylibdmtx.pylibdmtx import decode,encode
import cv2
import numpy as np
import matplotlib.pyplot as plt

plate = cv2.imread('plate.jpg')

concat = cv2.imread('concat.jpg')

decode(concat)



res = decode(plate)


len(res)

result = []
 



sorted_result


camera = cv2.imread('/Users/hui/Downloads/IMG_1007.jpg')
plt.imshow(camera)

res = decode(camera,timeout=1000)



# convert image to grayscale
gray = cv2.cvtColor(camera,cv2.COLOR_BGR2GRAY)
plt.imshow(gray,cmap='gray')
th,threshold = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)


plt.imshow(threshold,cmap='gray')

## (2) Morph-op to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
morphed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

## (3) Find the max-area contour
cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
cnt = sorted(cnts, key=cv2.contourArea)[-1]

## (4) Crop and save it
x,y,w,h = cv2.boundingRect(cnt)
dst = gray[y:y+h, x:x+w]
plt.imshow(camera)
plt.imshow(dst,cmap='gray')
camera.shape
dst.shape


(thresh, im_bw) = cv2.threshold(dst, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
plt.imshow(im_bw,cmap='gray')

im_bw_resize = cv2.resize(im_bw,(im_bw.shape[1]//2,int(im_bw.shape[0]//2)))

plt.imshow(im_bw_resize,cmap='gray')

cv2.imwrite('im_bw_resize.jpg',im_bw_resize)
result = decode(im_bw_resize,timeout=100000)
len(result)

result

code = []
for r in result:
    center_left = r.rect.left + r.rect.width/2
    center_top = r.rect.top + r.rect.height/2
    code.append((r.data.decode(),center_left,center_top))

code.sort(key=lambda x: -x[2])
code



def parse_plate_result(res):    
    for r in res:
        center_left = r.rect.left + r.rect.width/2
        center_top = r.rect.top + r.rect.height/2
        result.append((r.data.decode(),center_left,center_top))

    result.sort(key=lambda x:-x[2])


    sorted_result = []

    for r in range(8):
        row = result[r*12:r*12+12]
        row.sort(key=lambda x: x[1])
        sorted_result.extend(i[0] for i in row)
    return sorted_result