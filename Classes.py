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
        self.font = pygame.font.Font(None, 64)
        self.phrase = ""
        self.bullets = []
        self.player = Player((400, 300), self.bullets.append)
        self.asteroids = []

        self.cooldown = True
        self.lastShot = 0
        self.died = False
        self.diedTime = 0
        self.lines = 0

        for i in range(3):

            while True:
                pos = random_position(self.screen)

                if (pos.distance_to(self.player.pos) > self.min_distance):
                    break
            
            self.asteroids.append(Asteroid(pos, self.asteroids.append))
    
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

    def gameLogic(self):
        
        for gameObject in self.get_GameObject():
            
                gameObject.move(self.screen)

        if self.player:
            for asteroid in self.asteroids:
                if asteroid.collision(self.player):
                    self.player = None
                    self.phrase = "GAME OVER"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids:
                if asteroid.collision(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
        
        for bullet in self.bullets[:]:
            timePassed = pygame.time.get_ticks()
            bulletTime = bullet.timeShot
            if timePassed >= bulletTime + 4000:
                self.bullets.remove(bullet)
                break


        
    def draw(self):

        self.screen.fill((0, 0, 20))
        
        for gameObject in self.get_GameObject():
            gameObject.draw(self.screen)
        
        if self.phrase == "GAME OVER":
            self.gameOver()
        
        pygame.display.flip()
        self.clock.tick(60)

    def gameOver(self):
        self.screen.fill((0, 0, 20))

        if self.died == False:
            self.diedTime = pygame.time.get_ticks()
            self.died = True

        timePassed = pygame.time.get_ticks()

        text(self.screen, self.phrase, self.font)

        if timePassed >= self.diedTime + 4000:

            self.screen.fill((0, 0, 20))
            
            leaderboard = open("Leaderboard.txt", "r")

            self.lines = len(leaderboard.readlines())

            #text(self.screen, leaderboard.readline(), self.font)

            for x in leaderboard:
                for y in range(self.lines):
                    if y == 1:
                        text_line(self.screen, x, self.font, y * 20)
                        print(x)
                    if y == 2:
                        text_line(self.screen, x, self.font, y * 40)
                        print(x)
                    if y == 3:
                        text_line(self.screen, x, self.font, y * 60)
                        print(x)
                    if y == 4:
                        text_line(self.screen, x, self.font, y * 80)
                        print(x)
                    if y == 5:
                        text_line(self.screen, x, self.font, y * 100)
                        print(x)
                    if y == 6:
                        text_line(self.screen, x, self.font, y * 120)
                        print(x)
                    if y == 7:
                        text_line(self.screen, x, self.font, y * 140)
                        print(x)
                    if y == 8:
                        text_line(self.screen, x, self.font, y * 160)
                        print(x)

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
        timeShot = pygame.time.get_ticks()
        bullet = Bullet(self.pos, bulletVelocity, timeShot)
        self.create_bullet_callback(bullet)

class Asteroid(GameObject):

    def __init__(self, pos, asteroid_callback, size=3):
        self.asteroid_callback = asteroid_callback
        self.size = size
        size_scale = { 3:1, 2:0.5, 1:0.25 }
        scale = size_scale[size]
        sprite = rotozoom(load_sprite("Asteroid"), 0, scale)
        super().__init__(pos, sprite, random_velocity(1, 5))
    
    def split(self):
        if self.size > 1:
            if self.size == 3:
                for i in range (3):
                    asteroid = Asteroid(self.pos, self.asteroid_callback, self.size - 1)
                    self.asteroid_callback(asteroid)
            if self.size == 2:
                for i in range (5):
                    asteroid = Asteroid(self.pos, self.asteroid_callback, self.size - 1)
                    self.asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, pos, velocity, timeShot):
        super().__init__(pos, load_sprite("Bullet"), velocity)

        def move(self):

            self.pos = self.pos + self.velocity

        self.timeShot = timeShot