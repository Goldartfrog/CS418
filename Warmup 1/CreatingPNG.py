from PIL import Image
import re
import sys


f = open (sys.argv[1])
print(sys.argv[1])

Lines = f.readlines()
image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
firstline = re.split(' |\t|\n', Lines[0])
if (firstline[0] == "png"):
    image = Image.new("RGBA", (int(firstline[1]), int(firstline[2])), (0, 0, 0, 0))
for line in Lines:
    thisline = re.split(' |\t|\n', line)
    while ("" in thisline):
        thisline.remove("")
    if (thisline):
        if (thisline[0] == "xyrgb"):
            image.im.putpixel((int(thisline[1]), int(thisline[2])), (int(thisline[3]), int(thisline[4]), int(thisline[5]), 255))
        if (thisline[0] == "xyc"):
            color = tuple(int(thisline[3].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
            image.im.putpixel((int(thisline[1]), int(thisline[2])), (color[0], color[1], color[2], 255))
print(firstline[3])
image.save(firstline[3])