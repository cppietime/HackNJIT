# 2D game state

from gfx import rect, objreader, shader, pgame
from gfx.objreader import tmodel, instance
from toolbox import matrix
from assets import assets
from state import mRend

from OpenGL.GL import shaders
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import copy
import math

FLOOR = -1
BUFF = .006
level = 0
wide = 2
high = 2
nState = None
cScore = 0

class obect():
    def __init__(self,tex,size,pos,vel=[0,0,0],sol=False):
        self.pos = [pos[0],pos[1],0]
        self.scale = size
        self.model = tmodel(rect.rmod, tex)
        self.vel=copy.deepcopy(vel)
        self.solid=sol
        self.flagged=False

    def delet(self):
        self.flagged=True

    def translate(self, offset):
        self.pos = [self.pos[i] + offset[i] for i in range(len(self.pos))]
        return self

    def getInst(self):
        return instance(self.model, self.pos, self.scale, matrix.id(3))

    def update(self):
        if tuple(self.vel)==(0,0,0): return
        for i in range(2):
            if self.vel[i]==0:continue
            if inAir(self,i,self.vel[i]/abs(self.vel[i])):
                self.pos[i]+=self.vel[i]*pgame.delta
            else:
                self.vel[i]=0

    def hitbox(self):
        return (self.pos[0], self.pos[1], self.scale[0], self.scale[4])

class gobj(obect):
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        super().update()
        if inAir(self,1,-1):
            self.vel[1]-=5.25*pgame.delta
        else:
            self.vel[1]=0
        while not inAir(self,0,1) and not inAir(self,0,-1):
            self.pos[1]+=BUFF/2

VMAX = 1.5
ACC = 10
class player(gobj):
    def __init__(self,pos):
        super().__init__(assets.sprites['player'],matrix.scale(matrix.id(3),.1), pos)
        self.frame=0
        self.delt = 0
        self.tscale = [.25,.5]
    
    def update(self):
        super().update()
        self.delt += pgame.delta
        if self.delt >= .2:
            self.frame += 1
            self.frame %= 2
            self.delt -= .2
        if keys[pygame.K_LEFT]:
            pl.vel[0]-=ACC*pgame.delta
            if pl.vel[0]<-VMAX: pl.vel[0]=-VMAX
        elif keys[pygame.K_RIGHT]:
            pl.vel[0]+=ACC*pgame.delta
            if pl.vel[0]>VMAX: pl.vel[0]=VMAX
        else:
            if pl.vel[0]>0:
                pl.vel[0]-=ACC*pgame.delta
            elif pl.vel[0]<0:
                pl.vel[0]+=ACC*pgame.delta
            if abs(pl.vel[0])<=VMAX/6:
                pl.vel[0]=0

        if keys[pygame.K_UP]:
            if not inAir(self,1,-1):
                pygame.mixer.Sound.play(assets.sounds['jump'])
                pl.vel[1]=1.8

    def getInst(self):
        escale = copy.deepcopy(self.scale)
        if self.vel[0]<0: escale[0] *= -1
        toff = [0,1]
        v1=2
        if self.vel[0]==0:
            v1 = 0
        if self.vel[1]==0:
            toff[0] = self.frame+v1
        elif self.vel[1]>0:
            toff = [v1,0]
        else:
            toff = [v1+1,0]
        return instance(self.model, self.pos, escale, matrix.id(3), toff=toff, tscale=self.tscale)

    def hitbox(self):
        return(self.pos[0], self.pos[1], self.scale[0]*.65, self.scale[4]*.91)

