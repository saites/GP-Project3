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

UP,DOWN,LEFT,RIGHT = [MoveStatement.UP, MoveStatement.DOWN,MoveStatement.LEFT,
    MoveStatement.RIGHT]
def movePlayer(pos, player):
    if pos.move == UP:
        player.moveUp()
        print "move up"
    elif pos.move == DOWN:
        player.moveDown()
        print "move down"
    elif pos.move == RIGHT:
        player.moveRight()
        print "move right"
    else:
        player.moveLeft()
        print "move left"

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
            return
        print "1 ",
        movePlayer(pos1, p1)
        pos1 = pgm1 if pos1.children[0] is None else pos1.children[0]

        pos2 = doif(pos2, p2)
        if not isinstance(pos2, MoveStatement):
            pos2 = doif(pgm2, p2)
        if isinstance(pos2, PassStatement):
            return
        print "2 ",
        movePlayer(pos2, p2)
        pos2 = pgm2 if pos2.children[0] is None else pos2.children[0]


def playThatGame(b1, b2):
    v = Viewer(w, 640, 480)
    v.addPlayer(p1, (255,0,0),(0,128,0))
    v.addPlayer(p2, (0,255,0),(65,0,65))
    playGame(b1, b2, 0)

if __name__=='__main__':
    from sys import argv
    b1 = pk.load(open(argv[1], 'rb'))
    b2 = pk.load(open(argv[2], 'rb'))
    playThatGame(b1, b2)
    raw_input()
