from pylibdmtx.pylibdmtx import decode
import time
from PIL import Image 

img = Image.open('./camera_croped.jpg')

import glob
imgs = glob.glob('96DM/*.png')
originals = [i[5:15] for i in imgs]




# img
# imga = np.array(img)
# 
# imga.shape
# 
# 
# camera = cv2.imread('./imgs/printer_iphone.jpg')
# 
# 
# # convert image to grayscale
# gray = cv2.cvtColor(camera,cv2.COLOR_BGR2GRAY)
# th,threshold = cv2.threshold(gray,220,255,cv2.THRESH_BINARY)
# 
# ## (2) Morph-op to remove noise
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
# morphed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
# 
# 
# ## (3) Find the max-area contour
# cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
# cnt = sorted(cnts, key=cv2.contourArea)[-1]
# 
# ## (4) Crop and save it
# x,y,w,h = cv2.boundingRect(cnt)
# dst = gray[y:y+h, x:x+w]
# dst2 = camera[y:y+h, x:x+w]
# 
# 
# 
# (thresh, im_bw) = cv2.threshold(dst, 160, 255,cv2.THRESH_BINARY)# cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# 
# 
# im_bw_resize = cv2.resize(im_bw,(int(im_bw.shape[1]/1),int(im_bw.shape[0]/1)))
# 

def decode_panel(panel):
    px,py = panel.size
    p = None
    for ratio in [3,2,1.5]:
        panel_resize = panel.resize(( int(px/ratio) , int(py/ratio) ))
        res = decode(panel_resize,max_count=1,timeout=3000)
        
        if res and len(res[0].data.decode())==10 and res[0].data.decode().isnumeric():
            p = res[0].data.decode()
            return p
    return p
    


def panel_parse(im_bw):
    "read each panel of a black and white image."
    w,h = im_bw.size
    px = w//12
    py = h//8
    panel_result = []
    for r in range(8):
        for c in range(12):
            panel = im_bw.crop((px*(c -0.1) ,py*(r-0.1),px*(c+1.1),py*(r+1.1),))
            p = decode_panel(panel)
            panel_result.append(p)
    return panel_result

def show_panel(im_bw,panel,offset=(0,0)):
    r,c = panel
    x,y = offset
    w,h = im_bw.size
    px = w//12
    py = h//8
    r-=1
    c-=1    
    panel_img = im_bw.crop((px*(c-0.1)+x,py*(r-0.1)+y,px*(c+1.1)+x,py*(r+1.1)+y,))
    return panel_img


if __name__ == '__main__':
    t0 = time.perf_counter()
    resize_result = panel_parse(img)
    t1 = time.perf_counter()

    print(f'Time elasped: {t1-t0:.6f}s')

    for i,dres in enumerate(resize_result):
        if dres not in originals:
            print(f'{i//12+1}x{i%12+1} : {dres}=>{originals[i]}')
        else:
            print(f'{i//12+1}x{i%12+1} : correct')