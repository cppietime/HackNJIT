# Pygame handler

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

wSize = (800,600)
keepOpen = True
lft = 0
delta = 0

def sWin():
    pygame.init()
    pygame.mixer.pre_init(44100,16,2,4096)
    pygame.display.set_mode(wSize, DOUBLEBUF|OPENGL)

def run(handle):
    global keepOpen
    global lft
    global delta
    global events
    lft = 0
    while keepOpen:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                endGame()
                break
        handle()
        pygame.display.flip()
        t = pygame.time.get_ticks()
        delta = (t-lft)/1000.
        lft = t
    pygame.display.quit()
    pygame.quit()
    quit()

def endGame():
    global keepOpen
    keepOpen = False
