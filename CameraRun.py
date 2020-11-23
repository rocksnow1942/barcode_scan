from io import BytesIO
import time
import picamera
from PIL import Image,ImageDraw
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
        self.start_preview(fullscreen=False,window = self._previewWindow,hflip=True,rotation=90)
        self._captureStream = BytesIO()
        self.overlay = None
        self.drawOverlay()
        
    def loadSettings(self):
        resW = 1200
        previewW = 300
        scanRatio = 0.8
        self.resolution = (resW,resW*3//4)
        
        self.framerate = 24
        
        # preview window is rotated 90 deg and mirrorred.
        self._previewWindow = (30,10,previewW,previewW*4//3)
        
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
        # because preview is flipped and rotated,
        # the x overlay offset caused by scan window is actually y offset of scan window
        scan_offset_y = s1 * ph // resolutionX #in preview window, overlay offset caused by scan window in y direction.
        scan_offset_x = s2 * pw // resolutionY #in preview window, overlay offset caused by scan window in x direction.
        
        gridHeight = (s3-s1) * ph / resolutionX // (column -1) # overlay grid height in preview window, this is actually scan window width.
        gridWidth = (s4-s2) * pw / resolutionY // (row -1)   # overlay grid height in preview window, this is actually scan window height. 
        gridW_ = gridWidth*0.9//2 # half width of actually drawing box in preview window
        gridH_ = gridHeight*0.9//2 # half width of actually drawing box in preview window
        for r in range(row):
            for c in range(column):
                idx = r * column + c
                if idx in highlights:
                    outline = (255,0,0,180)
                    width = 3
                else:
                    outline = (0,255,0,180)
                    width = 1
                posy = c * gridHeight + yo + scan_offset_y
                posx = r * gridWidth + xo + scan_offset_x
                padDraw.rectangle([posx-gridW_,posy-gridH_,posx+gridW_,posy+gridH_],
                                   fill=(0,0,0,0),outline=outline,width=width)
        if self.overlay:
            self.remove_overlay(self.overlay)        
        self.overlay = self.add_overlay(pad.tobytes(),size=pad.size,layer=3)
    
    def run(self):
        ""
        try:
            while True:                
                time.sleep(1)
                action = input("action:\n").strip()
                if action == 's':
                    self.snapshot()
                elif action.isnumeric():
                    self.drawOverlay(highlights = [int(action)])
                else:                     
                    result = self.scan()
                    highlights = []
                    for idx,res in enumerate(result):
                        if len(res)!=10 or (not res.isnumeric()):
                            highlights.append(idx)
                    self.drawOverlay(highlights)
                        

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
        res = decode(panel,max_count=1)
        if res:
            return res[0].data.decode()
        return ""
        # px,py = panel.size
    
        # for size in [100,200]:
        #     resize = panel.resize((size,int(size*py/px)))
        #     res = decode(resize,max_count=1)
        #     if res:
        #         return res[0].data.decode()
        # return ""

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