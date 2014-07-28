from world import *
from player import *
from viewer import *
from genetic import *
from represent import *
from numpy import rot90
import cPickle as pk

w = World()
p1 = Player(10,10)
p2 = Player(20,10)
w.addPlayer(p1)
w.addPlayer(p2)


def movePlayer(pos, player, rot=False):
    if rot:
        DOWN,UP,RIGHT,LEFT = range(4)
    else:
        UP,DOWN,LEFT,RIGHT = range(4)
    if pos.move == UP:
        player.moveUp()
    elif pos.move == DOWN:
        player.moveDown()
    elif pos.move == RIGHT:
        player.moveRight()
    else:
        player.moveLeft()

def doif(pos, player, rot=False):
    pview = w.getPlayerView(player)
    if rot:
        pview = rot90(pview, 2)
        pview[pview == 2] = 4
        pview[pview == -2] = -4
        pview[pview == 1] = 2
        pview[pview == -1] = -2
        pview[pview == 4] = 1
        pview[pview == -4] = -1
    while(isinstance(pos, IfStatement)):
        if pview[pos.diry, pos.dirx] == pos.what:
            pos = pos.children[0]
        else:
            pos = pos.children[1]
    return pos
    
def metric(pgm1, pgm2):
    w.reset()
    p1.setLoc(10,15)
    p2.setLoc(30,15)
    pos1 = pgm1
    pos2 = pgm2
    while w.lost == -1:
        pos1 = doif(pos1, p1)
        if not isinstance(pos1, MoveStatement):
            pos1 = doif(pgm1, p1)
        if isinstance(pos1, PassStatement):
            return pgm2
        movePlayer(pos1, p1)
        pos1 = pgm1 if pos1.children[0] is None else pos1.children[0]
        pos2 = doif(pos2, p2, True)
        if not isinstance(pos2, MoveStatement):
            pos2 = doif(pgm2, p2, True)
        if isinstance(pos2, PassStatement):
            return pgm1
        movePlayer(pos2, p2, True)
        pos2 = pgm2 if pos2.children[0] is None else pos2.children[0]
    if w.lost == 1:
        return pgm2
    else:
        return pgm1

primitives = [IfStatement, MoveStatement]
terminals = [PassStatement]
GP = GeneticProgram(primitives, terminals, metric, crossDepth=30, mutateProb=.1)
GP.population = pk.load(open('pop400.p', 'rb'))

v = Viewer(w, 480, 360)
v.addPlayer(p1, (255,0,0), (127,0,0))
v.addPlayer(p2, (0,255,0), (0,127,0))
b = pk.load(open('bestfound.p','rb'))
for i in GP.population:
    metric(b, i)
