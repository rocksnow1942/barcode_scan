from PIL import Image,ImageOps,ImageDraw,ImagePath

img = Image.open('out.png')

img.show()

xy = [(10,20),(50,20),(50,50),(10,50)]

img1 = ImageDraw.Draw(img)

img1.polygon(xy,fill=(0,0,0,0),outline='red')

img.show()





# image overlay
img = Image.open('out.png')
pad = Image.new('RGBA',(
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))
        
pad.paste(img, (0, 0),img)
o = camera.add_overlay(pad.tobytes(),size=img.size, layer=3)