import pygame as pg
from math import sqrt
pg.init()

SCREENSIZE = 500
screen = pg.display.set_mode((SCREENSIZE, SCREENSIZE))
pg.display.set_caption('Red Circles Redemption')

backcolor = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
RADIUS = 25
SIZE = 50

class Circle:

    def __init__(self, c, r, loc, s):
        self.color = c
        self.radius = r
        self.location = loc
        self.speed = s

    def draw(self):
        pg.draw.circle(screen, self.color, (self.location), self.radius)

    def getDistance(self, target):
        return sqrt((self.location[0] - target.location[0])**2 + (self.location[1] - target.location[1])**2)

    def checkBorders(self, _screensize):
        if self.location[0] - self.radius < 0:
            self.location[0] = self.radius
        if self.location[0] + self.radius > _screensize:
            self.location[0] = _screensize - self.radius
        if self.location[1] - self.radius < 0:
            self.location[1] = self.radius
        if self.location[1] + self.radius > _screensize:
            self.location[1] = _screensize - self.radius

class Protagonist(Circle):
    def __init__(self, c, r, loc, s):
        super().__init__(c, r, loc, s)

    def move(self, dir):
        if(dir == 'north'):
            self.location[1] -= self.speed
        if(dir == 'south'):
            self.location[1] += self.speed
        if(dir == 'west'):
            self.location[0] -= self.speed
        if(dir == 'east'):
            self.location[0] += self.speed


class Enemy(Circle):

    def __init__(self, c, r, loc, s):
        super().__init__(c, r, loc, s)

    def charge(self, target):
        self.location[0] += (target.location[0] - self.location[0]) * self.speed / self.getDistance(target)
        self.location[1] += (target.location[1] - self.location[1]) * self.speed / self.getDistance(target)

class Safehouse:

    def __init__(self, c, s, loc):
        self.color = c
        self.size = s
        self.location = loc

    def draw(self):
        pg.draw.rect(screen, self.color,
        (self.location[0] - SIZE/2, self.location[0] - SIZE/2,
        self.location[1] + SIZE/2, self.location[1] + SIZE/2))

def isWin(_p, _s):
    return _s.location[0] - _s.size/2 < _p.location[0] < _s.location[0] + _s.size/2 and _s.location[1] - _s.size/2 < _p.location[1] < _s.location[1] + _s.size/2

def isLose(_p, _e):
    for el in _e:
        if el.getDistance(_p) <= el.radius + _p.radius:
            return True
    return False

p = Protagonist(YELLOW, RADIUS, [350, 350], 0.015)
enemies = []
enemies.append(Enemy(RED, RADIUS, [100, 100], 0.01))
enemies.append(Enemy(RED, RADIUS, [200, 100], 0.01))
enemies.append(Enemy(RED, RADIUS, [300, 100], 0.01))
sh = Safehouse(GREEN, SIZE, [SIZE/2, SIZE/2])

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if isWin(p, sh):
        running = False

    if isLose(p, enemies):
        running = False

    if pg.key.get_pressed()[pg.K_w]:
        p.move('north')
    if pg.key.get_pressed()[pg.K_s]:
        p.move('south')
    if pg.key.get_pressed()[pg.K_a]:
        p.move('west')
    if pg.key.get_pressed()[pg.K_d]:
        p.move('east')
    for en in enemies:
        en.charge(p)

    screen.fill(backcolor)
    p.checkBorders(SCREENSIZE)
    for el in enemies:
        el.checkBorders(SCREENSIZE)
    p.draw()
    sh.draw()
    for en in enemies:
        en.draw()
    pg.display.flip()
