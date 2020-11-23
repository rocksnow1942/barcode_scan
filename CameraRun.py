from io import BytesIO
import time
import picamera
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImagePath
import numpy as np

from pylibdmtx.pylibdmtx import decode
from datetime import datetime
# Create an array representing a 1280x720 image of
# a cross through the center of the display. The shape of
# the array must be of the form (height, width, color)
# a = np.zeros((2400,3200 , 3), dtype=np.uint8)
# a[240, :, :] = 0xff
# a[:, 320, :] = 0xff

def indexToGridName(index,grid=(12,8)):
    row = index//grid[0] + 1
    col = index - (row-1) * grid[0] + 1
    rowM = 'ABCDEFGHIJKLMN'[row-1]
    return f"{rowM}{col}"

class Camera(picamera.PiCamera):
    def __init__(self):
        super().__init__()
        self.loadSettings()
        self.start_preview(fullscreen=False,window = self._previewWindow)
        self._captureStream = BytesIO()
        self.overlay = self.drawOverlay()
        self.add_overlay(self.overlay.tobytes(),size=self.overlay.size,layer=3)
        
    def loadSettings(self):
        resW = 3200
        previewW = 600
        scanRatio = 0.8
        self.resolution = (resW,resW*3//4)
        # self.rotation = 90
        self.framerate = 24
        # self.hflip = True
        self._previewWindow = (10,10,previewW,previewW*3//4)
        
        self._scanGrid = (12,8)
        
        scanX = resW * (1-scanRatio) // 2
        gridSize = resW * scanRatio // (self._scanGrid[0]-1)
        scanY = (resW*3/4 - gridSize*(self._scanGrid[1]-1))//2
        
        
        self._scanWindow = (scanX,scanY,
                            scanX + gridSize*(self._scanGrid[0]-1),
                            scanY + gridSize*(self._scanGrid[1]-1))
        
        # self.contrast = 100
    
    def drawOverlay(self,highlights = []):
        pad = Image.new('RGBA',(800,480))
        padDraw = ImageDraw.Draw(pad)
        column,row = self._scanGrid
        xo,yo,pw,ph = self._previewWindow
        s1,s2,s3,s4 = self._scanWindow
        resolutionX, resolutionY = self.resolution
        scan_offset_x = s1 * pw // resolutionX
        scan_offset_y = s2 * ph // resolutionY
        gridWidth = (s3-s1) * pw / resolutionX // (column -1)
        gridHeight = (s4-s2) * ph / resolutionY // (row -1)    
        gridW_ = gridWidth*0.9//2
        gridH_ = gridHeight*0.9//2
        for r in range(row):
            for c in range(column):
                idx = r * column + c
                if idx in highlights:
                    outline = (255,0,0,180)
                else:
                    outline = (0,255,0,180)
                posx = c * gridWidth + xo + scan_offset_x
                posy = r * gridHeight + yo + scan_offset_y
                padDraw.rectangle([posx-gridW_,posy-gridH_,posx+gridW_,posy+gridH_],
                                   fill=(0,0,0,0),outline=outline,width=1)
        return pad
    
    def run(self):
        ""
        try:
            while True:                
                time.sleep(1)
                action = input("action:\n")
                if action == 's':
                    self.snapshot()
                 
                else:
                     
                    result = self.scan()
                    for i in result:
                        print(i)
                    
        finally:
            self.remove_overlay(self.overlay)
        
                
    def yieldPanel(self,img):
        "yield each panel in a image"
        column,row = self._scanGrid
        s1,s2,s3,s4 = self._scanWindow
        gridWidth = (s3-s1)//(column-1)
        gridHeight = (s4-s2)//(row-1)
        cropW = gridWidth * 1.2 // 2
        cropH = gridHeight * 1.2 // 2
        for r in range(row):
            for c in range(column):
                posx = c * gridWidth + s1
                posy = r * gridHeight + s2
                yield img.crop((posx-cropW,posy-cropH,posx+cropW,posy+cropH))

    def decodePanel(self,panel):
        px,py = panel.size
    
        for size in [100,200]:
            resize = panel.resize((size,int(size*py/px)))
            res = decode(resize,max_count=1)
            if res:
                return res[0].data.decode()
        return ""

    def snapshot(self,):
        "capture and save a image"
        self.capture(f'./{datetime.now().strftime("%H:%M:%S")} Snapshot.jpeg',format='jpeg')

    def scan(self):
        "perform a capture and decode"
        self._captureStream.seek(0)
        self.capture(self._captureStream,format='jpeg')
        self._captureStream.seek(0)
        img = Image.open(self._captureStream)
        results = []

        for idx, panel in enumerate(self.yieldPanel(img)):
            name = indexToGridName(idx,self._scanGrid)
            panel.save(f'./out/{name}.jpeg')
            res = self.decodePanel(panel)
            print(f"{name}:{res}")
            results.append(res)
        return results

c = Camera()
c.run()


# 
# 
# 
# c_w = 800
# c_h = c_w*3//4
# 
# 
# pad = Image.new('RGBA',(800,480))
# 
# padDraw = ImageDraw.Draw(pad)
# 
# padDraw.rectangle([100,100,200,200],fill=(0,0,0,0),outline=(255,0,0,180))
# 
# 
# camera = picamera.PiCamera()
# camera.resolution = (800 , 800 * 3//4)
# camera.rotation = 90
# camera.framerate = 24
# camera.hflip = True
# o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)
# 
# w_x,w_y,w_w,w_h = (0,0,320,240)
# 
# camera.start_preview(fullscreen=False,window=(w_x,w_y,w_w,w_h)) #
# # Add the overlay directly into layer 3 with transparency;
# # we can omit the size parameter of add_overlay as the
# # size is the same as the camera's resolution
# stream = BytesIO()
# 
# count = 0
# try:
#     # Wait indefinitely until the user terminates the script
#     while True:        
#         time.sleep(0.2)
#         # camera.remove_overlay(o)
#         # pad = Image.new('RGBA',(800,480))
#         # count += 1
#         # padDraw = ImageDraw.Draw(pad)
#         # outline = (0,255,0,180) if count%2 else ((0,0,255,180))
#         # padDraw.rectangle([150,110,170,130],fill=(0,0,0,0),outline=outline,wdith=1)
#         # # padDraw.rectangle([x*w_w//c_w,y*w_w//c_w,(x+w)*w_w//c_w,(y+h)*w_w//c_w],fill=(0,0,0,0),outline=(0,255,0,180))
#         # o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)
#         # 
#         # capture and detect
#         stream.seek(0)
#         camera.capture(stream,format='jpeg',) #resize=(c_w,c_h)
#         stream.seek(0)
#         img = Image.open(stream)
#         img = ImageOps.mirror(img)
# 
#         code = decode(img)
#         if code:
#             if o:
#                 camera.remove_overlay(o)
#             code = code[0]
#             print(code)
#             xy = [ (i.x*w_w//c_w +w_x ,i.y*w_w//c_w + w_y) for i in code.polygon]
#             # 
#             # x,y = code.rect.left,code.rect.top
#             # w,h = code.rect.width,code.rect.height
#             pad = Image.new('RGBA',(800,480))
# 
#             padDraw = ImageDraw.Draw(pad)
# 
#             padDraw.polygon(xy,fill=(0,0,0,0),outline=(0,255,0,180))
#             # padDraw.rectangle([x*w_w//c_w,y*w_w//c_w,(x+w)*w_w//c_w,(y+h)*w_w//c_w],fill=(0,0,0,0),outline=(0,255,0,180))
#             o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)
#         else:
#             if o:
#                 camera.remove_overlay(o)
#                 o = None
# except:
#     pass
# finally:
#     if o:
#         camera.remove_overlay(o)
# 