import pygame
import pygame.freetype

def main():

    pygame.init()

    res = (800, 600)
    screen = pygame.display.set_mode(res)

    exit = False

    while(not exit):

        events = pygame.event.get()
        for evt in events:
            if (evt.type == pygame.QUIT):
                exit = True

        screen.fill((0, 0, 20))

        pygame.display.flip()

main()