import sys
from pylibdmtx.pylibdmtx import decode
from PIL import Image 


def decode_panel(panel):
    px,py = panel.size
    for size in [100,200]:
        
        panel_resize = panel.resize((size, int(size*py/px)))
        res = decode(panel_resize,max_count=1)
        if res:
            return res[0].data
    return "Not decoded."

if __name__=='__main__':
    for row in 'ABCDEFGH':
        for col in range(1,13):
            file = f"./out/{row}{col}.jpeg"
            img = Image.open(file)
            res = decode_panel(img,max_count=1)
            print(f"{row}{col}: {res}")