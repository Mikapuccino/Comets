import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from Functions import *

# This file is used to create all the classes the game will use,
# additionally being used to run the entire game inside the classes

# This variable is used to define the up angle, this being pointed directly up

UP = Vector2(0, -1)

# This class is the main one that is used to run the whole game
# The main logic for the game is all contained within this class

class Comets:

    min_distance = 150

    def __init__(self):

        # Defines every variable the game needs
        
        self.initPygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.phrase = ""
        self.bullets = []
        self.player = Player((400, 300), self.bullets.append)
        self.asteroids = []

        self.start = False
        self.up_pressed = False
        self.down_pressed = False
        self.cooldown = True
        self.lastShot = 0
        self.died = False
        self.diedTime = 0
        self.score = 0
        self.writing = True
        self.show = True
        self.timeLeaderboard = 0
        self.end = True

        # Creates x asteroids at the start of the game, x = 3 for now

        for i in range(3):

            while True:
                pos = random_position(self.screen)

                if (pos.distance_to(self.player.pos) > self.min_distance):
                    break
            
            self.asteroids.append(Asteroid(pos, self.asteroids.append))
    
    # This function detects all game objects that exist

    def get_GameObject(self):

        gameObjects = [*self.bullets, *self.asteroids]

        if self.player:
            gameObjects.append(self.player)

        return gameObjects

    # Main game loop

    def main(self):

        while True:

            if self.end == True and self.start == False:

                self.main_menu()
        
            if self.end == False and self.start == True:

                self.inputLogic()
                self.gameLogic()
                self.draw()

    # This is only used to initiate pygame

    def initPygame(self):

        pygame.init()

    # This function is used to display the main menu and to do
    # the option the player selects

    def main_menu(self):

        self.start = False

        self.screen.fill((0, 0, 20))
        text_in_line(self.screen, "COMETS", self.font, 40, "white")
        text_in_line(self.screen, "START", self.font, 280, "white")
        text_in_line(self.screen, "EXIT", self.font, 340, "white")

        if self.up_pressed == True:

            text_in_line(self.screen, "START", self.font, 280)

        if self.down_pressed == True:

            text_in_line(self.screen, "EXIT", self.font, 340)

        events = pygame.event.get()

        for evt in events:
            if (evt.type == pygame.QUIT):
                quit()

        if pygame.key.get_pressed()[pygame.K_UP] == True:
            text_in_line(self.screen, "START", self.font, 280)
            text_in_line(self.screen, "EXIT", self.font, 340, "white")
            self.up_pressed = True
            self.down_pressed = False

        if pygame.key.get_pressed()[pygame.K_DOWN] == True:
            text_in_line(self.screen, "EXIT", self.font, 340)
            text_in_line(self.screen, "START", self.font, 280, "white")
            self.down_pressed = True
            self.up_pressed = False

        if pygame.key.get_pressed()[pygame.K_SPACE] == True:

            if self.down_pressed == True:
                quit()

            if self.up_pressed == True:
                self.start = True
                self.end = False
                self.restart()

        pygame.display.flip()
        self.clock.tick(60)

    # This funtion is used to detect the player's inputs during the game
    # and make the appropriate action

    def inputLogic(self):

        events = pygame.event.get()

        if self.cooldown == False:

            timePassed = pygame.time.get_ticks()

            if timePassed >= self.lastShot + 4000:

                self.cooldown = True

        for evt in events:
            if (evt.type == pygame.QUIT):
                quit()

            if self.phrase != "GAME OVER":

                if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE and self.cooldown == True:
                    self.player.shoot()
                    self.cooldown = False
                    self.lastShot = pygame.time.get_ticks()

        if self.phrase != "GAME OVER":

            if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
                self.player.rotate(clockwise=True)
    
            if pygame.key.get_pressed()[pygame.K_LEFT] == True:
                self.player.rotate(clockwise=False)
    
            if pygame.key.get_pressed()[pygame.K_UP] == True:
                self.player.accelerate()

    # This function is used to move all objects and detect collisions between objects
    # and doing the appropriate action for each collision
    # Also used to create more asteroids when there are no more asteroids in the game

    def gameLogic(self):
        
        for gameObject in self.get_GameObject():
            
                gameObject.move(self.screen)

        if self.asteroids == []:

            for i in range(3):

                while True:
                    pos = random_position(self.screen)

                    if (pos.distance_to(self.player.pos) > self.min_distance):
                        break
            
                self.asteroids.append(Asteroid(pos, self.asteroids.append))

        # If the player collides with an asteroid, the player dies and it's game over

        if self.player:
            for asteroid in self.asteroids:
                if asteroid.collision(self.player):
                    self.player = None
                    self.phrase = "GAME OVER"
                    break

        # If a bullet collides with an asteroid, it splits it if possible or it destroys it
        # Raises the player score by 100

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids:
                if asteroid.collision(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    self.score = self.score + 100
                    break
        
        # If a bullet has existed for 4 seconds, the bullet disappears

        for bullet in self.bullets[:]:
            timePassed = pygame.time.get_ticks()
            bulletTime = bullet.timeShot
            if timePassed >= bulletTime + 4000:
                self.bullets.remove(bullet)
                break
        
    # This functions is used to properly display each object
    # on the screen, with proper orientation, and to detect
    # if the player has died, calling the gameOver function
    
    def draw(self):

        self.screen.fill((0, 0, 20))
        
        for gameObject in self.get_GameObject():
            gameObject.draw(self.screen)
        
        if self.phrase == "GAME OVER":
            self.gameOver()
        
        pygame.display.flip()
        self.clock.tick(60)

    # This function is used to display the game over screen and call the leaderboard
    # screen, asking for an input from the player if they got a better score
    # than one of the best 10 scores

    def gameOver(self):
        self.screen.fill((0, 0, 20))

        if self.died == False:
            self.diedTime = pygame.time.get_ticks()
            self.died = True

        timePassed = pygame.time.get_ticks()
        
        ending = False

        text(self.screen, self.phrase, self.font, "white")

        if timePassed >= self.diedTime + 4000:

            self.screen.fill((0, 0, 20))
            
            # Opens leaderboard file and detects the scores in it

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

            # Detects if the player got a better score than what is on the leaderboard

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

            # Displays the leaderboard, with the new score if the player got a higher score
            # than one that was already on the leaderboard

            leaderboard = open("Leaderboard.txt", "r")

            text_in_line(self.screen, leaderboard.readline(), self.font, 40, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 80, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 120, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 160, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 200, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 240, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 280, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 320, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 360, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 400, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 440, "white")
            text_in_line(self.screen, leaderboard.readline(), self.font, 480, "white")

            leaderboard.close()
            
            while ending == False:
                
                ending = self.showLeaderboard(ending)

            if ending == True:
            
                self.end = True
                self.start = False

    # This function is used to edit the leaderboard when the player
    # got a higher score than one that is already on it

    def editLeaderboard(self, lineEdit):

        x = 0

        playerName = input("Input your name: ")
        leaderboard = open("Leaderboard.txt", "r")
        contents = leaderboard.readlines()

        # Edits the leaderboard to put the player initials and score on the proper
        # placement and moves every score below it, also removing the previous score in last place

        while (lineEdit + x) < len(contents):

            bottomUp = len(contents) - x - 1

            if x == 0:
                contents[bottomUp] = contents[bottomUp - 1].strip()
            if x > 0:
                contents[bottomUp] = contents[bottomUp - 1]

            x = x + 1

        contents[lineEdit - 1] = playerName[:3] + ": " + str(self.score) + "\n"
        leaderboard.close()
        leaderboard = open("Leaderboard.txt", "w")
        leaderboard.writelines(contents)
        leaderboard.close()
    
    # This function displays the leaderboard for 6 seconds

    def showLeaderboard(self, ended):

        timePassed = pygame.time.get_ticks()
        
        if self.show == True:
            
            self.timeLeaderboard = pygame.time.get_ticks()
            self.show = False
            
        if timePassed >= self.timeLeaderboard + 6000:

            self.phrase = ""
            ended = True
            return(ended)

    # This function is used to restart the game everytime the player
    # chooses start in the main menu

    def restart(self):

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

        for i in range(3):

            while True:
                pos = random_position(self.screen)

                if (pos.distance_to(self.player.pos) > self.min_distance):
                    break
            
            self.asteroids.append(Asteroid(pos, self.asteroids.append))

# This class is inherited by every other game object
# Used to define functions and variables that all game objects use

class GameObject:

    def __init__(self, pos, sprite, velocity):
        
        self.pos = Vector2(pos)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    # Used to draw the object on the screen

    def draw(self, surface):

        blitPos = self.pos - Vector2(self.radius)
        surface.blit(self.sprite, blitPos)

    # Used to move the object on the screen and wrap around the screen
    # if it moves beyond an edge of the screen
    
    def move(self, surface):

        self.pos = wrap_position((self.pos + self.velocity), surface)

    # Used to detect if there was a collision

    def collision(self, otherObj):

        distance = self.pos.distance_to(otherObj.pos)
        return distance < self.radius + otherObj.radius

# This class is used for the player, used to move, accelerate, rotate and shoot bullets

class Player(GameObject):

    Rotation = 3
    Acceleration = 0.25
    BulletSpeed = 5

    def __init__(self, pos, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.direction = Vector2(UP)
        super().__init__(pos, load_sprite("PlayerShip"), Vector2(0))

    # Used to change the speed at which the player moves

    def accelerate(self):

        self.velocity += self.direction * self.Acceleration

    # Used to properly rotate the player and the sprite

    def rotate(self, clockwise=True):
        
        turn = 0
        
        if clockwise:
            turn = 1
        else:
            turn = -1

        angle = self.Rotation * turn

        self.direction.rotate_ip(angle)

    # Used to display the player sprite with the proper rotation

    def draw(self, surface):

        angle = self.direction.angle_to(UP)
        rotatedSurface = rotozoom(self.sprite, angle, 1.0)
        rotatedSurfaceSize = Vector2(rotatedSurface.get_size())
        blitPos = self.pos - rotatedSurfaceSize * 0.5
        surface.blit(rotatedSurface, blitPos)

    # Used to shoot bulets from the front of the player,
    # with speed depending on the player speed

    def shoot(self):

        bulletVelocity = self.direction * self.BulletSpeed + self.velocity
        timeShot = pygame.time.get_ticks()
        bullet = Bullet(self.pos, bulletVelocity, timeShot)
        self.create_bullet_callback(bullet)

# This class is used for the asteroids, used for splitting the asteroids 
# properly depending on their size

class Asteroid(GameObject):

    def __init__(self, pos, asteroid_callback, size=3):
        self.asteroid_callback = asteroid_callback
        self.size = size
        size_scale = { 3:1, 2:0.5, 1:0.25 }
        scale = size_scale[size]
        sprite = rotozoom(load_sprite("Asteroid"), 0, scale)
        super().__init__(pos, sprite, random_velocity(1, 5))
    
    # This function is used to split the asteroid, splitting a big asteroid
    # into 3 medium asteroids and a medium asteroid into 5 small ones
    
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

# This class is used for bullets, only defining the time at which the bullet was fired
# This is used to determine the cooldown and the lifespan of the bullet

class Bullet(GameObject):
    def __init__(self, pos, velocity, timeShot):
        super().__init__(pos, load_sprite("Bullet"), velocity)

        self.timeShot = timeShot