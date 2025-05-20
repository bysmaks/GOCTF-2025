from PIL import Image
from random import randint
from math import ceil
image1 = Image.open("Лёлик.png")
x, y = image1.size
res = Image.new('RGB', (x, y))
pix = res.load()
res = ''
for i in range(y):
    for j in range(x):
        p1 = image1.getpixel((j, i))
        p1 = [bin(x)[2:] for x in p1]
        res += p1[0][-3]
        res += p1[1][-1]
        res += p1[2][-2]
        if len(res) > 300:
            break
now_sim = ''
for i in res:
    now_sim += i
    if len(now_sim) == 8:
        print(chr(int(now_sim, 2)), end='')
        now_sim = ''
