import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from Functions import *

UP = Vector2(0, -1)

class Comets:

    min_distance = 150

    def __init__(self):

        self.initPygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.player = Player((400, 300), self.bullets.append)
        self.asteroids = []

        self.cooldown = True
        self.lastShot = 0

        for i in range(3):

            while True:
                pos = random_position(self.screen)

                if (pos.distance_to(self.player.pos) > self.min_distance):
                    break
            
            self.asteroids.append(Asteroid(pos))
    
    def get_GameObject(self):

        gameObjects = [*self.bullets, *self.asteroids]

        if self.player:
            gameObjects.append(self.player)

        return gameObjects

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

        if self.cooldown == False:

            timePassed = pygame.time.get_ticks()

            if timePassed >= self.lastShot + 4000:

                self.cooldown = True

        for evt in events:
            if (evt.type == pygame.QUIT):
                quit()

            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE and self.cooldown == True:
                self.player.shoot()
                self.cooldown = False
                self.lastShot = pygame.time.get_ticks()


        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            self.player.rotate(clockwise=True)

        if pygame.key.get_pressed()[pygame.K_LEFT] == True:
            self.player.rotate(clockwise=False)

        if pygame.key.get_pressed()[pygame.K_UP] == True:
            self.player.accelerate()

#        print(self.bullets)

    def gameLogic(self):

        for gameObject in self.get_GameObject():
            
                gameObject.move(self.screen)

        if self.player:
            for asteroid in self.asteroids:
                if asteroid.collision(self.player):
                    self.player = None
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids:
                if asteroid.collision(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    break
        
#        for bullet in self.bullets[:]:
#            timePassed = pygame.time.get_ticks()
#            bulletTime = bullet.timeShot
#            if timePassed >= bulletTime + 4000:
#                self.bullets.remove(bullet)
#                break


        
    def draw(self):

        self.screen.fill((0, 0, 20))
        for gameObject in self.get_GameObject():
            gameObject.draw(self.screen)
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
    BulletSpeed = 5

    def __init__(self, pos, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
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

    def shoot(self):

        bulletVelocity = self.direction * self.BulletSpeed + self.velocity
        timeShot = pygame.time.get_ticks
        bullet = Bullet(self.pos, bulletVelocity, timeShot)
        self.create_bullet_callback(bullet)

class Asteroid(GameObject):

    def __init__(self, pos):
        self.direction = Vector2(UP)
        super().__init__(pos, load_sprite("Asteroid"), random_velocity(1, 5))

class Bullet(GameObject):
    def __init__(self, pos, velocity, timeShot):
        super().__init__(pos, load_sprite("PlayerShip"), velocity)

        def move():

            self.pos = self.pos + self.velocity

        self.timeShot = timeShot