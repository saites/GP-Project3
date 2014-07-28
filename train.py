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

CD = 30
MP = .1
primitives = [IfStatement, MoveStatement]
terminals = [PassStatement]
player1 = \
    GeneticProgram(primitives, terminals, None, crossDepth=CD, mutateProb=MP)
player2 = \
    GeneticProgram(primitives, terminals, None, crossDepth=CD, mutateProb=MP)
popSize = {i:50 for i in range(2,7)}
player1.genPopulation(popSize)
player2.genPopulation(popSize)

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

nTest = 40
def metric1(population):    
    toTest = [player2.population[i] for i in \
                permutation(len(player2.population))[:nTest]]
    gameResults = [[playGame(pgm1, pgm2, 1) for pgm2 in toTest] \
                    for pgm1 in population]
    fit = [(pgm1, sum(gameResults[idx])) for idx,pgm1 in enumerate(population)]
    return fit

def metric2(population):
    toTest = [player1.population[i] for i in \
                permutation(len(player1.population))[:nTest]]
    gameResults = [[playGame(pgm1, pgm2, -1) for pgm1 in toTest] \
                    for pgm2 in population]
    fit = [(pgm2, sum(gameResults[idx])) for idx,pgm2 in enumerate(population)]
    return fit

for i in xrange(1000):
    print i
    fit1 = metric1(player1.population)
    fit2 = metric2(player2.population)
    player1.breed(fit1)
    player2.breed(fit2)
    if i % 25 == 0:
        pk.dump(player1.population, open('p1pop%d.p'%i, 'wb'))
        pk.dump(player2.population, open('p2pop%d.p'%i,'wb'))
pk.dump(player1.population, open('p1pop%d.p'%i, 'wb'))
pk.dump(player2.population, open('p2pop%d.p'%i,'wb'))
