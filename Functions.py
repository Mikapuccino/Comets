from pygame.image import load
from pygame.math import Vector2

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

    

