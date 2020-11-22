from io import BytesIO
import time
import picamera
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImagePath
import numpy as np
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode
# Create an array representing a 1280x720 image of
# a cross through the center of the display. The shape of
# the array must be of the form (height, width, color)
# a = np.zeros((2400,3200 , 3), dtype=np.uint8)
# a[240, :, :] = 0xff
# a[:, 320, :] = 0xff

c_w = 800
c_h = c_w*3//4


pad = Image.new('RGBA',(800,480))

padDraw = ImageDraw.Draw(pad)

padDraw.rectangle([100,100,200,200],fill=(0,0,0,0),outline=(255,0,0,180))


camera = picamera.PiCamera()
camera.resolution = (200 * 4, 200 * 3)
camera.rotation = 90
camera.framerate = 24
camera.hflip = True
o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)

w_x,w_y,w_w,w_h = (0,0,320,240)

camera.start_preview(fullscreen=False,window=(w_x,w_y,w_w,w_h)) #
# Add the overlay directly into layer 3 with transparency;
# we can omit the size parameter of add_overlay as the
# size is the same as the camera's resolution
stream = BytesIO()

count = 0
try:
    # Wait indefinitely until the user terminates the script
    while True:        
        time.sleep(1)
        camera.remove_overlay(o)
        pad = Image.new('RGBA',(800,480))
        count += 1
        padDraw = ImageDraw.Draw(pad)
        outline = (0,255,0,180) if count%2 else ((0,0,255,180))
        padDraw.rectangle([150,110,170,130],fill=(0,0,0,0),outline=outline)
        # padDraw.rectangle([x*w_w//c_w,y*w_w//c_w,(x+w)*w_w//c_w,(y+h)*w_w//c_w],fill=(0,0,0,0),outline=(0,255,0,180))
        o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)
        
        # # capture and detect
        stream.seek(0)
        camera.capture(stream,format='jpeg',) #resize=(c_w,c_h)
        stream.seek(0)
        img = Image.open(stream)
        # img = ImageOps.mirror(img)
        
        # code = decode(img)
        # if code:
        #     if o:
        #         camera.remove_overlay(o)
        #     code = code[0]
        #     print(code.data.decode())
        #     xy = [ (i.x*w_w//c_w +w_x ,i.y*w_w//c_w + w_y) for i in code.polygon]
        #     # 
        #     # x,y = code.rect.left,code.rect.top
        #     # w,h = code.rect.width,code.rect.height
        #     pad = Image.new('RGBA',(800,480))
        # 
        #     padDraw = ImageDraw.Draw(pad)
        # 
        #     padDraw.polygon(xy,fill=(0,0,0,0),outline=(0,255,0,180))
        #     # padDraw.rectangle([x*w_w//c_w,y*w_w//c_w,(x+w)*w_w//c_w,(y+h)*w_w//c_w],fill=(0,0,0,0),outline=(0,255,0,180))
        #     o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)
        # else:
        #     if o:
        #         camera.remove_overlay(o)
        #         o = None
finally:
    if o:
        camera.remove_overlay(o)
    