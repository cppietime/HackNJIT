# Shader

from OpenGL.GL import *
from OpenGL.GL import shaders

def init():
    global shader
    global attrs
    global unifs
    vs = open('gfx/vert.glsl').read()
    fs = open('gfx/frag.glsl').read()
    shadev = shaders.compileShader(vs, GL_VERTEX_SHADER)
    shadef = shaders.compileShader(fs, GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(shadev, shadef)
    unifs = {'trans':glGetUniformLocation(shader,'trans'),
             'rentex':glGetUniformLocation(shader,'rentex'),
             'scale':glGetUniformLocation(shader,'scale'),
             'rot':glGetUniformLocation(shader,'rot'),
             'toff':glGetUniformLocation(shader,'toff'),
             'tscale':glGetUniformLocation(shader,'tscale'),
             'fog':glGetUniformLocation(shader,'fog'),
             'color':glGetUniformLocation(shader,'col')}
    attrs = {'pos':glGetAttribLocation(shader,'pos'),
             'tex':glGetAttribLocation(shader,'tex')}
