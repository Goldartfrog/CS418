from PIL import Image
import re
import sys
import numpy as np
import math

image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
width = 0
height = 0
filename = ""
points = []
tris = []
drawlines = []
usedepth = False
usesRGB = False
usehyp = False
usefrustum = False

class point:
    def __init__(self, vector):
        self.vec = vector
        self.updateValues()
    def updateValues(self):
        self.x = self.vec[0]
        self.y = self.vec[1]
        self.z = self.vec[2]
        self.w = self.vec[3]
        self.r = self.vec[4]
        self.g = self.vec[5]
        self.b = self.vec[6]
    def squareddistancexy(self, point2):
        return (self.x - point2.x)**2 + (self.y - point2.y)
    def DDA(self, point2, d): ## pass in a point and the coordinate which should be integered
        #setup
        a = self.vec
        b = point2.vec
        foundpoints = []
        if(a[d] == b[d]):
            return foundpoints
        if(a[d] > b[d]):
            c = a
            a = b
            b = c
        delta = np.subtract(b, a)
        s = delta / delta[d]
        #find first potential point
        e = math.ceil(a[d]) - a[d]
        o = e * s
        p = a + o
        while(p[d] < b[d]):
            foundpoints.append(point(p))
            p = p + s
        return foundpoints
    def convertToW(self):
        self.vec = self.vec / self.w
        self.vec[3] = 1 / self.w
        self.updateValues()
        return self
    def viewportTransform(self):
        self.vec[0] = (self.x + 1) * width / 2
        self.vec[1] = (self.y + 1) * height / 2
        self.vec[2] = (self.z + 1) / 2
        self.updateValues()
        return self
    def convertFromW(self):
        self.vec = self.vec / self.w
        self.vec[0] = self.x
        self.vec[1] = self.y
        self.vec[2] = self.z
        self.vec[3] = 1/self.w
        self.updateValues()
        return self
    def changeValue(self, index, value):
        self.vec[index] = value
        self.updateValues()
        return self
    def checkInside(self):
        xyzw = self.vec[0:4]
        frustummatrix = np.array([[1, 0, 0, 1], 
                                  [-1, 0, 0, 1], 
                                  [0, 1, 0, 1], 
                                  [0, -1, 0, 1], 
                                  [0, 0, 1, 1], 
                                  [0, 0, -1, 1]])
        check = frustummatrix.dot(xyzw)
        return check




class tri:
    def __init__(self, index1, index2, index3):
        self.verticies = [index1, index2, index3]


class pixelline:
    def __init__(self, index1, index2):
        self.verticies = [index1, index2]

def displayToStorage(color):
    display = color
    if (display <= 0.0031308):
        return 12.92*display
    else:
        return ((display**(1/2.4)*1.055) - 0.055)
def storageToDisplay(color):
    storage = color
    if (storage <= 0.04045):
        return (storage/12.92)
    else:
        return (((storage + 0.055)/1.055)**2.4)


def drawTriangle(point1, point2, point3):
    storepoints = []
    line1 = point1.DDA(point2, 1)
    line2 = point2.DDA(point3, 1)
    line3 = point1.DDA(point3, 1)
    lines = [line1, line2, line3]
    lines = sorted(lines, key = lambda line : len(line))
    other2 = np.concatenate((lines[0], lines[1]))
    other2 = sorted(other2, key = lambda p : p.y)
    for i, side in enumerate(lines[2]):
        thing = side.DDA(other2[i], 0)
        for l in thing:
            storepoints.append(l)
    return storepoints

