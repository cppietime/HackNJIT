# Opening menu

from OpenGL.GL import *
from OpenGL.GLU import *
from gfx import pgame, shader
from state import tgstate, mRend

nState = None

def onChange():
    glLoadIdentity()
    gluOrtho2D(-1,1,-1,1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

def handle():
    global nState
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    mRend.clear()
    mRend.qtext(-.95,.8,"Hack and Plat 2017",.07)
    mRend.qtext(-.95,.6,"Developed for HackNJIT 2017 by Yaakov Schectman",.028)
    mRend.qtext(-.9,.4,"Collect all the rare pepes",.05)
    mRend.qtext(-.9,.2,"Arrow keys to move",.04)
    mRend.qtext(-.9,0,"Press Space to begin",.04)
    mRend.qtext(-.96,-.2,"Collect Kekels for hi score",.04)
    mRend.qtext(-.96,-.4,"Press R to restart a level,",.04)
    mRend.qtext(-.9,-.6,"But lose your kekels from the level",.03)
    mRend.handle(True,shader.shader)
    for event in pgame.events:
        if event.type==pgame.KEYDOWN and event.key==pgame.K_SPACE:
            print('good we aer')
            nState = tgstate