class coin(obect):
    def __init__(self, *args):
        super().__init__(*args)
        self.frame=0
        self.delt=0

    def update(self):
        global score
        self.delt+=pgame.delta
        if self.delt>=.2:
            self.frame+=1
            self.frame%=2
            self.delt-=.2
        super().update()
        if boxesOverlap(self.hitbox(),pl.hitbox(),(BUFF,BUFF)) and not self.flagged:
            self.delet()
            score += 1
            pygame.mixer.Sound.play(assets.sounds['coin'])

    def hitbox(self):
        return(self.pos[0],self.pos[1],self.scale[0]*.55,self.scale[4])

    def getInst(self):
        return instance(self.model, self.pos, self.scale, matrix.id(3), tscale=(.5,1.), toff=(self.frame, 0),c=[1,1,0,1])

class end(obect):
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        global btime, target, paused
        super().update()
        if boxesOverlap(self.hitbox(),pl.hitbox(),(BUFF,BUFF)) and not self.flagged:
            self.delet()
            btime=1
            target=level+1
            paused = True

class mPlat(obect):
    def __init__(self, *args, d=[0,0,0], time=1):
        super().__init__(*args, sol=True)
        self.d=copy.deepcopy(d)
        self.time=time
        self.delt=0
        self.cPos = self.pos

    def update(self):
        super().update()
        self.delt+=pgame.delta
        self.delt%=self.time
        dis = (self.delt%self.time)/self.time
        if self.delt >= self.time/2.:
            dis = 1-dis
        self.cPos = [self.pos[i] + self.d[i] * dis * 2 for i in range(len(self.pos))]

    def hitbox(self):
        return (self.cPos[0], self.cPos[1], self.scale[0], self.scale[4])

    def getInst(self):
        return instance(self.model, self.cPos, self.scale, matrix.id(3))
    

def boxesOverlap(h1, h2, buffer):
    hdist = abs(h1[0]-h2[0])
    vdist = abs(h1[1]-h2[1])
    return hdist<abs(h1[2])+abs(h2[2])+buffer[0] and vdist<abs(h1[3])+abs(h2[3])+buffer[1]

def inAir(obj,axis,sign):
    nbox = copy.deepcopy(list(obj.hitbox()))
    nbox[axis] += sign*nbox[axis+2]
    nbox[axis+2] = 0
    nbox[3-(axis)] -= 2*BUFF
    for o in objs:
        if o==obj:
            continue
        if boxesOverlap(nbox, o.hitbox(), (BUFF,BUFF)):
            return False
    return nbox[axis] >= -[wide,high][axis] and nbox[axis] <= [wide,high][axis]

