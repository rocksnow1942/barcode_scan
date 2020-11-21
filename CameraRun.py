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



pad = Image.new('RGBA',(800,480))

padDraw = ImageDraw.Draw(pad)

padDraw.rectangle([100,100,200,200],fill=(0,0,0,0),outline=(255,0,0,180))


camera = picamera.PiCamera()
camera.resolution = (3200,2400)
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
c_w,c_h = 1200,900

try:
    # Wait indefinitely until the user terminates the script
    while True:
        time.sleep(1)
        
        # capture and detect
        stream.seek(0)
        camera.capture(stream,format='jpeg',resize=(c_w,c_h))
        stream.seek(0)
        img = Image.open(stream)
        # img = ImageOps.mirror(img)
        
        code = decode(img)
        if code:
            if o:
                camera.remove_overlay(o)
            code = code[0]
            print(code.data.decode())
            xy = [ (i.x*w_w//c_w,i.y*w_w//c_w) for i in code.polygon]
            # x,y = code.rect.left,code.rect.top
            # w,h = code.rect.width,code.rect.height
            pad = Image.new('RGBA',(800,480))

            padDraw = ImageDraw.Draw(pad)

            padDraw.polygon(xy,fill=(0,0,0,0),outline=(0,255,0,180))
            # padDraw.rectangle([x,y,x+w,y+h],fill=(0,0,0,0),outline=(0,255,0,180))
            o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)
        else:
            if o:
                camera.remove_overlay(o)
                o = None
finally:
    camera.remove_overlay(o)
    pass