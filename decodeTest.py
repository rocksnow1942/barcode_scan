from pylibdmtx.pylibdmtx import decode
from PIL import Image 

file = './1.jpeg'
img = Image.open(file)
res = decode(
img,
timeout = 10000,
gap_size=None,
shrink = 1,
shape = None,
deviation = 5,
threshold = 100,
min_edge=None,
max_edge = None,
corrections=None,
max_count = 96
)

for i in res:
    print(i)