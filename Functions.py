from pygame.image import load
from pygame.math import Vector2
import random

def load_sprite(name, withAlpha = True):

    path = f"{name}.png"
    loadedSprite = load(path)

    if withAlpha:

        return loadedSprite.convert_alpha()
    
    else:

        return loadedSprite.convert()

def wrap_position(pos, surface):

    x,y = pos
    w,h = surface.get_size()

    return Vector2(x % w, y % h)

def random_position(surface):

    return Vector2(random.randrange(surface.get_width()), 
    random.randrange(surface.get_height()))

def random_velocity(min_velocity, max_velocity):

    speed = random.randint(min_velocity, max_velocity)
    angle = random.randrange(0, 360)

    return Vector2(speed, 0).rotate(angle)


    