def onChange():
    global active
    assets.loadTG()
    glLoadIdentity()
    gluOrtho2D(-1,1,-1,1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    active = True
    if 'initd' not in globals():
        init()

def onLeave():
    global active
    active = False

def init():
    global active, black, initd, objs, bgs, score, paused, btime, ttime, target, nex, cMus
    cMus = None
    nex = False
    target = 0
    btime = 0
    ttime = 0
    paused = True
    score = 0
    active = True
    initd = True
    objs = []
    bgs = []
    '''pl = player((0,.1))
    flr = object(assets.sprites['player'],matrix.size(1,.2,1),(0,-.5),sol=True)
    bg = object(assets.sprites['player'],matrix.size(2,2,2),(0,0))
    bgs.append(bg)
    objs.append(flr)'''
    loadLevel('level.lvl')
    #pygame.mixer.music.load('assets/audio/diamonddust.wav')
    #pygame.mixer.music.play(-1)
    paused = False
    black = instance(tmodel(rect.rmod,assets.sprites['wall']),(0,0),matrix.size(1,1,1),matrix.id(3),c=[.1,.1,.1,1])

from os import path

def loadLevel(level):
    global pl, objs, bgs, wide, high, cMus, score
    score = cScore
    objs=[]
    bgs=[]
    if not path.exists(level):
        loadLevel("fin.lvl")
        return
    fin = open(level)
    lines = fin.readlines();
    [wide, high] = [float(i) for i in lines[0].split()]
    #black = instance(tmodel(rect.rmod, assets.sprites['wall']), p=(0,0), s=matrix.size(wide, high,1), r=matrix.id(3), c=[.2,.2,.2,1])
    pl = player([float(i) for i in lines[1].split()])
    for line in lines[1:]:
        ws = line.split()
        o = None
        if ws[0].lower()=='w':
            toks = [float(i) for i in ws[1:]]
            o = obect(assets.sprites['wall'],matrix.size(toks[2],toks[3],1),toks[0:2],sol=True)
        elif ws[0].lower()=='c':
            toks = [float(i) for i in ws[1:]]
            o = coin(assets.sprites['coin'], matrix.size(.025,.025,1),toks)
        elif ws[0].lower()=='e':
            toks = [float(i) for i in ws[1:]]
            o = end(assets.sprites['end'], matrix.size(.06, .06,1),toks)
        elif ws[0].lower()=='b':
            bgs.append(obect(assets.bgs[ws[1]], matrix.size(wide,high,1), (0,0)))
        elif ws[0].lower()=='m':
            if ws[1].lower() != cMus:
                cMus = ws[1].lower()
                pygame.mixer.music.load(cMus)
                pygame.mixer.music.play(-1)
        elif ws[0].lower()=='p':
            toks = [float(i) for i in ws[1:]]
            o = mPlat(assets.sprites['wall'],matrix.size(toks[2],toks[3],1),toks[0:2],d=toks[4:7],time=toks[7])
        if o!=None:
            objs.append(o)

def handle():
    if not active:
        return
    global keys, objs, ttime, btime, level, target, nex, paused, cScore
    if nex:
        cScore = score
        loadLevel('level'+str(level)+'.lvl')
        nex = False
        target = 0
        paused = False
    for event in pgame.events:
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                paused = not paused
            elif event.key==pygame.K_r:
                loadLevel('level'+str(level)+'.lvl')
    keys = pygame.key.get_pressed()
    if not paused:
        pl.update()
        for o in objs:
            o.update()
        dels = [o for o in objs if o.flagged==True]
        objs = [o for o in objs if not o in dels]
        for d in dels:
            del(d)
        del(dels)
    '''if btime != 0:
        ttime += pgame.delta
        mRend.black(math.sin(ttime*math.pi/btime/2.))
        if ttime >= btime:
            ttime = 0
            btime = 0
            mRend.black(0.)
            if target != 0:
                level = target
                target = 0
                nex = True'''
    x,y = 0,0
    if pl.pos[0] <= 1-wide:
        x = wide-1
    elif pl.pos[0] >= wide-1:
        x = 1-wide
    else:
        x = -pl.pos[0]
    if pl.pos[1] <= 1-high:
        y = high-1
    elif pl.pos[1] >= high-1:
        y = 1-high
    else:
        y = -pl.pos[1]
    glPushMatrix()
    glTranslatef(x,y,0)
    mRend.clear()
    for o in bgs:
        mRend.q(o.getInst())
    mRend.handle(True,shader.shader)
    mRend.clear()
    for o in objs:
        mRend.q(o.getInst())
    mRend.handle(False,shader.shader)
    mRend.clear()
    mRend.q(pl.getInst())
    mRend.handle(False,shader.shader)
    mRend.clear()
    glPopMatrix()
    mRend.qtext(-.9,-.9,"Score"+str(score),.03)
    mRend.handle(False,shader.shader)
    if paused and target==0:
        mRend.clear()
        mRend.qtext(-.5,-.5,"Paused",.05)
        mRend.handle(False,shader.shader)
        del(dels)
    mRend.clear()
    if btime != 0:
        ttime += pgame.delta
        black.col[3]=(math.sin(ttime*math.pi/btime/2.))
        if ttime >= btime:
            ttime = 0
            btime = 0
            black.col[3]=(0.)
            if target != 0:
                level = target
                target = 0
                nex = True
        mRend.q(black)
        mRend.handle(False,shader.shader)
    
