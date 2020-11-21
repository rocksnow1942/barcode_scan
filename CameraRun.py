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
camera.start_preview(fullscreen=False,window=(0,0,320,240)) #
# Add the overlay directly into layer 3 with transparency;
# we can omit the size parameter of add_overlay as the
# size is the same as the camera's resolution
stream = BytesIO()
try:
    # Wait indefinitely until the user terminates the script
    while True:
        time.sleep(1)
        
        # capture and detect
        stream.seek(0)
        camera.capture(stream,format='jpeg',resize=(1200,800))
        stream.seek(0)
        img = Image.open(stream)
        # img = ImageOps.mirror(img)
        
        code = decode(img)
        if code:
            camera.remove_overlay(o)
            code = code[0]
            print(code)
            xy = [ (i.x*4//15,i.y*4//15) for i in code.polygon]
            
            pad = Image.new('RGBA',(800,480))

            padDraw = ImageDraw.Draw(pad)

            padDraw.polygon(xy,fill=(0,0,0,0),outline=(0,255,0,180))
            o = camera.add_overlay(pad.tobytes(),size=pad.size, layer=3)
        else:
            camera.remove_overlay(o)
finally:
    camera.remove_overlay(o)
    pass