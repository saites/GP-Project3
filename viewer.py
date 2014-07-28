import pygame
from pygame.locals import *
from numpy import rot90, zeros

class Viewer:
    def __init__(self, world, w=280, h=180):
        self.world = world
        self.players = []

        pygame.init()
        self.screen = pygame.display.set_mode((w,h))
        self.fpsClock = pygame.time.Clock()
        pygame.display.set_caption('TRON')

        self.W = w
        self.H = h

        h,w = world.wmap.shape
        self.surface = pygame.Surface((w,h))
        pygame.surfarray.use_arraytype('numpy')
        self.hColor = {}
        self.tColor = {}
        self.fps = 30

    def addPlayer(self, player, hColor, tColor):
        self.players.append(player)
        player.addListener(self)
        self.hColor[player] = hColor
        self.tColor[player] = tColor
        self.fps = 20*len(self.players)

    def notify(self, player): 
        self.draw()

    def draw(self):
        im = zeros(self.world.wmap.shape+(3,)).astype(int)
        for p in self.players:
            im[self.world.wmap == -p.pNum] = self.tColor[p]
            im[self.world.wmap == p.pNum] = self.hColor[p]
        im = pygame.surfarray.map_array(self.surface, im)
        pygame.surfarray.blit_array(self.surface, rot90(im,3))
        pygame.transform.scale(self.surface, (self.W, self.H), self.screen)
        pygame.display.update()
        self.fpsClock.tick(self.fps)
