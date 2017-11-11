# .obj file reader

from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class model():
    def __init__(self, v, vt, vn, f):
        self.verts=v
        self.texs=vt
        self.norm=vn
        self.faces=f

class tmodel():
    def __init__(self, m, t):
        self.model=m
        self.tex=t

class instance():
    def __init__(tm, p, s, r):
        self.tmod = tm
        self.pos = p
        self.scale = s
        self.rot = r

def readObj(fileName):
    verts = []
    tex = []
    norms = []
    faces = []
    fin = open(fileName,'rb')
    for line in fin:
        if line[0]=='#': continue
        toks = line.lower().split()
        key = toks[0]
        if key=='v':
            val = [float(tok) for tok in toks[1:]]
            verts.append(val)
        elif key=='vt':
            val = [float(tok) for tok in toks[1:]]
            tex.append(val)
        elif key=='vn':
            val = [float(tok) for tok in toks[1:]]
            norms.append(val)
        elif key=='f':
            proc = [tok.split('/') for tok in toks[1:]]
            faces.append(proc)
    fin.close()
    return model(verts,tex,norms,faces)

def loadTex(fileName):
    hasAlpha = fileName[-3:].lower()=='png'
    img = Image.open(fileName)
    imd = np.array(list(img.getData()),np.uint8)
    tex = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glBindTexture(GL_TEXTURE_2D,tex)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA if hasAlpha else GL_RGB, GL_UNSIGNED_BYTE, imd)
    glBindTexture(GL_TEXTURE_2D,0)
    return tex
