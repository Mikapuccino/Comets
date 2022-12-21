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
        self.score = 0
        self.writing = True
        self.show = True
        self.timeLeaderboard = 0
        self.end = False

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

        while self.end == False:

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
                    self.score = self.score + 100
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
        
        ending = False

        text(self.screen, self.phrase, self.font)

        if timePassed >= self.diedTime + 4000:

            count = 0

            self.screen.fill((0, 0, 20))
            
            leaderboard = open("Leaderboard.txt", "r")

            skip = 2
            for i in range(skip):
                leaderboard.readline()
            score1 = leaderboard.readline()
            score1 = score1.split(" ")
            score2 = leaderboard.readline()
            score2 = score2.split(" ")
            score3 = leaderboard.readline()
            score3 = score3.split(" ")
            score4 = leaderboard.readline()
            score4 = score4.split(" ")
            score5 = leaderboard.readline()
            score5 = score5.split(" ")
            score6 = leaderboard.readline()
            score6 = score6.split(" ")
            score7 = leaderboard.readline()
            score7 = score7.split(" ")
            score8 = leaderboard.readline()
            score8 = score8.split(" ")
            score9 = leaderboard.readline()
            score9 = score9.split(" ")
            score10 = leaderboard.readline()
            score10 = score10.split(" ")

            leaderboard.close()

            if self.score > int(score1[1]):
                self.editLeaderboard(3)
                self.score = 0
            
            if self.score > int(score2[1]):
                self.editLeaderboard(4)
                self.score = 0
            
            if self.score > int(score3[1]):
                self.editLeaderboard(5)
                self.score = 0
            
            if self.score > int(score4[1]):
                self.editLeaderboard(6)
                self.score = 0
            
            if self.score > int(score5[1]):
                self.editLeaderboard(7)
                self.score = 0
            
            if self.score > int(score6[1]):
                self.editLeaderboard(8)
                self.score = 0
            
            if self.score > int(score7[1]):
                self.editLeaderboard(9)
                self.score = 0
            
            if self.score > int(score8[1]):
                self.editLeaderboard(10)
                self.score = 0

            if self.score > int(score9[1]):
                self.editLeaderboard(11)
                self.score = 0

            if self.score > int(score10[1]):
                self.editLeaderboard(12)
                self.score = 0

            leaderboard = open("Leaderboard.txt", "r")

            text_in_line(self.screen, leaderboard.readline(), self.font, 40)
            text_in_line(self.screen, leaderboard.readline(), self.font, 80)
            text_in_line(self.screen, leaderboard.readline(), self.font, 120)
            text_in_line(self.screen, leaderboard.readline(), self.font, 160)
            text_in_line(self.screen, leaderboard.readline(), self.font, 200)
            text_in_line(self.screen, leaderboard.readline(), self.font, 240)
            text_in_line(self.screen, leaderboard.readline(), self.font, 280)
            text_in_line(self.screen, leaderboard.readline(), self.font, 320)
            text_in_line(self.screen, leaderboard.readline(), self.font, 360)
            text_in_line(self.screen, leaderboard.readline(), self.font, 400)
            text_in_line(self.screen, leaderboard.readline(), self.font, 440)
            text_in_line(self.screen, leaderboard.readline(), self.font, 480)

            leaderboard.close()
            
            while ending == False:
                
                ending = self.showLeaderboard(ending)

            if ending == True:
            
                self.end = True

    def editLeaderboard(self, lineEdit):

        playerName = input("Input your name: ")
        leaderboard = open("Leaderboard.txt", "r")
        contents = leaderboard.readlines()
        contents[lineEdit - 1] = playerName[:3] + ": " + str(self.score) + "\n"
        leaderboard.close()
        leaderboard = open("Leaderboard.txt", "w")
        leaderboard.writelines(contents)
        leaderboard.close()
    
    def showLeaderboard(self, ended):

        timePassed = pygame.time.get_ticks()
        
        if self.show == True:
            
            self.timeLeaderboard = pygame.time.get_ticks()
            self.show = False
            
        if timePassed >= self.timeLeaderboard + 6000:

            self.phrase = ""
            ended = True
            return(ended)

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