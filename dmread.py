from pylibdmtx.pylibdmtx import decode,encode
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
imgs = glob.glob('96DM/*.png')
originals = [i[5:15] for i in imgs]


plate = cv2.imread('plate.jpg')

single = cv2.imread('IMG_1008.jpg')

decode(single)

concat = cv2.imread('concat.jpg')

decode(concat)



res = decode(plate)


len(res)

result = []
 



camera = cv2.imread('/Users/hui/Downloads/IMG_1007.jpg')
plt.imshow(camera)

res = decode(camera,timeout=1000)

camera=single

# convert image to grayscale
gray = cv2.cvtColor(camera,cv2.COLOR_BGR2GRAY)
plt.imshow(gray,cmap='gray')


# create threshold to remove backgroud black.
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
plt.imshow(dst,cmap='gray')


# convert to black and white
(thresh, im_bw) = cv2.threshold(dst, 160, 255,cv2.THRESH_BINARY)# cv2.THRESH_BINARY | cv2.THRESH_OTSU)
plt.imshow(im_bw,cmap='gray')

# resize to smaller seems to be helpful with reading.
im_bw_resize = cv2.resize(im_bw,(int(im_bw.shape[1]/1.5),int(im_bw.shape[0]/1.5)))

plt.imshow(im_bw_resize,cmap='gray')

cv2.imwrite('im_bw_resize4.jpg',im_bw_resize)
result = decode(im_bw_resize,timeout=100000,max_count=96)


result = decode(im_bw,timeout=100000,max_count=96)
decode(im_bw)
decode(dst)

def panel_parse(im_bw):
    "read each panel of a black and white image."
    h,w = im_bw.shape
    px = w//12
    py = h//8
    panel_result = []
    for r in range(8):
        for c in range(12):
            panel = im_bw[py*r:py*r+py,px*c:px*c+px]
            res = decode(panel,max_count=1,timeout=5000)         
            if res:
                panel_result.append(res[0])
            else:
                panel_result.append(None)
    return panel_result
    
resize_result = panel_parse(im_bw_resize)

for i,dres in enumerate(resize_result):
    read = dres and dres.data.decode()
    if read != originals[i]:
        print(f'{i//12+1}x{i%12+1} : {read}=>{originals[i]}')


     