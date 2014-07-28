from random import randint
from numpy import zeros, array, pad

class World:
    def __init__(self, shape=(31,41)):
        if(len(shape) != 2):
            raise ValueError('shape must be 2D')
        elif(shape[0] <= 2 or shape[1] <= 2):
            raise ValueError('shape must be > 2')

        self.shape = shape
        self.reset()
        self.nPlayers = 0

    def reset(self):
        self.wmap = zeros(self.shape)
        self.lost = -1
        self.steps = 0

    def isOpen(self, x, y):
        h,w = self.wmap.shape
        if x < 0 or x >= w or y < 0 or y >= h:
            return False
        return self.wmap[y,x] == 0

    def addPlayer(self, player):
        self.nPlayers += 1
        assert(self.nPlayers < 3)
        player.addListener(self)
        player.head = self.nPlayers
        player.tail = self.nPlayers * -1
        player.pNum = self.nPlayers
        self.notify(player)

    def notify(self, player):
        self.steps += 1
        self.wmap[self.wmap == player.head] = player.tail
        if not self.isOpen(player.x, player.y):
            player.x = -1
            player.y = -1
            self.lost = player.pNum if self.lost == -1 else self.lost
        else:
            self.wmap[player.y,player.x] = player.head
        
    def getPlayerView(self, player):
        assert(player.x != -1 and player.y != -1)
        return pad(self.wmap,2,'constant',constant_values=3)\
            [player.y:player.y+5, player.x:player.x+5]
