import struct
from collections import namedtuple
import numpy as np

from obj import Obj

V2 = namedtuple('Point2',['x','y'])
V3 = namedtuple('Point2',['x','y','z'])

#Primitivas
POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

def char(c):
    #1 byte
    return struct.pack('=c',c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h',w)

def dword(d):
    #4 bytes
    return struct.pack('=l',d)

def color(r,g,b):
    return bytes([int(b*255),int(g*255),int(r*255)])

class Model(object):
    def __init__(self,filename,translate=(0,0,0),rotate=(0,0,0),scale=(1,1,1)):
        model = Obj(filename)

        self.vertices = model.vertices
        self.texcoords = model.textcoords
        self.normals = model.normals
        self.faces = model.faces

        self.translate = translate
        self.rotate = rotate
        self.scale = scale

class Renderer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.glClearColor(0,0,0)
        self.glClear()

        self.glColor(1,1,1)

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None

        self.primitiveType = TRIANGLES
        self.vertexBuffer = []

    def glAddVertices(self,verts,):
        for vert in verts:
            self.vertexBuffer.append(vert)

    def glPrimitiveAssembly(self,tVerts):
        primitives = []
        if self.primitiveType==TRIANGLES:
            for i in range(0,len(tVerts),3):
                triangle = []
                triangle.append(tVerts[i])
                triangle.append(tVerts[i+1])
                triangle.append(tVerts[i+2])
                primitives.append(triangle)

        return primitives

    def glClearColor(self,r,g,b):
        self.clearColor = color(r,g,b)

    def glColor(self,r,g,b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

    def glPoint(self,x,y,clr=None):
        if 0<=x<self.width and 0<=y<self.height:
            self.pixels[x][y] = clr or self.currColor

    def glTriangle(self,v0,v1,v2,clr=None):
        self.glLine(v0,v1,clr or self.currColor)
        self.glLine(v1,v2,clr or self.currColor)
        self.glLine(v2,v0,clr or self.currColor)

    def glModelMatrix(self,translate=(0,0,0),scale=(1,1,1)):
        translation = np.matrix([[1,0,0,translate[0]],
                                 [0,1,0,translate[1]],
                                 [0,0,1,translate[2]],
                                 [0,0,0,1]])
        scaleMat = np.matrix([[scale[0],0,0,0],
                                 [0,scale[1],0,0],
                                 [0,0,scale[2],0],
                                 [0,0,0,1]])

        return translation*scaleMat

    def glLine(self,v0,v1,clr=None):
        #Bresenham line algorithm
        #y = mx+b
        #m =(v1.y-v0.y)/(v1.x-v0.x)
        #y = v0.y

        #for x in range(v0.x,v1.x+1):
            #self.glPoint(x,int(y))
            #y += m

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        #Si el punto 0 es igual al punto 1, solo dibuja un punto
        if x0==x1 and y0==y1:
            self.glPoint(x0,y0)
            return

        dy = abs(y1-y0)
        dx = abs(x1-x0)

        steep = dy>dx

        #Si la linea tiene pendiente mayor a 1 o menor a -1
        #intercambiamos las x por las y, y se dibuja la linea
        #de manera vertical en lugar de horizontal
        if steep:
            x0,y0=y0,x0
            x1,y1=y1,x1

        #Si el punto inicial en x es mayor que el punto final en x,
        #intercambiamos los puntos para siempre dibujar de
        #izquierda a derecha
        if x0>x1:
            x0,x1=x1,x0
            y0,y1=y1,y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset=0
        limit=0.5
        m=dy/dx
        y=y0

        for x in range(x0,x1+1):
            if steep:
                #Dibujar de manera vertical
                self.glPoint(y,x,clr or self.currColor)
            else:
                #Dibujar de manera horizontal
                self.glPoint(x,y,clr or self.currColor)

            offset+=m
            if offset>=limit:
                if y0<y1:
                    y+=1
                else:
                    y-=1

                limit+=1

    def glLoadModel(self,filename,translate=(0,0,0),rotate=(0,0,0),scale=(1,1,1)):
        self.objects.append(Model(filename,translate,rotate,scale))


    def glRender(self):
        transformedVerts = []

        for model in self.objects:
            mMat = self.glModelMatrix(model.translate,model.scale)

            for face in model.faces:
                vertCount = len(face)
                v0 = model.vertices[face[0][0]-1]
                v1 = model.vertices[face[1][0]-1]
                v2 = model.vertices[face[2][0]-1]

                if vertCount == 4:
                    v3 = model.vertices[face[3][0]-1]

                if self.vertexShader:
                    v0 = self.vertexShader(v0,modelMatrix=mMat)
                    v1 = self.vertexShader(v1, modelMatrix=mMat)
                    v2 = self.vertexShader(v2, modelMatrix=mMat)

                    if vertCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix=mMat)

                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if vertCount==4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)

        #for vert in self.vertexBuffer:
        #    if self.vertexShader:
        #        transformedVerts.append(self.vertexShader(vert, modelMatrix=self.modelMatrix))
        #    else:
        #        transformedVerts.append(vert)

        primitives = self.glPrimitiveAssembly(transformedVerts)

        primColor = None
        if self.fragmentShader:
            primColor = self.fragmentShader()
            primColor = color(primColor[0],primColor[1],primColor[2])
        else:
            primColor = self.currColor

        # Rasterizando las primitivas
        for prim in primitives:
            if self.primitiveType==TRIANGLES:
                self.glTriangle(prim[0],prim[1],prim[2],primColor)

    def glPolygon(self, vertices, clr=None):
        num_vertices = len(vertices)

        # Calculate the bounding box of the polygon
        min_x, min_y = max_x, max_y = vertices[0]
        for x, y in vertices:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        # Convert the color to the expected format (b, g, r)
        color_byte = clr or self.currColor
        b, g, r = color_byte

        # Loop through each row in the bounding box
        for y in range(min_y, max_y + 1):
            intersections = []

            # Loop through each edge of the polygon
            for i in range(num_vertices):
                j = (i + 1) % num_vertices
                v0 = vertices[i]
                v1 = vertices[j]

                # Check if the edge intersects with the current row (y)
                if v0[1] < y and v1[1] >= y or v1[1] < y and v0[1] >= y:
                    x_intersection = v0[0] + (y - v0[1]) / (v1[1] - v0[1]) * (v1[0] - v0[0])
                    intersections.append(x_intersection)

            # Sort the intersection points
            intersections.sort()

            # Fill the pixels between pairs of intersections
            for i in range(0, len(intersections), 2):
                x_start = int(intersections[i])
                x_end = min(int(intersections[i + 1]), max_x)

                # Fill the row with the specified color
                for x in range(x_start, x_end + 1):
                    self.glPoint(x, y, (b, g, r))


    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    # Convert color tuple to bytes and write to file
                    file.write(bytes(self.pixels[x][y]))