import pygame
import pygame.freetype
from Classes import *

# Where the function Comets() are called to start the game.

comets = Comets()
start = False

while start == False:
    start = comets.main_menu()

if start == True:
    comets.main()