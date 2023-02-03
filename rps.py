import pygame
import random
from pygame.locals import (
    K_0,K_1,K_2,K_3,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



def fight(input1, input2):
    if (input1>input2):
        print("Player1 WIN")
    else:
        print("Player2 WIN")

'''
while(True):
    val = input("Enter a int between 0 and 10: ")
    fight(int(val))
    continue
'''

def fight2(input1, input2):
    
    pygame.init()

    # Define constants for the screen width and height
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    #######################################################################################################################################
    # Run until the user asks to quit
    running = True
    while running:

        numFont = pygame.font.SysFont("Times New Roman", 90)
        textFont = pygame.font.SysFont("Times New Roman", 30)

        red = (255,0,0)
        green = (0, 255, 0)

        text1 = textFont.render("player1 inputted:", 1, red)
        text2 = textFont.render("player2 inputted:", 1, green)
        if input1 > input2:
            resulttext = textFont.render("PLAYER 1 WIN!!!:", 1, (122, 0, 122))
        else:
            resulttext = textFont.render("PLAYER 2 WIN!!!:", 1, (0, 122, 122))

        num1 = numFont.render(str(input1), 1, red)
        num2 = numFont.render(str(input2), 1, green)
        
        ### pass a string to myFont.render

        screen.blit(text1, (50, 100))
        screen.blit(num1, (50, 150))

        screen.blit(text2, (400, 100))
        screen.blit(num2, (400, 150))

        screen.blit(resulttext, (250, 300))


        # This line says "Draw surf onto the screen at the center"
        pygame.display.flip()
        
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False


        ######################################




    # Done! Time to quit.
    pygame.quit()
    
