from world import *
from player import *
from viewer import *
from genetic import *
from represent import *
from numpy.random import permutation
import cPickle as pk
from sys import argv

w = World()
p1 = Player(10,10)
p2 = Player(20,10)
w.addPlayer(p1,1)
w.addPlayer(p2,2)


L,R,F = [MoveStatement.L,MoveStatement.R,MoveStatement.F]
def movePlayer(pos, player):
    if pos.move == L:
        player.turnLeft()
        #print player.pNum, "left"
    elif pos.move == R:
        player.turnRight()
        #print player.pNum, "right"
    elif pos.move == F:
        player.goForward()
        #print player.pNum, "forward"
    else:
        assert(False)

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
    while w.lost is None:
        pos1 = doif(pos1, p1)
        if isinstance(pos1, PassStatement):
            p1.goForward()
            pos1 = pgm1
            #print "1 forward"
        else:
            movePlayer(pos1, p1)
            pos1 = pgm1 if pos1.children[0] is None else pos1.children[0]

        pos2 = doif(pos2, p2)
        if isinstance(pos2, PassStatement):
            p2.goForward()
            pos2 = pgm2
            #print "2 forward"
        else:
            movePlayer(pos2, p2)
            pos2 = pgm2 if pos2.children[0] is None else pos2.children[0]
    if p1.x == -1:
        if p2.x == -1:
            #print "draw"
            return 0
        else:
            #print "p2 wins"
            return -1
    else:
        #print "p1 wins"
        return 1

'''
v = Viewer(w)
v.addPlayer(p1, (255,0,0),(128,0,0))
v.addPlayer(p2, (0,255,0),(0,128,0))
'''
pop1 = pk.load(open(argv[1],'rb'))
pop2 = pk.load(open(argv[2],'rb'))

t = 0
b1 = pop1[0]
for p in pop2:
    t += playGame(b1, p, 0)
print t

t = 0
b2 = pop2[0]
for p in pop1:
    t += playGame(p, b2, 0)
print t
        
#for i in xrange(len(pop1)):
#    b1 = pop1[i]
#    b2 = pop2[i]
#    playGame(b1, b2, 0)
pk.dump(b1, open('b1.p','wb'))
pk.dump(b2, open('b2.p','wb'))

