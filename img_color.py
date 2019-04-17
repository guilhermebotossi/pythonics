from PIL import Image, ImageDraw, ImageFont
from struct import pack
file = "lua.jpg"
im = Image.open(file)
pix = im.load()
size = im.size
#print (size)  
black = (0, 0, 0)
w = size[1]
h = size[0]
list = [[0] * h for i in range(w)]
#print len(list), len(list[0])
for i in range(w - 1):
    for j in range(h - 1):
        #print i, j
        if pix[j,i] == black :
            list[i][j] = 0
        else:
            list[i][j] = 1

text = ""
for i in range(len(list)):
    for j in range(len(list[0])):
        #print list[i][j],
        text += str(list[i][j]) + " "
    text += "\n"
    #print 
    
#print text    
img = Image.new('RGB', (w * 5, h * 5), color = (255, 255, 255))
d = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 5)
d.text((1,1), text, fill=(0, 0, 0), font = font)
img.save('pil.png')
#(566, 480)