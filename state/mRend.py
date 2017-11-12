# MasterRenderer

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

from toolbox import matrix
from gfx import rect, shader
from gfx.objreader import model, tmodel, instance
from assets import assets

def init():
    global fontmod
    global blackout
    global col
    col = [0,0,0,0]
    fontmod = tmodel(rect.rmod, assets.font)

def clear():
    global batch
    batch = {}

def black(amt):
    global col
    col[3]=amt

def handle(clear, s):
    if clear:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    shaders.glUseProgram(s)

    try:
        glEnableVertexAttribArray(shader.attrs['pos'])
        glEnableVertexAttribArray(shader.attrs['tex'])
        glUniform4fv(shader.unifs['fog'],1,col)
        glUniform1i(shader.unifs['rentex'],0)
        glActiveTexture(GL_TEXTURE0)
        for model in batch:
            try:
                model.verts.bind()
                model.faces.bind()
                glVertexAttribPointer(shader.attrs['pos'],3,GL_FLOAT,False,12,model.verts)
                model.texs.bind()
                glVertexAttribPointer(shader.attrs['tex'],2,GL_FLOAT,False,8,model.texs)
                for tem in batch[model]:
                    glBindTexture(GL_TEXTURE_2D, tem.tex)
                    for inst in batch[model][tem]:
                        glUniform4fv(shader.unifs['color'],1,inst.col)
                        glUniform2fv(shader.unifs['tscale'],1,inst.tscale)
                        glUniform2fv(shader.unifs['toff'],1,inst.toff)
                        glUniform3fv(shader.unifs['trans'],1,inst.pos)
                        glUniformMatrix3fv(shader.unifs['scale'],1,True,inst.scale)
                        glUniformMatrix3fv(shader.unifs['rot'],1,True,inst.rot)
                        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)
            finally:
                model.faces.unbind()
                model.texs.unbind()
                model.verts.unbind()
    finally:
        glBindTexture(GL_TEXTURE_2D,0)
        glDisableVertexAttribArray(shader.attrs['tex'])
        glDisableVertexAttribArray(shader.attrs['pos'])

def q(mod):
    global batch
    base = mod.tmod.model
    if base not in batch:
        batch[base]={}
    tem = mod.tmod
    if tem not in batch[base]:
        batch[base][tem]=[]
    batch[base][tem].append(mod)

import string

def qtext(x, y, msg, size):
    for i in range(len(msg)):
        let = msg.upper()[i]
        if let not in (string.ascii_uppercase + string.digits + '.,'): continue
        val=0
        if let==',':
            val=1
        elif let>='0' and let<='9':
            val = ord(let) - ord('0')+2
        elif let>='A' and let<='Z':
            val = ord(let) - ord('A')+12
        scale = [1./8.,1./8.]
        offset = [val%8., 7-val//8.]
        linst = instance(fontmod,(x+i*1.5*size,y,0),matrix.size(size,size,size),matrix.id(3),tscale=scale,toff=offset)
        q(linst)
        
