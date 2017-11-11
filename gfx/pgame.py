# Pygame handler

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

wSize = (800,600)
keepOpen = True

def sWin():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

def run(handle):
    while keepOpen:
        handle()
