import pygame
import pygame.freetype

def main():

    pygame.init()

    res = (800, 600)
    screen = pygame.display.set_mode(res)

    playerImage = pygame.image.load("PlayerShip.png")

    playerPos = (384,284)
    screen.blit(playerImage, playerPos)

    newPlayerX = 384
    newPlayerY = 284

    exit = False

    while(not exit):
        
        events = pygame.event.get()
        for evt in events:
            if (evt.type == pygame.QUIT):
                exit = True

        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            playerImage = pygame.transform.rotate(playerImage, -90)

        if pygame.key.get_pressed()[pygame.K_LEFT] == True:
            playerImage = pygame.transform.rotate(playerImage, 90)

        if pygame.key.get_pressed()[pygame.K_UP] == True:
            newPlayerY = newPlayerY - 0.2

        if pygame.key.get_pressed()[pygame.K_DOWN] == True:
            newPlayerY = newPlayerY + 0.2



        screen.fill((0, 0, 20))

        screen.blit(playerImage, playerPos)

        playerPos = (newPlayerX, newPlayerY)

        pygame.display.flip()

main()