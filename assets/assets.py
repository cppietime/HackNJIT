# Assets

from gfx import objreader
from OpenGL.GL import *
import pygame

def init():
    global font, sounds
    font = objreader.loadTex('assets/img/font.png')
    sounds = {'jump': pygame.mixer.Sound('assets/audio/jump.wav'),
              'coin':pygame.mixer.Sound('assets/audio/coin.wav')}
    #loadTG()

def loadTG():
    unload()
    global sprites, bgs
    sprites = {'player':objreader.loadTex('assets/img/player.png'),
               'wall':objreader.loadTex('assets/img/dug.jpg'),
               'coin':objreader.loadTex('assets/img/coin.png'),
               'end':objreader.loadTex('assets/img/end.png')}
    bgs = {'cawk':objreader.loadTex('assets/img/cawk.jpg'),
           'swirl':objreader.loadTex('assets/img/swirl.jpg'),
           'newton':objreader.loadTex('assets/img/newton.jpg'),
           'glay':objreader.loadTex('assets/img/glay.jpg'),
           'brue':objreader.loadTex('assets/img/brue.jpg'),
           'fin':objreader.loadTex('assets/img/fin.jpg')}

def unload():
    global sprites
    if not 'sprites' in globals(): return
    if len(sprites)==0: return
    glDeleteTextures(len(sprites),list(sprites.values()))
