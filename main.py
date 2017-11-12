# Main

import pygame
import threading
import OpenGL
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *

from gfx import pgame, objreader, rect, shader
from gfx.objreader import model, tmodel, instance
from toolbox import matrix
from state import mRend, tgstate, openmenu
from assets import assets

def handle():
    if 'cstate' in globals():
        if cstate != None:
            cstate.handle()
            if cstate.nState != None and cstate.nState != cstate:
                print('we good')
                changeState(cstate.nState)

def init():
    assets.init()
    mRend.init()
    global cstate
    cstate = None
    shader.init()
    gluPerspective(45,8./6.,.1,50)
    glTranslatef(0.,0.,-5)
    changeState(openmenu)

def main():
    pgame.sWin()
    pygame.display.set_caption('Hack and Plat')
    init()
    pygame.time.wait(2000)
    pgame.run(handle)

def changeState(stt):
    global cstate
    cstate = stt
    stt.onChange()

main()
