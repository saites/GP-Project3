from player import *
from genetic import *
from random import randint

class IfStatement(Primitive):
    #NW,N,NE,W,C,E,SW,S,SE = range(25)
    def __init__(self, direction=0, what=0):
        Primitive.__init__(self, 2)
        self.dirx = direction % 5
        self.diry = direction / 5
        self.what = what
        self.children = [None, None]

    def __str__(self):
        return "if w.getPlayerView(p[pnum])[%d,%d] == %d:"\
            % (self.diry, self.dirx, self.what)

    def makeRand(self):
        self.dirx = randint(0,4)
        self.diry = randint(0,4)
        self.what = randint(-2,3)

class MoveStatement(Primitive):
    F,L,R = range(3)
    def __init__(self, move=0):   
        Primitive.__init__(self, 1)
        self.move = move
        self.children = [None]

    def __str__(self):
        if self.move == MoveStatement.L:
            mystr = "p[pnum].turnLeft()"
        elif self.move == MoveStatement.D:
            mystr = "p[pnum].turnRight()"
        elif self.move == MoveStatement.F:
            mystr = "p[pnum].goForward()"
        return mystr

    def makeRand(self): 
        self.move = randint(0,2)

class PassStatement(Terminal):
    def __init__(self):
        pass

    def __str__(self):
        return "Pass"
