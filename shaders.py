import ml

import random

def vertexShader(vertex,**kwargs):
    modelMatrix = kwargs["modelMatrix"]
    vt = [vertex[0],vertex[1],vertex[2],1]

    vt = modelMatrix @ vt
    vt = vt.tolist()[0]
    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]
    return vt

def fragmentShader(**kwargs):
    textCoords = kwargs["textCoords"]
    texture = kwargs["texture"]

    if texture !=None:
        color = texture.getColor(textCoords[0],textCoords[1])
    else:
        color = (1,1,1)
    return color