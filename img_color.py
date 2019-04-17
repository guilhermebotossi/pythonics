from PIL import Image
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

for i in range(len(list)):
    for j in range(len(list[0])):
        print list[i][j], 
    print 
    
#im.save('lua_invertida1.jpg')
#(566, 480)