def readFile():
    f = open (sys.argv[1])
    currentcolor = (255, 255, 255)
    Lines = f.readlines()
    
    for line in Lines:
        thisline = re.split(' |\t|\n', line)
        while ("" in thisline):
            thisline.remove("")
        if (thisline):
            if (thisline[0] == "png"):
                global width, height, filename
                width = int(thisline[1])
                height = int(thisline[2])
                filename = thisline[3]
                global image
                image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            if (thisline[0] == "depth"):
                global usedepth
                usedepth = True
            if (thisline[0] == "sRGB"):
                global usesRGB
                usesRGB = True
            if (thisline[0] == "hyp"):
                global usehyp
                usehyp = True
            if (thisline[0] == "frustum"):
                global usefrustum
                usefrustum = True
            if(thisline[0] == "xyzw"):
                toappend = []
                if (usesRGB):
                    toappend = np.array([float(thisline[1]), float(thisline[2]), float(thisline[3]), float(thisline[4]), 
                                        storageToDisplay(int(currentcolor[0])/255), 
                                        storageToDisplay(int(currentcolor[1])/255), 
                                        storageToDisplay(int(currentcolor[2])/255)])
                else:
                    toappend = np.array([float(thisline[1]), float(thisline[2]), float(thisline[3]), float(thisline[4]), 
                                        int(currentcolor[0]), 
                                        int(currentcolor[1]), 
                                        int(currentcolor[2])])
                points.append(point(toappend))
            if(thisline[0] == "rgb"):
                currentcolor = (thisline[1], thisline[2], thisline[3])
            if(thisline[0] == "tri"):
                indicies = []
                for word in thisline[1:]:
                    if int(word) > 0:
                        indicies.append(int(word) - 1)
                    if int(word) < 0:
                        indicies.append(len(points) + int(word))

                tris.append(tri(indicies[0], indicies[1], indicies[2]))
            if (thisline[0] == "line"):
                lineends = []
                for word in thisline[1:]:
                    if int(word) > 0:
                        lineends.append(int(word) - 1)
                    if int(word) < 0:
                        lineends.append(len(points) + int(word))
                drawlines.append(pixelline(lineends[0], lineends[1]))

def render():
    inside = []
    if (tris):
        for t in tris:
            if (not usefrustum):
                point1 = point(points[t.verticies[0]].vec).convertToW().viewportTransform()
                point2 = point(points[t.verticies[1]].vec).convertToW().viewportTransform()
                point3 = point(points[t.verticies[2]].vec).convertToW().viewportTransform()
                if (not usehyp):
                    point1.convertFromW()
                    point2.convertFromW()
                    point3.convertFromW()
                inside = np.concatenate((inside, drawTriangle(point1, point2, point3)))
            # else:
            #     point1 = point(points[t.verticies[0]].vec)
            #     point2 = point(points[t.verticies[1]].vec)
            #     point3 = point(points[t.verticies[2]].vec)
            #     pointstocheck = [point1, point2, point3]
            #     todiscard = []
            #     for poin in pointstocheck:
            #         dis = poin.checkInside()
            #         dodis = False
            #         for num in dis:
            #             if (num < 0):
            #                 dodis = True
            #         if(dodis == True):
            #             todiscard.append(poin)
            #     while(len(todiscard != 0)):
            #         for d in todiscard:
            #             pointstocheck.remove(d)
            #             for poin in pointstocheck:
            #                 one = d.checkInside()
            #                 two = poin.checkInside()
            #                 dim = 0
            #                 for i in len(one):
            #                     if (one[i] < 0):
            #                         dim = i
                            
                
                    

    if(drawlines):
        for l in drawlines:
            point1 = point(points[l.verticies[0]].vec).convertToW().viewportTransform()
            point2 = point(points[l.verticies[1]].vec).convertToW().viewportTransform()
            if (not usehyp):
                point1.convertFromW()
                point2.convertFromW()
            theline = 0
            if (abs(point1.x - point2.x) - abs(point1.y - point2.y) > 0):
                theline = point1.DDA(point2, 0)
                for po in theline:
                    po.changeValue(1, round(po.vec[1]))
                    inside.append(po)
            else:
                theline = point1.DDA(point2, 1)
                for po in theline:
                    po.changeValue(0, round(po.vec[0]))
                    inside.append(po)
        
    depth = {}
    for p in inside:
        pixX = int(p.x)
        pixY = int(p.y)
        toDraw = False
        if (usedepth):
            if (p.z > -1):
                if ((pixX, pixY) in depth):
                    if (p.z < depth[(pixX, pixY)]):
                        toDraw = True
                else:
                    depth[(pixX, pixY)] = p.z
                    toDraw = True
        else:
            toDraw = True
        
        if(usehyp):
            p.convertFromW()
        

        if (pixX < width and pixX >= 0 and pixY < height and pixY >= 0 and toDraw):
            if (usesRGB):
                image.im.putpixel((pixX, pixY), (int(displayToStorage(p.r)*255), 
                                                int(displayToStorage(p.g)*255), 
                                                int(displayToStorage(p.b)*255), 255))
            else:
                image.im.putpixel((pixX, pixY), (int(p.r), 
                                                int(p.g), 
                                                int(p.b), 255))
    image.save(filename)

if __name__ == '__main__':
    readFile()
    render()

