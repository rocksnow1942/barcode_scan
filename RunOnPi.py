from pylibdmtx.pylibdmtx import decode
import cv2

camera = cv2.imread('./imgs/printer_iphone.jpg')


# convert image to grayscale
gray = cv2.cvtColor(camera,cv2.COLOR_BGR2GRAY)
th,threshold = cv2.threshold(gray,220,255,cv2.THRESH_BINARY)

## (2) Morph-op to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
morphed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)


## (3) Find the max-area contour
cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
cnt = sorted(cnts, key=cv2.contourArea)[-1]

## (4) Crop and save it
x,y,w,h = cv2.boundingRect(cnt)
dst = gray[y:y+h, x:x+w]

(thresh, im_bw) = cv2.threshold(dst, 160, 255,cv2.THRESH_BINARY)# cv2.THRESH_BINARY | cv2.THRESH_OTSU)


im_bw_resize = cv2.resize(im_bw,(int(im_bw.shape[1]/1),int(im_bw.shape[0]/1)))


def panel_parse(im_bw):
    "read each panel of a black and white image."
    h,w = im_bw.shape
    px = w//12
    py = h//8
    panel_result = []
    for r in range(8):
        for c in range(12):
            panel = im_bw[py*r:py*r+py,px*c:px*c+px]
            p = None
            for ratio in [3,2,1.5]:
                panel_resize = cv2.resize(panel,
                        (int(panel.shape[1]/ratio),int(panel.shape[0]/ratio)))
                res = decode(panel_resize,max_count=1,timeout=3000)
                
                if res and len(res[0].data.decode())==10 and res[0].data.decode().isnumeric():
                    p = res[0].data.decode()
                    break
            panel_result.append(p)
    return panel_result


resize_result = panel_parse(im_bw_resize)

print(resize_result)