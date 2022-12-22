import pygame
from pygame.image import load
from pygame.math import Vector2
from pygame import Color
import random

# This file is used to define additional functions used in the game

# This function loads the proper sprite for each object,
# also removing transparent spaces in the image

def load_sprite(name, withAlpha = True):

    path = f"{name}.png"
    loadedSprite = load(path)

    if withAlpha:

        return loadedSprite.convert_alpha()
    
    else:

        return loadedSprite.convert()

# This function is used to wrap an object around the screen when it reaches an edge

def wrap_position(pos, surface):

    x,y = pos
    w,h = surface.get_size()

    return Vector2(x % w, y % h)

# This function is used to determine a random position for an object
# This is only used when creating fully new asteroids

def random_position(surface):

    return Vector2(random.randrange(surface.get_width()), 
    random.randrange(surface.get_height()))

# This function is used to determine a random position for an object
# This is only used when creating new asteroids

def random_velocity(min_velocity, max_velocity):

    speed = random.randint(min_velocity, max_velocity)
    angle = random.randrange(0, 360)

    return Vector2(speed, 0).rotate(angle)

# This function is used to display text in the center of the screen

def text(surface, text, font, color=Color("tomato")):

    textSurface = font.render(text, True, color)
    rect = textSurface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(textSurface, rect)

# This function is used to display text in the screen
# at a specific height and in the middle of the screen's width 

def text_in_line(surface, text, font, pos, color=Color("tomato")):

    checkText = text.strip()
    textSurface = font.render(checkText, True, color)
    rect = textSurface.get_rect()
    rect.center = Vector2(400, pos)

    surface.blit(textSurface, rect)