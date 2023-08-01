import shaders
from gl import Renderer, V2, color

width = 1000
height = 1000

rend = Renderer(width,height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel(filename="model.obj",textureName="model.bmp",translate=(400,height/2,0),rotate=(180,0,90),scale=(200,200,200))
rend.glLoadModel(filename="model.obj",textureName="model.bmp",translate=(3*width/4,height/4,0),rotate=(180,0,180),scale=(200,200,200))
rend.glLoadModel(filename="model.obj",textureName="model.bmp",translate=(1*width/4,height/4,0),rotate=(270,0,270),scale=(200,200,200))
rend.glLoadModel(filename="model.obj",textureName="model.bmp",translate=(2*width/4,height/4,0),rotate=(90,0,270),scale=(200,200,200))



rend.glRender()


rend.glFinish("output.bmp")