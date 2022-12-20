import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from Functions import *

UP = Vector2(0, -1)

class Comets:

    def __init__(self):

        self.initPygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player((400, 300))
    
    def main(self):

        while True:

            self.inputLogic()
            self.gameLogic()
            self.draw()

    def initPygame(self):

        pygame.init()
        pygame.display.set_caption("Comets")

    def inputLogic(self):

        events = pygame.event.get()
        for evt in events:
            if (evt.type == pygame.QUIT):
                quit()

        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            self.player.rotate(clockwise=True)

        if pygame.key.get_pressed()[pygame.K_LEFT] == True:
            self.player.rotate(clockwise=False)

        if pygame.key.get_pressed()[pygame.K_UP] == True:
            self.player.accelerate()

#        if pygame.key.get_pressed()[pygame.K_DOWN] == True:
#            newPlayerY = newPlayerY + 0.2

    def gameLogic(self):

        self.player.move(self.screen)
        
    def draw(self):

        self.screen.fill((0, 0, 20))
        self.player.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

class GameObject:

    def __init__(self, pos, sprite, velocity):
        
        self.pos = Vector2(pos)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):

        blitPos = self.pos - Vector2(self.radius)
        surface.blit(self.sprite, blitPos)

    def move(self, surface):

        self.pos = wrap_position((self.pos + self.velocity), surface)

    def collision(self, otherObj):

        distance = self.pos.distance_to(otherObj.pos)
        return distance < self.radius + otherObj.radius

class Player(GameObject):

    Rotation = 3
    Acceleration = 0.25

    def __init__(self, pos):
        self.direction = Vector2(UP)
        super().__init__(pos, load_sprite("PlayerShip"), Vector2(0))

    def accelerate(self):

        self.velocity += self.direction * self.Acceleration

    def rotate(self, clockwise=True):
        
        turn = 0
        
        if clockwise:
            turn = 1
        else:
            turn = -1

        angle = self.Rotation * turn

        self.direction.rotate_ip(angle)

    def draw(self, surface):

        angle = self.direction.angle_to(UP)
        rotatedSurface = rotozoom(self.sprite, angle, 1.0)
        rotatedSurfaceSize = Vector2(rotatedSurface.get_size())
        blitPos = self.pos - rotatedSurfaceSize * 0.5
        surface.blit(rotatedSurface, blitPos)