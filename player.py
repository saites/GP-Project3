from numpy import pad, zeros

class Player:
    UP, LEFT, DOWN, RIGHT = range(4)
    def __init__(self, x, y): 
        self.listeners = []
        self.x = x
        self.y = y
        self.d = Player.UP

    def setLoc(self,x,y):
        self.x = x
        self.y = y
        self.notifyAll()

    def turnLeft(self):
        self.d = (self.d+1) % 4
        self.goForward()

    def turnRight(self):
        self.d = (self.d-1) % 4
        self.goForward()

    def goForward(self):
        if self.d == Player.UP:
            self.y += 1
        elif self.d == Player.DOWN:
            self.y -= 1
        elif self.d == Player.LEFT:
            self.x -= 1
        elif self.d == Player.RIGHT:
            self.x += 1
        self.notifyAll()

    def notifyAll(self):
        for l in self.listeners:
            l.notify(self)

    def addListener(self, l):
        self.listeners.append(l)
