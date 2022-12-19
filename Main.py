import pygame
import pygame.freetype
from Classes import *

#class Player:
#    def __init__(self, pos):
#
#        self.pos = pos
#        self.Surface = pygame.Surface((16, 16), pygame.SRCALPHA)
#        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
#        self.sprite = pygame.image.load("PlayerShip.png")
#
#    def rotate(self, angle):
#        self.rect = pygame.transform.rotate(self.rect, angle)
#
#def main():
#
#    pygame.init()
#
#    res = (800, 600)
#    screen = pygame.display.set_mode(res)
#
#    player = Player((384, 284))
#
#    screen.blit(player.sprite, player.pos)
#
#    newPlayerX = 384
#    newPlayerY = 284
#
#    exit = False
#
#    while(not exit):
#        
#        events = pygame.event.get()
#        for evt in events:
#            if (evt.type == pygame.QUIT):
#                exit = True
#
#        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
#            player.rotate(-2)
#
#        if pygame.key.get_pressed()[pygame.K_LEFT] == True:
#            player.rotate(2)
#
#        if pygame.key.get_pressed()[pygame.K_UP] == True:
#            newPlayerY = newPlayerY - 0.2
#
#        if pygame.key.get_pressed()[pygame.K_DOWN] == True:
#            newPlayerY = newPlayerY + 0.2
#
#
#
#        screen.fill((0, 0, 20))
#
#        screen.blit(player.sprite, player.pos)
#
#        player.pos = (newPlayerX, newPlayerY)
#
#        pygame.display.flip()
#
#main()

comets = Comets()
comets.main()