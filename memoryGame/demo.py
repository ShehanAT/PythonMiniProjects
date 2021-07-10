import pygame
import pygame_menu 
import random 
import sys 

DIAMOND_ASSETPATH = {
    "red": "./assets/red_diamond.png",
    "green": "./assets/green_diamond.png",
    "blue": "./assets/blue_diamond.png",
    "yellow": "./assets/yellow_diamond.png",
    "tan": "./assets/tan_diamond.png",
    "grey": "./assets/grey_diamond.png",
    "teal": "./assets/teal_diamond.png"
}
HEXAGON_ASSETPATH = {
    "red": "./assets/red_hexagon.png",
    "green": "./assets/green_hexagon.png",
    "blue": "./assets/blue_hexagon.png",
    "yellow": "./assets/yellow_hexagon.png",
    "tan": "./assets/tan_hexagon.png",
    "grey": "./assets/grey_hexagon.png",
    "teal": "./assets/teal_hexagon.png"
}
OCTAGON_ASSETPATH = {
    "red": "./assets/red_octagon.png",
    "green": "./assets/green_octagon.png",
    "blue": "./assets/blue_octagon.png",
    "yellow": "./assets/yellow_octagon.png",
    "tan": "./assets/tan_octagon.png",
    "grey": "./assets/grey_octagon.png",
    "teal": "./assets/teal_octagon.png"
}
SQUARE_ASSETPATH = {
    "red": "./assets/red_square.png",
    "green": "./assets/green_square.png",
    "blue": "./assets/blue_square.png",
    "yellow": "./assets/yellow_square.png",
    "tan": "./assets/tan_square.png",
    "grey": "./assets/grey_square.png",
    "teal": "./assets/teal_square.png"
}
TRIANGLE_ASSETPATH = {
    "red": "./assets/red_triangle.png",
    "green": "./assets/green_triangle.png",
    "blue": "./assets/blue_triangle.png",
    "yellow": "./assets/yellow_triangle.png",
    "tan": "./assets/tan_triangle.png",
    "grey": "./assets/grey_triangle.png",
    "teal": "./assets/teal_triangle.png"
}


FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 4 # number of columns of icons
BOARDHEIGHT = 3 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
GAME_SCORE = 0
GAME_LEVEL = 1 
GAME_PAUSED = False 


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)


BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

TIMER_PAUSED = False 
TIMER_RUNNING = True 

SQUARE = 'square'
DIAMOND = 'diamond'
HEXAGON = 'hexagon'
OCTAGON = 'octagon'
TRIANGLE = 'triangle'

SPRITE_RED = "red"
SPRITE_GREEN = "green"
SPRITE_BLUE = "blue"
SPRITE_YELLOW = "yellow"
SPRITE_TAN = "tan"
SPRITE_GREY = "grey"
SPRITE_TEAL = "teal"

ALLCOLORS = (SPRITE_RED, SPRITE_GREEN, SPRITE_BLUE, SPRITE_YELLOW, SPRITE_TAN, SPRITE_GREY, SPRITE_TEAL)
ALLSHAPES = (DIAMOND, HEXAGON, OCTAGON, SQUARE, TRIANGLE)

def levelUp():
    global BOARDWIDTH, BOARDHEIGHT
    BOARDWIDTH += 1 
    BOARDHEIGHT += 1 


def drawDiamondSprite(color, left, top, width, height):
    diamondImage = None; 
    if(DIAMOND_ASSETPATH[color]):
        diamondImage = DIAMOND_ASSETPATH[color];
    diamondImage = pygame.transform.scale(pygame.image.load(diamondImage).convert_alpha(), (width, height))
    diamond = Gem((left, top), diamondImage)
    diamond.draw(DISPLAYSURF)

def drawHexagonSprite(color, left, top, width, height):
    hexagonImage = None; 
    if(HEXAGON_ASSETPATH[color]):
        hexagonImage = HEXAGON_ASSETPATH[color];
    hexagonImage = pygame.transform.scale(pygame.image.load(hexagonImage).convert_alpha(), (width, height))
    hexagon = Gem((left, top), hexagonImage)
    hexagon.draw(DISPLAYSURF)

def drawOctagonSprite(color, left, top, width, height):
    octagonImage = None; 
    if(OCTAGON_ASSETPATH[color]):
        octagonImage = OCTAGON_ASSETPATH[color];
    octagonImage = pygame.transform.scale(pygame.image.load(octagonImage).convert_alpha(), (width, height))
    octagon = Gem((left, top), octagonImage)
    octagon.draw(DISPLAYSURF)

def drawSquareSprite(color, left, top, width, height):
    squareImage = None; 
    if(SQUARE_ASSETPATH[color]):
        squareImage = SQUARE_ASSETPATH[color];
    squareImage = pygame.transform.scale(pygame.image.load(squareImage).convert_alpha(), (width, height))
    square = Gem((left, top), squareImage)
    square.draw(DISPLAYSURF)

def drawTriangleSprite(color, left, top, width, height):
    triangleImage = None; 
    if(TRIANGLE_ASSETPATH[color]):
        triangleImage =TRIANGLE_ASSETPATH[color];
    triangleImage = pygame.transform.scale(pygame.image.load(triangleImage).convert_alpha(), (width, height))
    triangle = Gem((left, top), triangleImage)
    triangle.draw(DISPLAYSURF)

class Gem(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image 
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect);


def main():
    global DISPLAYSURF 
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

