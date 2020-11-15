# import qrcode

# # img = qrcode.make('test text')


# from barcode import EAN13,Code128,UPCA

# c128 = Code128('AB123ab')

# c128.save('128.png')



from pylibdmtx.pylibdmtx import decode,encode
from PIL import Image
import random

for i in range(96):
    d = f"{int(random.random()* (10**10)):010}"
    print(d)
    text = d
    dm = encode(text.encode(),scheme='AutoBest',size='12x12')
    # print(dm)
    img = Image.frombytes('RGB',(dm.width,dm.height),dm.pixels)
    img.save(f"./96DM/{text}.png")

