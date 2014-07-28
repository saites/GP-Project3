from world import *
from player import *
from viewer import *
from genetic import *
from represent import *
from numpy.random import permutation
import cPickle as pk

w = World()
p1 = Player(10,10)
p2 = Player(20,10)
w.addPlayer(p1)
w.addPlayer(p2)

primitives = [IfStatement, MoveStatement]
terminals = [PassStatement]
pop1 = pk.load(open('p1pop200.p','rb'))
pop2 = pk.load(open('p2pop200.p','rb'))

UP,DOWN,LEFT,RIGHT = [MoveStatement.UP, MoveStatement.DOWN,MoveStatement.LEFT,
    MoveStatement.RIGHT]
def movePlayer(pos, player):
    if pos.move == UP:
        player.moveUp()
    elif pos.move == DOWN:
        player.moveDown()
    elif pos.move == RIGHT:
        player.moveRight()
    else:
        player.moveLeft()

def doif(pos, player):
    pview = w.getPlayerView(player)
    while(isinstance(pos, IfStatement)):
        if pview[pos.diry, pos.dirx] == pos.what:
            pos = pos.children[0]
        else:
            pos = pos.children[1]
    return pos
    
def playGame(pgm1, pgm2, mod):
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
            return -mod
        movePlayer(pos1, p1)
        pos1 = pgm1 if pos1.children[0] is None else pos1.children[0]

        pos2 = doif(pos2, p2)
        if not isinstance(pos2, MoveStatement):
            pos2 = doif(pgm2, p2)
        if isinstance(pos2, PassStatement):
            return mod
        movePlayer(pos2, p2)
        pos2 = pgm2 if pos2.children[0] is None else pos2.children[0]
    if w.lost == 1:
        return -mod
    else:
        return mod

nTest = 100
def metric1(population):    
    toTest = [pop2[i] for i in \
                permutation(len(pop2))[:nTest]]
    gameResults = [[playGame(pgm1, pgm2, 1) for pgm2 in toTest] \
                    for pgm1 in population]
    fit = [(pgm1, sum(gameResults[idx])) for idx,pgm1 in enumerate(population)]
    return fit

def metric2(population):
    toTest = [pop1[i] for i in \
                permutation(len(pop1))[:nTest]]
    gameResults = [[playGame(pgm1, pgm2, -1) for pgm1 in toTest] \
                    for pgm2 in population]
    fit = [(pgm2, sum(gameResults[idx])) for idx,pgm2 in enumerate(population)]
    return fit


fit1 = metric1(pop1)
fit2 = metric1(pop2)
fit1.sort(lambda y,x: x[1] -y[1])
fit2.sort(lambda y,x: x[1] -y[1])
b1 = fit1[0][0]
b2 = fit2[0][0]
pk.dump(b1, open('b1.p','wb'))
pk.dump(b2, open('b2.p','wb'))
exit()

v = Viewer(w, 640, 480)
v.addPlayer(p1, (255,0,0),(128,0,0))
v.addPlayer(p2, (0,255,0),(0,128,0))
playGame(b1, b2, 0)
