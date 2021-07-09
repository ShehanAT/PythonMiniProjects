import pygame
import pygame_menu 
import random 
import sys 

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)


BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
GAME_PAUSED = False 

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(DISPLAYSURF, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    DISPLAYSURF.blit(textSurf, textRect)

def unpause():
    global GAME_PAUSED 
    GAME_PAUSED = False 
    print("Resume Game!")

def pause():
    font = pygame.font.SysFont("Consolas", 32)
    while GAME_PAUSED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pause_text = font.render("Game Paused", 1, (255, 255, 255))
        pause_rect = pause_text.get_rect(center = (WINDOWWIDTH/2, WINDOWHEIGHT/2))
            # DISPLAYSURF.fill(0,0,0);
        DISPLAYSURF.blit(pause_text, pause_rect)
        button("Resume", WINDOWWIDTH/2, WINDOWHEIGHT/2, 100, 50, NAVYBLUE, GRAY, unpause)
        button("Quit", WINDOWWIDTH/2, WINDOWHEIGHT/2 - 50, 100, 50, NAVYBLUE, GRAY, unpause)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


FPS = 30
FPSCLOCK = pygame.time.Clock()
pygame.init()

while True: # main game loop
    mouseClicked = False

    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    # drawBoard(mainBoard, revealedBoxes)
    font = pygame.font.SysFont("Consolas", 32)
    # game_score_string = "Score: " + str(GAME_SCORE) + "     Level: " + str(GAME_LEVEL)
    # game_score_text = font.render(game_score_string, 1, (255, 255, 255))
    # game_score_rect = game_score_text.get_rect(center = (120, 10))

    for event in pygame.event.get(): # event handling loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            GAME_PAUSED = True  
        pause()



        
