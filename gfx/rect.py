# Basic Rectangle model

import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import *
from gfx.objreader import model

verts = vbo.VBO(np.array([
    [-1,-1,0],
    [1,-1,0],
    [1,1,0],
    [-1,1,0]],'f'))

tex = vbo.VBO(np.array([
    [0,0],
    [1,0],
    [1,1],
    [0,1]],'f'))

inds = vbo.VBO(np.array([[0,1,2, 0,2,3]],dtype=np.int32),target=GL_ELEMENT_ARRAY_BUFFER)

rmod = model(verts, tex, None, inds)
