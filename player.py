from world import *
from numpy import pad, zeros

class Player:
    def __init__(self, x, y):
        self.listeners = []
        self.x = x
        self.y = y

    def setLoc(self, x, y):
        self.x = x
        self.y = y
        self.notifyAll()

    def moveLeft(self):
        return self.setLoc(self.x-1, self.y)

    def moveRight(self):
        return self.setLoc(self.x+1, self.y)

    def moveUp(self):
        return self.setLoc(self.x, self.y+1)

    def moveDown(self):
        return self.setLoc(self.x, self.y-1)

    def notifyAll(self):
        for l in self.listeners:
            l.notify(self)

    def addListener(self, l):
        self.listeners.append(l)
